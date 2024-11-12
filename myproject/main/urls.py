from django.urls import path
from .views import OrderList, CostList

urlpatterns = [
    path('order_list/', OrderList.as_view(), name='order_list'),
    path('cost_list/', CostList.as_view(), name='cost_list'),
]
