from django.urls import path
from .views import AdminLoginView

urlpatterns = [
    path('auth', AdminLoginView.as_view(), name='admin_login'),
]
