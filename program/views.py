from program.serializers import ProgramSerializer, ToolCheckHistorySerializer, ToolCheckSave, ToolingDataSerializer, ToolCheckDetailSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import ProgramsList, ToolCheckDetail, ToolCheckHistory, ToolingsList
from django.db.models import Q
from datetime import datetime
from django.conf import settings
import json
import os
import mimetypes
import shutil
from django.core.paginator import EmptyPage, Paginator
from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_toolings(request):
    """
    加工機のリスト取得
    """
    toolingList = list(ProgramsList.objects.values('tooling').distinct())
    returnList = [x['tooling'] for x in toolingList]
    return Response(returnList, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_programs(request):
    """
    プログラムのリスト取得
    """
    tooling = request.query_params.get("tooling", "")
    keyword = request.query_params.get("keyword", "")
    is_item = request.query_params.get("is_item", "")
    page_index = int(request.query_params.get("page", "1"))

    queryset = ProgramsList.objects
    if tooling == "" and keyword == "":
        queryset = queryset.all()
    else:
        if tooling != "":
            queryset = queryset.filter(tooling=tooling)

        if keyword != "":
            if is_item == "true":
                queryset = queryset.filter(item_code__exact=keyword)
            else:
                queryset = queryset.filter(Q(onum__icontains=keyword) | Q(
                    model_num__icontains=keyword) | Q(item_code__icontains=keyword))

    queryset = queryset.order_by("-create_date")
    page_size = 5
    paginator = Paginator(queryset, page_size)
    try:
        program_data = paginator.page(page_index)
        return Response(ProgramSerializer(program_data, many=True).data)
    except EmptyPage:
        return Response(data=[])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tools(request):
    id_str = request.query_params.get("program_ids", "")
    page_index = int(request.query_params.get("page", "1"))
    if id_str != "":
        try:
            id_array = json.loads(id_str)
        except BaseException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(id_array) > 0:
            toolings = ToolingsList.objects.filter(
                program__id__in=id_array).order_by(
                'tooling', 'tnum')
            distinct_toolings = toolings.values(
                'tooling', 'tnum', 'tool_name', 'holder_name', 'tip_name').distinct()
            page_size = 20
            paginator = Paginator(distinct_toolings, page_size)
            try:
                tooling_data = paginator.page(page_index)
                return Response(
                    ToolingDataSerializer(
                        tooling_data,
                        many=True).data)
            except EmptyPage:
                return Response(data=[])
        else:
            return Response([])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_pdf(request):
    id_str = request.query_params.get("id", "")
    type_str = request.query_params.get("type", "")

    if id_str.strip() == "":
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            program = ProgramsList.objects.get(id=int(id_str))
            folder_path = program.folder_path
            if folder_path:
                file_name = "{0}.pdf".format(
                    program.onum) if type_str == "" else "{0}_3d.pdf".format(
                    program.onum)
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    branch_path = "static/pdfs/{0}/{1}".format(
                        datetime.now().strftime("%Y%m%d"), request.user.id)
                    cur_folder = os.path.join(settings.BASE_DIR, branch_path)
                    if not os.path.exists(cur_folder):
                        os.makedirs(cur_folder)
                    target_path = os.path.join(cur_folder, file_name)
                    if os.path.exists(target_path):
                        os.remove(target_path)
                    shutil.copyfile(file_path, target_path)
                    return Response(
                        "{0}/{1}".format(branch_path, file_name), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ProgramsList.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_check_history(request):
    serializer = ToolCheckSave(data=request.data)
    if serializer.is_valid():
        input_data = serializer.validated_data
        tool_check_history = ToolCheckHistory.objects.create(
            user=request.user,
            number=input_data["number"],
            tooling=input_data["tooling"],
            program_info=input_data["onum"],
            started_at=input_data["started_at"])
        return Response(ToolCheckHistorySerializer(tool_check_history).data)
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_check_detail(request):
    serializer = ToolCheckDetailSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_check_histories(request):
    tooling = request.query_params.get("tooling", "")
    number = int(request.query_params.get("number", "0"))
    date = request.query_params.get("date", "")
    user_id = request.query_params.get("user", "")
    page_index = int(request.query_params.get("page", "1"))

    query_set = ToolCheckHistory.objects.all()
    if tooling != "":
        query_set = query_set.filter(tooling=tooling)
    if number > 0:
        query_set = query_set.filter(number=number)
    if date != "":
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        query_set = query_set.filter(
            created_at__year=date_obj.year,
            created_at__month=date_obj.month,
            created_at__day=date_obj.day)
    if user_id != "":
        query_set = query_set.filter(user__id=user_id)

    query_set = query_set.order_by("-created_at")
    page_size = 20
    paginator = Paginator(query_set, page_size)
    try:
        history_data = paginator.page(page_index)
        return Response(
            ToolCheckHistorySerializer(
                history_data,
                many=True).data)
    except EmptyPage:
        return Response(data=[])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_check_detail(request):
    detail_id = int(request.query_params.get("detail_id", "0"))
    page_index = int(request.query_params.get("page", "1"))
    if detail_id > 0:
        details = ToolCheckDetail.objects.filter(
            history__id=detail_id).order_by(
            'tooling', 'tnum')
        page_size = 20
        paginator = Paginator(details, page_size)
        try:
            detail_data = paginator.page(page_index)
            return Response(
                ToolCheckDetailSerializer(
                    detail_data, many=True).data)
        except EmptyPage:
            return Response(data=[])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_check_history(request, id):
    try:
        detail = ToolCheckHistory.objects.get(pk=id)
        return Response(ToolCheckHistorySerializer(detail).data)
    except ToolCheckHistory.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
