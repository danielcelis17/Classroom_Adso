from django.contrib import admin
from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cliente', Cliente_APIView.as_view()),
]
