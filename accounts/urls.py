from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Existing views
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # New views
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('about/', views.about_view, name='about'),
    path('settings/', views.settings_view, name='settings'),
    path('farmer-page/', views.farmer_page_view, name='farmer_page'),
    path('success/', views.success_page, name='success_page'),
path('view_product/<int:product_id>/', views.view_product, name='view_product'),
]
