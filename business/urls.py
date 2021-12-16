from django.urls import path, include
from .views import *

urlpatterns = [
    path("issues/", issues.as_view(), name="issues"),
    path("issues/<pk>/", issue_detail.as_view(), name="issue_detail"),
]