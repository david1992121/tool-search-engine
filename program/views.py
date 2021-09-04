from program.serializers import ProgramSerializer, ToolingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import ProgramsList, ToolingsList
from django.db.models import Q
import json

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
            return Response(ToolingSerializer(toolings, many = True).data)
        else:
            return Response([])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


