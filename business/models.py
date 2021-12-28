from django.db import models
from django import forms
from business import DEAL, PRODUCT
from django.conf import settings
from math import fsum
from django.shortcuts import reverse

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    contact_phone = models.CharField(max_length=255, null=True, blank=True)
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

class Deal(models.Model):
    # type = models.CharField(choices=DEAL.TYPE_CHOICES, max_length=50)
    status = models.CharField(choices=DEAL.STATUS_CHOICES, max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="deals")
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_private = models.BooleanField(default=True)
    trade_value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    trade_information = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to="deals/", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.company.name} / {self.get_total_value()}"

    def get_total_value(self):
        return fsum([self.get_total_cash_value(), self.trade_value or 0])

    def get_total_cash_value(self):
        return fsum([product.value for product in self.products.all()])

class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=PRODUCT.TYPE_CHOICES, max_length=50)
    is_active = models.BooleanField(default=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="products", help_text="Enter cash value of this product in $")
    value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.get_type_display()} Product"

    def subclass(self):
        if self.type == "magazine":
            return self.magazine
        elif self.type == "website":
            return self.website
        elif self.type == "newsletter":
            return self.newsletter
        elif self.type == "flag":
            return self.flag
        elif self.type == "event":
            return self.event
        elif self.type == "popup":
            return self.popup
        elif self.type == "other":
            return self.other
        else:
            return None

    def get_detail_url(self):
        return reverse(f"{self.type}_product", kwargs={"pk": self.subclass().pk})

class Magazine(Product):
    size = models.CharField(choices=PRODUCT.SIZES, max_length=255)
    placement = models.CharField(choices=PRODUCT.PLACEMENTS, max_length=255)
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="products/magazine/", null=True, blank=True)
    is_color = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Magazine Product {self.get_size_display()}"

    def get_icon(self):
        return "fas fa-book-open"

class Website(Product):
    media = models.ImageField(upload_to="products/website/", null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Website Product"

    def get_icon(self):
        return "fa fa-globe"

class Newsletter(Product):
    months = models.PositiveIntegerField()
    size = models.CharField(choices=PRODUCT.NEWSLETTER_SIZES, max_length=50)
    
    def __str__(self) -> str:
        return f"Newsletter Product"

    def get_icon(self):
        return "fas fa-inbox"

class Flag(Product):
    image = models.ImageField(upload_to="products/flag/", null=True, blank=True)
    months = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Flag Product"

    def get_icon(self):
        return "fas fa-flag"

class Event(Product):
    def __str__(self) -> str:
        return f"Event Product"

    def get_icon(self):
        return "far fa-calendar-alt"

class Popup(Product):
    date = models.DateTimeField()
    duration = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Popup Product"

    def get_icon(self):
        return "fa fa-handshake"

class Other(Product):
    def __str__(self) -> str:
        return f"Other Product"

    def get_icon(self):
        return "fas fa-question"