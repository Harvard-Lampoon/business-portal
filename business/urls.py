from django.urls import path, include
from .views import *

urlpatterns = [
    path("issues/", issues.as_view(), name="issues"),
    path("issues/<pk>/", issue_detail.as_view(), name="issue_detail"),
    path("companies/", companies.as_view(), name="companies"),
    path("companies/<pk>/", company_detail.as_view(), name="company_detail"),
    path("deal-all/", public_deals.as_view(), name="public_deals"),
    path("my-deals/", my_deals.as_view(), name="my_deals"),
    path("create/deals/", create_deal, name="create_deal"),
    path("deals/<pk>/", deal_detail.as_view(), name="deal_detail"),
    path("create/get-data/company/", create_deal_get_data_company, name="create_deal_get_data_company"),
    path("create/deals/magazine/<deal_pk>/", create_magazine_product.as_view(), name="create_magazine_product"),
    path("create/deals/website/<deal_pk>/", create_website_product.as_view(), name="create_website_product"),
    path("create/deals/newsletter/<deal_pk>/", create_newsletter_product.as_view(), name="create_newsletter_product"),
    path("create/deals/flag/<deal_pk>/", create_flag_product.as_view(), name="create_flag_product"),
    path("create/deals/event/<deal_pk>/", create_event_product.as_view(), name="create_event_product"),
    path("create/deals/popup/<deal_pk>/", create_popup_product.as_view(), name="create_popup_product"),
    path("create/deals/other/<deal_pk>/", create_other_product.as_view(), name="create_other_product"),
    path("products/magazine/<pk>/", magazine_product.as_view(), name="magazine_product"),
    path("products/website/<pk>/", website_product.as_view(), name="website_product"),
    path("products/newsletter/<pk>/", newsletter_product.as_view(), name="newsletter_product"),
    path("products/flag/<pk>/", flag_product.as_view(), name="flag_product"),
    path("products/event/<pk>/", event_product.as_view(), name="event_product"),
    path("products/popup/<pk>/", popup_product.as_view(), name="popup_product"),
    path("products/other/<pk>/", other_product.as_view(), name="other_product"),
]