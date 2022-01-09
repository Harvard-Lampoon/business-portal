from django.db import models
from django.http.response import Http404
from requests.api import head
from .managers import ApiClientManager
from django.utils import timezone
from django.conf import settings
import requests
import json
from .utils import make_envelope
import base64

class ApiClient(models.Model):
    access_token = models.TextField(max_length=2000, null=True, blank=True)
    authorization_code = models.TextField(max_length=2000, null=True, blank=True)
    refresh_token = models.TextField(max_length=2000, null=True, blank=True)
    base_uri = models.CharField(max_length=255, null=True, blank=True)
    account_id = models.CharField(max_length=255, null=True, blank=True)
    last_refresh   = models.DateTimeField(null=True, blank=True)
    expires_in = models.PositiveBigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ApiClientManager()

    def __str__(self) -> str:
        return f"ApiClient {self.last_refresh}"

    def refresh(self):
        print("Refreshing API Client")
        integrator_and_secret_key = b"Basic " + base64.b64encode(str.encode("{}:{}".format(settings.DS_INTEGREATION_KEY, settings.DS_SECRET_KEY)))
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": integrator_and_secret_key.decode("utf-8")
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        try:
            response = requests.post(settings.DS_BASE_URI + "/token", headers=headers, data=json.dumps(data))
            print(response)
            data = response.json()
            self.last_refresh = timezone.now()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]
            self.expires_in = data["expires_in"]
            self.save()
        except:
            print("Issue with refreshing access token")
            raise Http404("Issue with refreshing access token")

    def handle_refresh(self):
        delta_time = timezone.now() - self.last_refresh
        if delta_time.seconds > self.expires_in - 60:
            self.refresh()
            return True
        return False
        

    def send_document(self, envelope):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        try:
            print(headers)
            print(envelope)
            response = requests.post(f"{self.base_uri}/restapi/v2.1/accounts/{self.account_id}/envelopes", headers=headers, data=json.dumps(envelope))
            print(response.url)
            print("RESPONSE", response)
            data = response.json()
            print(data)
            return response
        except:
            print("Issue with sending document to sign")
            raise Http404("Issue with sending document to sign")
