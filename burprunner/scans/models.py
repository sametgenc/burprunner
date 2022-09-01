from django.db import models


class Scan(models.Model):
    jenkins_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task_id = models.IntegerField(null=True, blank=True)
    progress = models.FloatField(default=0.0)

    @property
    def issue_count(self):
        return Issue.objects.filter(scan=self).count()

    def __str__(self):
        return f"{self.jenkins_id}"


class Issue(models.Model):
    scan = models.ForeignKey(
        "scans.Scan",
        related_name="scan_issues",
        related_query_name="scan_issue",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255)
    issue_background = models.TextField(null=True, blank=True)
    remediation_background = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
