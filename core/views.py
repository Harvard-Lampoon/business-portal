from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from business.models import Deal
from datetime import datetime
from docusign.models import ApiClient

@login_required
def home(request):
    if not ApiClient.objects.filter(is_active=True).exists():
        return redirect(ApiClient.objects.get_auth_code_uri(request))
    context = {
        "monthly_data": Deal.objects.get_monthly_data()
    }
    return render(request, "index.html", context)

