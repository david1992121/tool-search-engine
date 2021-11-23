from user.serializers import UserSerializer
from .models import NonePermanent, ProgramsList, ToolingsList, ToolCheckHistory, ToolCheckDetail
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
    is_non_permanent = serializers.SerializerMethodField('get_non_permanent')
    tnum = serializers.IntegerField()
    tool_name = serializers.CharField()
    holder_name = serializers.CharField()
    tooling = serializers.CharField()
    tip_name = serializers.CharField()

    def get_non_permanent(self, obj):
        return NonePermanent.objects.filter(tooling = obj['tooling'], tnum = obj['tnum']).count() > 0

class ToolCheckDetailSerializer(serializers.ModelSerializer):
    history_id = serializers.IntegerField(write_only = True)
    
    class Meta:
        model = ToolCheckDetail
        exclude = ('history', )


class ToolCheckHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = '__all__'
        model = ToolCheckHistory

class ToolCheckSave(serializers.Serializer):
    tooling = serializers.CharField()
    onum = serializers.CharField()
    started_at = serializers.CharField()
    number = serializers.IntegerField()
