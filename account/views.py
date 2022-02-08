from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserSettingsForm
from django.contrib import messages

@login_required
def account_settings(request):
    user = request.user
    if request.method=="POST":
        form = UserSettingsForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("account_settings")
    else:
        form = UserSettingsForm(instance=user)
    context = {
        "account": user,
        "form": form
    }
    return render(request, "account_settings.html", context)