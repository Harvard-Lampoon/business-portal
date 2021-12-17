from django.db import models

from business import CONTRACT, AD
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Issue(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Contract(models.Model):
    type = models.CharField(choices=CONTRACT.TYPE_CHOICES, max_length=50)
    status = models.CharField(choices=CONTRACT.STATUS_CHOICES, max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=50)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.company.name} / {self.value}"

class Advertisement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=AD.TYPE_CHOICES, max_length=50)
    is_active = models.BooleanField(default=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="ads")

    cash_value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    trade_value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    trade_contents = models.TextField(null=True, blank=True)

    notes = models.TextField(null=True, blank=True)


    def __str__(self) -> str:
        return f"{self.get_type_display()} Ad"

class Magazine(Advertisement):
    size = models.CharField(choices=AD.SIZES, max_length=255)
    placement = models.CharField(choices=AD.PLACEMENTS, max_length=255)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="ads/magazine/", null=True, blank=True)
    is_color = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Magazine Ad {self.size}"

class Website(Advertisement):
    media = models.ImageField(upload_to="ads/website/", null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Website Ad"

class Newsletter(Advertisement):
    months = models.PositiveIntegerField()
    size = models.CharField(choices=AD.NEWSLETTER_SIZES, max_length=50)
    
    def __str__(self) -> str:
        return f"Newsletter Ad"

class Flag(Advertisement):
    image = models.ImageField(upload_to="ads/flag/", null=True, blank=True)
    months = models.PositiveIntegerField()
    deployed = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Flag Ad"


class Event(Advertisement):
    def __str__(self) -> str:
        return f"Event Ad"

class Popup(Advertisement):
    date = models.DateTimeField()
    duration = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Popup Ad"