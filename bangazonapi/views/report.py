from django.http import HttpResponseServerError
from django.views import View
from django.shortcuts import render
from ..models import Order, Customer, Payment

class PaidOrdersReportView(View):
    def get(self, request):
        status = request.GET.get('status')
        if status == 'complete':
            orders = Order.objects.filter(status='paid').select_related('customer', 'payment')
            context = {
                'orders': orders,
            }
            return render(request, 'templates/reports/paid_orders.html', context)
        else:
            return HttpResponseServerError("Invalid status parameter")