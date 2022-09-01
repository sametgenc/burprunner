from django.contrib import admin
from scans.models import Scan, Issue


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ["jenkins_id", "issue_count", "progress"]
    readonly_fields = ["jenkins_id", "created_at", "updated_at", "task_id", "progress"]

    class Meta:
        model = Scan


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["name", "origin", "path", "severity"]
    readonly_fields = [
        "name",
        "origin",
        "path",
        "severity",
        "confidence",
        "issue_background",
        "remediation_background",
    ]

    class Meta:
        model = Issue
