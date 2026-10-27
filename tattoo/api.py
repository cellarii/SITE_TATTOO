from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from tattoo.models import Profile
from tattoo.models import Service
from tattoo.models import Appointment
from tattoo.models import Review
from tattoo.models import Portfolio

from tattoo.serializers import ServiceSerializer, PortfolioSerializer, ReviewSerializer, AppointmentSerializer

class ServiceViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
    ):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class PortfolioViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
    ):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class ReviewViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
    ):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class AppointmentViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
    ):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer