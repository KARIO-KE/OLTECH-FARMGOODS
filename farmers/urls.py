from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'farmers'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('view_product/<int:product_id>/', views.view_product, name='view_product'),
    path('farmer_page/', views.farmer_home, name='farmer_page'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('edit_product/', views.edit_product, name='edit_product'),
]
