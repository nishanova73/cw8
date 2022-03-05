from django.urls import path

from accounts.views import login_view, logout_view, register_view, UserDetailView, UserChangeView, \
    UserChangePasswordView, AllUsers

app_name = 'accounts'


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('profile/<int:pk>/edit/', UserChangeView.as_view(), name='user_update'),
    path('profile/<int:pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('progile/all/', AllUsers.as_view(), name='all_users')
]