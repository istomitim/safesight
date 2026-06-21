import hashlib

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Scan, UrlScan
from .services import check_hash_on_virustotal, check_url_on_virustotal, take_screenshot

@login_required # # only logged-in users access
def home(request):
    last_result = None

    # User clicks "Check
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # Check FILE
        if form_type == "file":
            uploaded_file = request.FILES["file"]

            # Hash calculations, reading it in chunks
            sha256 = hashlib.sha256()
            for chunk in uploaded_file.chunks():
                sha256.update(chunk)

            file_hash = sha256.hexdigest()

            # Conneciton to VirusTotal API
            verdict = check_hash_on_virustotal(file_hash)

            # Save the scan to the database
            scan = Scan.objects.create(
                user=request.user,
                file_name=uploaded_file.name,
                file_hash=file_hash,
                verdict=verdict,
            )
            last_result = {
                "name": scan.file_name,
                "verdict": scan.verdict,
                "badge": scan.badge_class(), # colour
                "type": "file",
            }

        # Check URL
        elif form_type == "url":
            url = request.POST.get("url")
            verdict = check_url_on_virustotal(url)
            screenshot = take_screenshot(url)
            scan = UrlScan.objects.create(
                user=request.user,
                url=url,
                verdict=verdict,
                screenshot=screenshot,
            )
            last_result = {
                "name": scan.url,
                "verdict": scan.verdict,
                "badge": scan.badge_class(),
                "type": "url",
                "screenshot": scan.screenshot,
            }

    file_scans = Scan.objects.filter(user=request.user)
    url_scans = UrlScan.objects.filter(user=request.user)

    # Filter - sort by date
    recent = sorted(
        list(file_scans) + list(url_scans),
        key=lambda s: s.created_at,
        reverse=True,
    )

    context = {
        "last_result": last_result,
        "recent": recent,
    }

    # Built HTML page from the template
    return render(request, "scanner/home.html", context)


# Full history page
@login_required
def history(request):
    scans = Scan.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "scans": scans,
        "total": scans.count(),
    }
    return render(request, "scanner/history.html", context)