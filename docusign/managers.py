from django.db import models
from django.db.models import base
from django.http.response import Http404
import requests
from django.conf import settings
from django.shortcuts import redirect, reverse
import base64
import json
from django.utils import timezone

class ApiClientManager(models.Manager):
    # Returns object, created (bool)

    def get_auth_code_uri(self, request):
        return f"{settings.DS_BASE_URI}/auth?response_type=code&scope=signature&client_id={settings.DS_INTEGREATION_KEY}&redirect_uri={request.build_absolute_uri(reverse('ds_callback'))}"

    def get_client(self, request):
        print("getting client")
        clients = self.get_queryset().filter(is_active=True)
        print(clients)
        if clients.exists():
            client = clients.first()
            client.handle_refresh()
            return client
        print("no existing client")
        raise Http404
        
    def finish_creation(self, authorization_code):
        base_url = settings.DS_BASE_URI
        integrator_and_secret_key = b"Basic " + base64.b64encode(str.encode("{}:{}".format(settings.DS_INTEGREATION_KEY, settings.DS_SECRET_KEY)))
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": integrator_and_secret_key.decode("utf-8")
        }
        print(headers)
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
        }
        print(data)
        # GET ACCESS TOKEN
        try:
            response = requests.post(base_url + "/token", headers=headers, data=json.dumps(data))
            last_refresh = timezone.now()
            print(response.url)
            data = response.json()
            print(data)
            access_token = data["access_token"]
            refresh_token = data["refresh_token"]
            expires_in = data["expires_in"]
            
        except:
            print("Issue with obtaining first access token")
            raise Http404
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        # GET ACCOUNT ID AND BASE URI
        try:
            response = requests.get(base_url + "/userinfo", headers=headers)
            
            data = response.json()
            print(data)
            account_id = data["accounts"][0]["account_id"]
            base_uri = data["accounts"][0]["base_uri"]
        except:
            print("Issue with obtaining account id & base uri")
            raise Http404
        
        client = super().create(
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
            authorization_code = authorization_code,
            account_id = account_id, 
            base_uri = base_uri,
            last_refresh = last_refresh
        )
        return client
