from django.urls import path
from .views import create_polling_unit

urlpatterns = [
    path('polling-unit/create/', create_polling_unit, name='create_polling_unit'),
    # Other URL patterns...
]
