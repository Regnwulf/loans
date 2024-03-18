from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('api/', include('api.urls')),
    path('api/token/', ObtainAuthToken.as_view(), name='token_obtain'),
]
