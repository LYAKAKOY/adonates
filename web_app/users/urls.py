import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.greet, name='greet_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
