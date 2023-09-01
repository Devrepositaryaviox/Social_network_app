from django.urls import path
from user_post import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register-user/', views.RegisterUserAPIView.as_view()),
    path('post-create-list/', views.PostListCreateAPIView.as_view()),
    path('post/<int:pk>/', views.PostRetrieveUpdateDeleteAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]