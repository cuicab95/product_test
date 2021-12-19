from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class IndexView(LoginRequiredMixin, View):
    template_name = "index.html"

    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)


class OrderDetailView(LoginRequiredMixin, View):
    template_name = "order_detail.html"

    def get(self, request, order_id):
        ctx = {'order_id': order_id}
        return render(request, self.template_name, ctx)
