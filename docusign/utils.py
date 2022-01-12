import base64
import os
from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs, Recipients
from django.template.loader import render_to_string
from django.shortcuts import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import logging
logger = logging.getLogger("django")

def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
        link_callback=link_callback
        )
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def make_envelope(deal, request):
    event_notification_url = request.build_absolute_uri(reverse('document_signed'))
    data = {
        "status": "sent",
        "documents": [
            {
                "documentBase64": base64.b64encode(deal.generate_pdf(request).file.read()).decode("ascii"),
                "documentId": "1",
                "fileExtension": "pdf",
                "name": "Harvard_Lampoon_Contract.pdf"
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
                                "anchorString": "**client_signature**",
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
            "url": event_notification_url,
            "requireAcknowledgment": "true",
            "loggingEnabled": "true",
            "recipientEvents": [
                {
                    "recipientEventStatusCode": "Completed",
                    "includeDocuments": "false"
                },
            ]
        }
    }
    print("URL: ", event_notification_url)
    logger.warning("test log")
    logger.warning(f"URL: {event_notification_url}")
    return data