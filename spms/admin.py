from django.contrib import admin
from .models import CBSPerformance

@admin.register(CBSPerformance)
class CBSPerformanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CBSPerformance._meta.get_fields()]

    def get_queryset(self, request):
        return super().get_queryset(request).using('dospms')
