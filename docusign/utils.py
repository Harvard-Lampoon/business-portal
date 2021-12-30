import base64
from os import path
from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients
from django.template.loader import render_to_string
from django.shortcuts import reverse
def make_envelope(deal, request):
    data = {
        "status": "sent",
        "documents": [
            {
                "documentBase64": base64.b64encode(bytes(render_to_string("emails/request-signature.html", {"test": "12345"}), "utf-8")).decode("ascii"),
                "documentId": 1,
                "fileExtension": "html",
                "name": "Harvard Lampoon Contract"
            }
        ],
        "emailSubject": "Please sign this contract",
        "recipients": {
            "signers": [
                {
                    "email": deal.company.contact_email,
                    "name": deal.company.contact_name,
                    "recipientId": "1",
                    "routingOrder": "1",
                    "tabs": {
                        "signHereTabs": [
                            {
                                "anchorString": "**signature_1**",
                                "anchorUnits": "pixels",
                                "anchorXOffset": "10",
                                "anchorYOffset": "10",
                            }
                        ]
                    }
                }
            ],
            "carbonCopies": [
                {
                    "email": "samsuchin@gmail.com",
                    "name": "Sam Suchin",
                    "recipientId": "2",
                    "routingOrder": "2",
                }
            ]
        },
        "eventNotification": {
            "url": request.build_absolute_uri(reverse('document_signed')),
            "requireAcknowledgment": "true",
            "includeDocuments": "true"
        }
    }

    return data