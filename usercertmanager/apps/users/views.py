from django.shortcuts import render
from django.views.generic import TemplateView


class LoginButtonView(TemplateView):
    template_name = "auth/begin_login.html"
