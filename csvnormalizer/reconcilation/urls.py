from django.urls import path

from .views import CSVReconciliationView

urlpatterns = [
    path("", CSVReconciliationView.as_view(), name="csv-reconciliation"),
]
