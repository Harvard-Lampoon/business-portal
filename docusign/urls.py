from .views import *
from django.urls import path

urlpatterns = [
    path("callback/", confirm_connection, name="ds_callback"),
    path("request-signature/<deal_pk>/", request_signature, name="request_signature"),
    path("document-signed", document_signed, name="document_signed"),
    path("preview-contract/<deal_pk>/", preview_contract, name="preview_contract"),
]
