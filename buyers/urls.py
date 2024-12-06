from django.urls import path
from . import views

app_name = 'buyers'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
       path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('logout/', views.logout_view, name='logout'),
]
