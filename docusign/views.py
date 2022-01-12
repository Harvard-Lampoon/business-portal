from datetime import time, timezone
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
import requests
from requests.api import get
from business.models import Deal
from docusign.models import ApiClient
from docusign.utils import make_envelope
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
import io
from django.core.files import File
import logging
logger = logging.getLogger("django")


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
    deal = get_object_or_404(Deal, pk = deal_pk, created_by = request.user)
    client = ApiClient.objects.get_client(request)
    print(client)
    print("making env...")
    envelope = make_envelope(deal, request)
    response = client.send_document(envelope)
    deal.status = "pending"
    deal.save()
    print("RESPONSE", response)
    messages.success(request, "Succesfully sent signature request...")
    return redirect(reverse("deal_detail", kwargs={"pk": deal.pk}))

def preview_contract(request, deal_pk):
    deal = get_object_or_404(Deal, pk = deal_pk)
    if request.user==deal.created_by or request.user.is_staff:
        company_name = deal.company.name.replace(" ", "_")
        return FileResponse(deal.generate_pdf(request).file, as_attachment=True, filename=f"Harvard_Lampoon_{company_name}_Contract.pdf")
    raise Http404()

@csrf_exempt
def document_signed(request):
    print("DOCUMENT SIGNED!!!!")
    print(request)
    print("POST: ", request.POST)
    print("GET: ", request.GET)
    print(request.FILES)
    logger.warning(f"{request}, GET: {request.GET}, POST: {request.POST}, FILES: {request.FILES}, body: {request.body}")
    data = json.loads(request.body)
    signed_pdf = io.BytesIO(data["envelopeDocuments"][0]["PDFBytes"].encode("utf-8"))
    logger.warning(signed_pdf)
    file_name = "Signed_{}".format(data["envelopeDocuments"][0]["name"])
    deal_pk = data["customFields"]["textCustomFields"][0]["value"]
    deal = get_object_or_404(Deal, pk=deal_pk)
    deal.pdf.save(file_name, File(signed_pdf))
    deal.signed_at = timezone.now()
    deal.status = "confirmed"
    deal.save()
    # Get deal pk from /restapi/v2.1/accounts/{accountId}/envelopes/{envelopeId}/custom_fields
    # List documents to get document ID
    # Get document pdf and update deal
    
    # deal.signed_at = timezone.now()
    return JsonResponse({"status": "success"})
