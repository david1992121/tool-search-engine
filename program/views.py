from program.serializers import ProgramSerializer, ToolingDataSerializer, ToolingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import ProgramsList, ToolingsList
from django.db.models import Q
from django.http.response import HttpResponse
import json, os, mimetypes
from wsgiref.util import FileWrapper

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_toolings(request):
    """
    加工機のリスト取得
    """
    toolingList = list(ProgramsList.objects.values('tooling').distinct())
    returnList = [x['tooling'] for x in toolingList]
    return Response(returnList, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_programs(request):
    """
    プログラムのリスト取得
    """
    tooling = request.query_params.get("tooling", "")
    keyword = request.query_params.get("keyword", "")
    is_item = request.query_params.get("is_item", "")


    queryset = ProgramsList.objects
    if tooling == "" and keyword == "":
        queryset = queryset.all()
    else:
        if tooling != "":
            queryset = queryset.filter(tooling = tooling)

        if keyword != "":
            if is_item == "true":
                queryset = queryset.filter(item_code__exact = keyword)
            else:
                queryset = queryset.filter(Q(onum__icontains = keyword) | Q(model_num__icontains = keyword) | Q(item_code__icontains = keyword))

    queryset = queryset.order_by("-create_date")

    return Response(ProgramSerializer(queryset, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tools(request):
    id_str = request.query_params.get("program_ids", "")
    if id_str != "":
        try:
            id_array = json.loads(id_str)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if len(id_array) > 0:
            toolings = ToolingsList.objects.filter(program__id__in = id_array).order_by('tooling', 'tnum')
            distinct_toolings = toolings.values('tooling', 'tnum', 'tool_name', 'holder_name').distinct()
            return Response(ToolingDataSerializer(distinct_toolings, many = True).data)
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
            program = ProgramsList.objects.get(id = int(id_str))
            folder_path = program.folder_path
            if folder_path:
                file_name = "{0}.pdf".format(program.onum) if type_str == "" else "{0}_3d.pdf".format(program.onum)
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    wrapper = FileWrapper(open(file_path,'rb'))
                    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(file_path)[0])
                    response['Content-Length'] = os.path.getsize(file_path)
                    response['Content-Disposition'] = "attachment; filename=" + file_name
                    response['Access-Control-Expose-Headers'] = "Content-Disposition"
                    return response
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except ProgramsList.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


