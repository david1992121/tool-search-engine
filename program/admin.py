from program.models import ProgramsList, ToolingsList, NonePermanent
from django.contrib import admin

# Register your models here.


class ProgramAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'onum',
        'tooling',
        'model_num',
        'parts_name',
        'folder_path',
        'create_date']
    list_filter = ['onum', 'tooling']


class ToolingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'program',
        'onum',
        'item_code',
        'tnum',
        'tool_name',
        'folder_path']
    list_filter = ['onum', 'tnum']


class NonePermanentAdmin(admin.ModelAdmin):
    list_display = ['tooling', 'tnum']


admin.site.register(ProgramsList, ProgramAdmin)
admin.site.register(ToolingsList, ToolingAdmin)
admin.site.register(NonePermanent, NonePermanentAdmin)
