from django.http import HttpResponseServerError
from django.views import View
from django.shortcuts import render
from bangazonapi.models import Order

class PaidOrdersReportView(View):
    def get(self, request):
        status = request.GET.get('status')
        if status == 'complete':
            orders = Order.objects.filter(payment_type__isnull=False,)
            context = {
                'orders': orders,
            }
            return render(request, 'reports/paid_orders.html', context)
        else:
            return HttpResponseServerError("Invalid status parameter")