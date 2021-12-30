from django.db import models
from datetime import datetime
import calendar

class DealManager(models.Manager):
    def get_monthly_data(self):
        data = []
        for i in range(1, datetime.now().month + 1):
            deals = self.get_queryset().filter(signed_at__month=i)
            sum = 0
            for deal in deals:
                sum+= deal.get_total_value()
            data.append({'x': calendar.month_name[i], 'y': sum})
        return data