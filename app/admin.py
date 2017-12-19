from django.contrib import admin
from app.models import Info,Total
class InfoAdmin(admin.ModelAdmin):
    search_fields = ('name','date','amount','ttype')
admin.site.register(Info,InfoAdmin)
admin.site.register(Total)
