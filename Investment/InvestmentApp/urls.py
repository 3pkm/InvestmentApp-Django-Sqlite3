from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root URL redirects to login
    path('', auth_views.LoginView.as_view(template_name='Investment/login.html'), name='login'),
    
    # Authentication views
    path('login/', auth_views.LoginView.as_view(template_name='Investment/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='Investment/password_reset_form.html',
        email_template_name='Investment/password_reset_email.html',
        subject_template_name='Investment/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='Investment/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='Investment/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='Investment/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Dashboard views
    path('home/', views.index, name='home'),
    path('products/', views.products_view, name='products'),
    path('investments/', views.investments_view, name='investments'),
    path('monthly_calculator/', views.monthly_investment_calculator, name='monthly_calculator'),
    path('one_time_calculator/', views.one_time_investment_calculator, name='one_time_calculator'),

    # AJAX and data modification views
    path('add_investment/', views.add_investment, name='add_investment'),
    path('delete_investment/<int:investment_id>/', views.delete_investment, name='delete_investment'),
    path('update_investment/<int:investment_id>/', views.update_investment, name='update_investment'),
]
