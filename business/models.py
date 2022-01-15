from io import BytesIO
from django.db import models
from django import forms
from business import DEAL, PRODUCT
from django.conf import settings
from math import fsum
from django.shortcuts import reverse
from docusign.utils import render_to_pdf
from docusign.models import ApiClient
from docusign.utils import make_envelope
from .managers import DealManager
import decimal

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255, null=True, blank=True)
    contact_position = models.CharField(max_length=100, null=True, blank=True)
    billing_address = models.CharField(max_length=255)
    city_state_zip = models.CharField(max_length=255)
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
    info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    trade_value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    cash_payment = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    pdf = models.FileField(upload_to="deals/", null=True, blank=True)

    objects = DealManager()

    def __str__(self) -> str:
        return f"{self.company.name} / {self.get_total_value()}"

    def get_total_value(self):
        return fsum([self.cash_payment or 0, self.trade_value or 0])

    def get_product_value(self):
        return fsum([product.get_true_value() for product in self.products.all()])

    def generate_pdf(self, request):
        self.pdf.delete()
        context = {
            "deal": self,
            "request": request
        }
        pdf = render_to_pdf('pdfs/deal-contract.html', context)
        self.pdf.save("Harvard_Lampoon_Contract", (BytesIO(pdf.content)))
        return self.pdf

    def get_signed_at_number(self):
        if self.signed_at:
            return self.signed_at.strftime("%Y%m%d")
        return None

class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=PRODUCT.TYPE_CHOICES, max_length=50)
    is_active = models.BooleanField(default=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="products", help_text="Enter cash value of this product in $")
    value = models.DecimalField(decimal_places=2, max_digits=50, null=True, blank=True)
    discount = models.PositiveIntegerField("Discount Percentage", default=0, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.get_type_display()} Product"

    def subclass(self):
        return eval("self." + self.type)

    def get_detail_url(self):
        return reverse(f"{self.type}_product", kwargs={"pk": self.subclass().pk})

    def get_true_value(self):
        if self.discount:
            return round(self.value*(1 - decimal.Decimal(self.discount/100)), 2)
        return self.value

    def get_issue(self):
        if self.type == "magazine":
            return self.magazine.issue.name or "Unknown"
        return "NA"

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
    
    def get_description(self):
        return f"{self.get_size_display()} {self.get_placement_display()} Ad"


class Website(Product):
    media = models.ImageField(upload_to="products/website/", null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Website Product"

    def get_icon(self):
        return "fa fa-globe"

    def get_description(self):
        return f"Website Ad"


class Newsletter(Product):
    months = models.PositiveIntegerField()
    size = models.CharField(choices=PRODUCT.NEWSLETTER_SIZES, max_length=50)
    
    def __str__(self) -> str:
        return f"Newsletter Product"

    def get_icon(self):
        return "fas fa-inbox"

    def get_description(self):
        return f"{self.months} months {self.get_size_display()} Newsletter"

class Flag(Product):
    image = models.ImageField(upload_to="products/flag/", null=True, blank=True)
    months = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Flag Product"

    def get_icon(self):
        return "fas fa-flag"

    def get_description(self):
        return f"{self.months} months Flag"


class Event(Product):
    def __str__(self) -> str:
        return f"Event Product"

    def get_icon(self):
        return "far fa-calendar-alt"

    def get_description(self):
        return f"Event Ad"

class Popup(Product):
    date = models.DateTimeField()
    duration = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Popup Product"

    def get_icon(self):
        return "fa fa-handshake"

    def get_description(self):
        return f"{self.date} Popup"

class Other(Product):
    def __str__(self) -> str:
        return f"Other Product"

    def get_icon(self):
        return "fas fa-question"

    def get_description(self):
        return f"Other"