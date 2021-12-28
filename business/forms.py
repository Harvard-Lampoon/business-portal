from django import forms
from business.models import *

class MagazineForm(forms.ModelForm):
     class Meta:
         model = Magazine
         fields = '__all__'

class WebsiteForm(forms.ModelForm):
     class Meta:
         model = Website
         fields = "__all__"

class NewsletterForm(forms.ModelForm):
     class Meta:
         model = Newsletter
         fields = "__all__"

class FlagForm(forms.ModelForm):
     class Meta:
         model = Flag
         fields = "__all__"

class EventForm(forms.ModelForm):
     class Meta:
         model = Popup
         fields = "__all__"

class PopupForm(forms.ModelForm):
     class Event:
         model = Popup
         fields = "__all__"

class OtherForm(forms.ModelForm):
     class Meta:
         model = Other
         fields = "__all__"
