from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('sendotp/', views.sendotp, name='sendotp'),
    path('otplogin/', views.otplogin, name='otplogin'),

    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('orders/', views.orders, name='orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('manage_order/<product>/', views.manage_order, name='manage_order'),
    path('add_instrument/', views.add_instrument, name='add_instrument'),
]


