import json

from django.views import View
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from scans.models import Scan, Issue


@method_decorator(csrf_exempt, name="dispatch")
class ScansView(View):
    def put(self, request: HttpRequest, jenkins_id: int) -> JsonResponse:
        data = json.loads(request.body)
        scan, _ = Scan.objects.get_or_create(jenkins_id=jenkins_id)
        scan.task_id = data.get("task_id")
        scan.progress = data["scan_metrics"]["crawl_and_audit_progress"]
        scan.save()

        issue_list = []
        for event in data.get("issue_events", []):
            if event.get("type") != "issue_found":
                continue

            issue = event["issue"]
            issue_list.append(
                Issue(
                    scan=scan,
                    name=issue.get("name"),
                    origin=issue.get("origin"),
                    path=issue.get("path"),
                    severity=issue.get("severity"),
                    confidence=issue.get("confidence"),
                    issue_background=issue.get("issue_background", None),
                    remediation_background=issue.get("remediation_background", None)
                )
            )

        if issue_list:
            Issue.objects.bulk_create(issue_list)

        return JsonResponse({"status": "ok"})

    def get(self, request: HttpRequest, jenkins_id: int):
        scan: Scan = get_object_or_404(klass=Scan, jenkins_id=jenkins_id)
        return render(request, 'scans/issues.html', {"vulnerabilities": Issue.objects.filter(scan=scan)})


