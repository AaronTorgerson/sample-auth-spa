from django.urls import path

from api.views import get_stocks

urlpatterns = [
    path('stocks', get_stocks),
]
