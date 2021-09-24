from .models import ProgramsList, ToolingsList
from rest_framework import serializers

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProgramsList

class ToolingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ToolingsList

class ToolingDataSerializer(serializers.Serializer):
    tnum = serializers.CharField()
    tool_name = serializers.CharField()
    holder_name = serializers.CharField()
    tooling = serializers.CharField()


        