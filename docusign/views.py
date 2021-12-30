from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
import requests
from requests.api import get
from business.models import Deal
from docusign.models import ApiClient
from docusign.utils import make_envelope

def confirm_connection(request):
    print(request.GET)
    code = request.GET.get("code", None)
    print("CODE", code)
    if not code:
        print("Issue obtaining code in redirect uri")
        raise Http404
    print("WORKING")
    client = ApiClient.objects.finish_creation(code)
    messages.success(request, "Docusign connection is now setup")
    return redirect(reverse("home"))

def request_signature(request, deal_pk):
    client = ApiClient.objects.get_client(request)
    print(client)
    print("making env...")
    deal = get_object_or_404(Deal, pk = deal_pk, created_by = request.user)
    envelope = make_envelope(deal, request)
    response = client.send_document(envelope)
    print("RESPONSE", response)
    messages.success(request, "Succesfully sent signature request...")
    return redirect(reverse("deal_detail", kwargs={"pk": deal.pk}))

def document_signed(request):
    print("DOCUMENT SIGNED!!!!")
    print(request)
    print(request.GET)
    print(request.FILES)
    return JsonResponse({"status": "success"})