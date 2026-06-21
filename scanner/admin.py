from django.contrib import admin
from .models import Scan, UrlScan


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("file_name", "verdict", "user", "created_at")
    list_filter = ("verdict",)
    search_fields = ("file_name", "file_hash")


@admin.register(UrlScan)
class UrlScanAdmin(admin.ModelAdmin):
    list_display = ("url", "verdict", "user", "created_at")
    list_filter = ("verdict",)
    search_fields = ("url",)