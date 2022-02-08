from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import CreateView
from business.forms import *
from business.models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from portal.decorators import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.apps import apps

@method_decorator([login_required, business_required], name="dispatch")
class issues(ListView):
    paginate_by = 25
    model = Issue
    template_name = "business/issues.html"
    def get_queryset(self):
        filter_qs = self.request.GET.get("filter", "")
        context = super().get_queryset().filter(Q(name__icontains=filter_qs)).order_by("-release_date")
        return context
    
    def post(self, request, *args, **kwargs):
        issue = Issue.objects.create(
            name=request.POST.get("name"),
            release_date = request.POST.get("release-date")
        )
        return redirect(reverse("issue_detail", kwargs={"pk": issue.pk}))

@method_decorator([login_required, business_required], name="dispatch")
class issue_detail(UpdateView):
    model = Issue
    fields = "__all__"
    template_name = "business/issue-detail.html"

    def post(self, request, *args, **kwargs):
        print(request.POST)
        action = request.POST.get("action", None)
        print(action)
        if action=="Delete":
            obj = self.get_object()
            obj.delete()
            messages.success(request, "{} has been deleted".format(obj.name))
            return redirect(reverse("issues"))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})

@method_decorator([login_required], name="dispatch")
class my_deals(ListView):
    paginate_by = 25
    model = Deal
    template_name = "business/deals.html"
    def get_queryset(self):
        filter_qs = self.request.GET.get("filter", "")
        context = super().get_queryset().filter(created_by=self.request.user).filter(
        Q(company__name__icontains=filter_qs)|
        Q(company__contact_name__icontains=filter_qs)|
        Q(company__contact_email__icontains=filter_qs)
        ).order_by("-created_at")
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Deals"
        return context

@method_decorator([login_required, business_required], name="dispatch")
class public_deals(ListView):
    paginate_by = 25
    model = Deal
    template_name = "business/deals.html"
    def get_queryset(self):
        filter_qs = self.request.GET.get("filter", "")
        context = super().get_queryset().filter(is_private=False).filter(
        Q(created_by__name__icontains=filter_qs)|
        Q(created_by__email__icontains=filter_qs)|
        Q(company__name__icontains=filter_qs)|
        Q(company__contact_name__icontains=filter_qs)|
        Q(company__contact_email__icontains=filter_qs)
        ).order_by("-created_at")
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Public Deals"
        return context

class deal_detail(UpdateView):
    model = Deal
    fields = ["is_private", "trade_value", "cash_payment", "info"]
    template_name = "business/deal-detail.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by == request.user or request.user.account_type=="staff" or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You do not have business staff access or own this deal')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        print(action)
        if action=="Delete":
            obj = self.get_object()
            obj.delete()
            messages.success(request, "{} deal has been deleted".format(obj.company.name))
            return redirect(reverse("my_deals"))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = PRODUCT.TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse('deal_detail', kwargs={'pk': self.object.pk})

@login_required
def create_deal(request):
    companies = Company.objects.filter(is_active=True).order_by("-name")
    if request.method=="POST":
        data = request.POST
        info = data.get("info", " ")
        action = data.get("action")
        if action == "select":
            company = get_object_or_404(Company, pk=data.get("company-pk"))
        elif action == "create":
            company = Company.objects.create(name=data.get("company-name"), contact_name=data.get("contact-name"), contact_email=data.get("contact-email"), billing_address=data.get("billing-address"), city_state_zip=data.get("city-state-zip"))
        else:
            raise Http404()
        
        deal = Deal.objects.create(
            status="created",
            company=company,
            info=info,
            created_by=request.user,
        )
        return redirect(reverse("deal_detail", kwargs={"pk": deal.pk}))
    context = {
        "companies": companies,
    }
    return render(request, "business/create-deal.html", context)

def create_deal_get_data_company(request):
    if request.method=="GET":
        deal_action = request.GET.get("action")
        html = render_to_string("business/create/company_{}.html".format(deal_action), context={"companies": Company.objects.filter(is_active=True)})
        data = {
            "html": html,
            "action": deal_action
        }
        return JsonResponse(data)

class ProductCreateView(CreateView):
    template_name = "business/create/product.html"

    def form_valid(self, form):
        form.instance.deal = Deal.objects.get(pk=self.kwargs.get('deal_pk'))
        form.instance.type = self.model.__name__.lower()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('deal_detail', kwargs={'pk': self.object.deal.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.model.__name__
        context["deal_pk"] = self.kwargs.get("deal_pk")
        return context

class create_magazine_product(ProductCreateView):
    model = Magazine
    fields = [ "value", "discount", "notes", "size", "placement", "issue", "image", "is_color"]

class create_website_product(ProductCreateView):
    model = Website
    fields = [ "value", "discount", "notes", "media"]

class create_newsletter_product(ProductCreateView):
    model = Newsletter
    fields = [ "value", "discount", "notes", "months", "size"]

class create_flag_product(ProductCreateView):
    model = Flag
    fields = [ "value", "discount", "notes", "image", "months"]

class create_event_product(ProductCreateView):
    model = Event
    fields = [ "value", "notes"]

class create_popup_product(ProductCreateView):
    model = Popup
    fields = [ "value", "discount", "notes", "date", "duration"]
    
class create_other_product(ProductCreateView):
    model = Other
    fields = [ "value", "notes"]

class ProductUpdateView(UpdateView):
    template_name = "business/product-detail.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.deal.created_by == request.user or request.user.account_type=="staff" or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You do not have business staff access or own this product')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action=="Delete":
            obj = self.get_object()
            obj.delete()
            messages.success(request, "{} has been deleted".format(obj))
            return redirect(reverse('deal_detail', kwargs={'pk': obj.deal.pk}))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('deal_detail', kwargs={'pk': self.object.deal.pk})

class magazine_product(ProductUpdateView):
    model = Magazine
    fields = [ "value", "discount", "notes", "size", "placement", "issue", "image", "is_color"]

class website_product(ProductUpdateView):
    model = Website
    fields = [ "value", "discount", "notes", "media"]

class newsletter_product(ProductUpdateView):
    model = Newsletter
    fields = [ "value", "discount", "notes", "months", "size"]

class flag_product(ProductUpdateView):
    model = Flag
    fields = [ "value", "discount", "notes", "image", "months"]

class event_product(ProductUpdateView):
    model = Event
    fields = [ "value", "notes"]

class popup_product(ProductUpdateView):
    model = Popup
    fields = [ "value", "discount", "notes", "date", "duration"]

class other_product(ProductUpdateView):
    model = Other
    fields = [ "value", "notes"]

def deals(request):
    pass

@method_decorator([login_required, business_required], name="dispatch")
class companies(ListView):
    paginate_by = 25
    model = Company
    template_name = "business/companies.html"

    def get_queryset(self):
        filter_qs = self.request.GET.get("filter", "")
        context = super().get_queryset().filter(
        Q(name__icontains=filter_qs)|
        Q(contact_name__icontains=filter_qs)|
        Q(contact_email__icontains=filter_qs)
        ).order_by("-created_at")
        return context
    
    def post(self, request, *args, **kwargs):
        object = self.model.objects.create(
            name=request.POST.get("name"),
            contact_name=request.POST.get("contact_name"),
            contact_email=request.POST.get("contact_email"),
            billing_address=request.POST.get("billing_address"),
            city_state_zip=request.POST.get("city_state_zip"),
            added_by=request.user
        )
        return redirect(reverse("company_detail", kwargs={"pk": object.pk}))

class company_detail(UpdateView):
    model = Company
    fields = "__all__"
    template_name = "business/company-detail.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.added_by == request.user or request.user.account_type=="staff" or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'You do not have business staff access or did not add this company')
        return redirect("login")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action=="Delete":
            obj = self.get_object()
            obj.delete()
            messages.success(request, "{} has been deleted".format(obj.name))
            return redirect(reverse("companies"))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('company_detail', kwargs={'pk': self.object.pk})


def ads(request):
    pass

def ad_detail(request):
    pass