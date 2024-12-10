from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('about/', views.about_view, name='about'),
    path('settings/', views.settings_view, name='settings'),
    path('farmer-page/', views.farmer_page_view, name='farmer_page'),
    path('success/', views.success_page, name='success_page'),
    path('upload_success/', views.upload_success, name='upload_success'),
    path('contact/', views.contact_view, name='contact'),
    path('add-photo/', views.add_photo, name='add_photo'),
    path('profile/success/', views.profile_success, name='profile_success'),
    path('farmer_message/', views.farmer_detail, name='farmer_detail'),

]
