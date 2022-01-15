from django.db import models
from datetime import datetime
import calendar

class DealManager(models.Manager):
    def get_monthly_data(self):
        data = []
        for i in range(1, datetime.now().month + 1):
            deals = self.get_queryset().filter(signed_at__month=i, status="confirmed")
            sum = 0
            for deal in deals:
                sum+= deal.get_total_value()
            data.append(sum)
        return data
    
    def get_public_deals(self):
        return self.get_queryset().filter(is_private=False).order_by("-created_at")