from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'farmers'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('upload_success/', views.upload_success, name='upload_success'),
    path('farmer_page/', views.farmer_home, name='farmer_page'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('edit/<int:pk>/', views.edit_message, name='edit_message'),  # Edit message
    path('delete/<int:pk>/', views.delete_message, name='delete_message'),
    path('upload_message/', views.upload_message, name='upload_message'),
    path('upload_message/success_page.html', views.success_message_view, name='success_message'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('farmer_products/', views.product_list, name='farmer_products'),
    path('farmers/message/<str:farmer_name>/', views.message_detail, name='message_detail'),
]
