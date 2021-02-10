from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('profile/', views.profile_view, name="profile"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('about/', views.about_view, name="about"),
    path('update_post/<int:pk>/', views.update_post, name="update_post"),
    path('delete_post/<int:pk>/', views.delete_post, name="delete_post"),
]
