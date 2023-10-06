from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'register', views.RegisterView, basename='register')
router.register(r'login', views.LoginView, basename='login')
# router.register(r'<int:pk>/', views.RegisterView, basename='register')
router.register(r'single_blog', views.SingleBlogView, basename='single_blog')

urlpatterns = [
    path('', include(router.urls))
]
