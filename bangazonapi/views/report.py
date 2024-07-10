from django.http import HttpResponseServerError
from django.views import View
from django.shortcuts import render
from django.db.models import Sum, F
from bangazonapi.models import Order, OrderProduct, Product

class PaidOrdersReportView(View):
    def get(self, request):
        status = request.GET.get('status')
        if status == 'complete':
            orders = Order.objects.filter(payment_type__isnull=False,).select_related('customer', 'payment_type')

            order_data = []
            for order in orders:
                total_paid = OrderProduct.objects.filter(order=order).aggregate(
                    total=Sum(F('product__price'))
                )['total'] or 0
                order_data.append({
                    'id': order.id,
                    'customer_name': f"{order.customer.user.first_name} {order.customer.user.last_name}",
                    'payment_type_merchant': order.payment_type.merchant_name,
                    'total_paid': total_paid
                })

            context = {
                'orders': order_data,
            }
            return render(request, 'reports/paid_orders.html', context)
        else:
            return HttpResponseServerError("Invalid status parameter")