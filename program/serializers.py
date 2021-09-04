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
        