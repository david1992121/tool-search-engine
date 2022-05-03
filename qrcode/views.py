from qrcode.models import Qrcode
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_item_code(request):
    code_str = request.query_params.get('code', "")
    if code_str != "" and code_str.lstrip("0"):
        code_str = code_str.lstrip("0")
        qr_code = Qrcode.objects.using('qr').filter(aufnr=code_str).first()
        if qr_code:
            return Response(qr_code.matnr, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
