# Create your views here.
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import stripe

from .models import Appointment
from .serializers import AppointmentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by("-id")
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]

@api_view(["POST"])
@permission_classes([AllowAny])
def create_checkout_session(request):
    appt_id = request.data.get("appointment_id")
    if not appt_id:
        return Response({"error": "appointment_id is required"}, status=400)

    appt = get_object_or_404(Appointment, pk=appt_id)
    amount_cents = int(request.data.get("amount_cents", 2000))  # default $20

    success_url = request.build_absolute_uri(reverse("checkout_success"))
    cancel_url = request.build_absolute_uri(reverse("checkout_cancel"))

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": amount_cents,
                "product_data": {"name": f"Appointment with {appt.provider_name}"},
            },
            "quantity": 1,
        }],
        customer_email=appt.client_email,
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return Response({"checkout_url": session.url}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([AllowAny])
def checkout_success(_request):
    return Response({"status": "success"})

@api_view(["GET"])
@permission_classes([AllowAny])
def checkout_cancel(_request):
    return Response({"status": "canceled"})
