from django.db import models

from business import DEAL, AD
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
    release_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Deal(models.Model):
    type = models.CharField(choices=DEAL.TYPE_CHOICES, max_length=50)
    status = models.CharField(choices=DEAL.STATUS_CHOICES, max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=50)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.company.name} / {self.value} / {self.issue.name}"

class Ad(models.Model):
    size = models.CharField(choices=AD.SIZES, max_length=255)
    placement = models.CharField(choices=AD.PLACEMENTS, max_length=255)
    is_active = models.BooleanField(default=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ads/", null=True, blank=True)
    is_color = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.size} / {self.deal.company} / {self.deal.issue.name}"