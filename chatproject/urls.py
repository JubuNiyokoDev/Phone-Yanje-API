from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chat.views import CreateUserView, LoginUserView,FindLocationAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup', CreateUserView.as_view(), name='signup'),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/find-location/', FindLocationAPIView.as_view(), name='find-location'),
]
