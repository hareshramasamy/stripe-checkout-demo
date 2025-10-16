from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, create_checkout_session, checkout_success, checkout_cancel

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointments")

urlpatterns = [
    path("", include(router.urls)),
    path("checkout-session/", create_checkout_session, name="create_checkout_session"),
    path("success/", checkout_success, name="checkout_success"),
    path("cancel/", checkout_cancel, name="checkout_cancel"),
]