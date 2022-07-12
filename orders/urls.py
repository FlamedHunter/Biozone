from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('review_order/<order_number>/', views.review_order, name='review_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
]


