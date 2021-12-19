from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(LoginRequiredMixin, View):
    template_name = "index.html"

    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)
