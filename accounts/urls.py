
from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns= [
	path('signup/', views.signUpUser, name='signup'),
	path('login/', views.loginUser, name='login'),
	path('logout/', views.logoutUser, name='logout'),

    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url='/accounts/password_change_done'
        ), name='password_change'),

	#path('password_change/', PasswordChangeView.as_view( success_url='accounts/password_change/done/'), name="password_change"),
	path('password_change_done/', PasswordChangeDoneView.as_view(), name="password_change_done"),


	path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             #subject_template_name='accounts/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

