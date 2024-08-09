from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chat.views import CreateUserView, LoginUserView,FindLocationAPIByNumberView,FindLocationAPIByEMEIView,FindLocationAPIByGoogleView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup', CreateUserView.as_view(), name='signup'),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/find-location/', FindLocationAPIByNumberView.as_view(), name='find-location'),
    path('api/findByEMEI/', FindLocationAPIByEMEIView.as_view(), name='find-location'),
    path('api/findByGoogle/', FindLocationAPIByGoogleView.as_view(), name='find-location'),
]
