from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views.generic import UpdateView, ListView
from business.models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from portal.decorators import *
from django.db.models import Q

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
    template_name = "business/issue_detail.html"


def deals(request):
    pass

def deal_detail(request):
    pass

def companies(request):
    pass

def company_detail(request):
    pass

def ads(request):
    pass

def ad_detail(request):
    pass