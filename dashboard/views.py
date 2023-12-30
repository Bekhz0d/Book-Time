from django.shortcuts import render
from django.views.generic import View


class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard/index3.html')
    