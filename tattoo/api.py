from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tattoo.models import Profile, Service, Appointment, Review, Portfolio
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate

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

class ProfileViewSet(GenericViewSet):
    queryset = Profile.objects.all()

    @action(detail=False, url_path='me', methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data = {
            'is_authenticated':self.request.user.is_authenticated
        }

        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "role": self.request.user.profile.role
            })


        return Response(data = data)

    @action(detail=False, url_path='logout', methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)

        return Response()

    @action(detail=False, url_path="login", methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        success = False
        status_code = 403

        user = authenticate(username=username, password=password)
        if user:
            success= True
            status_code = 200
            django_login(self.request, user)

        return Response({
            'success': success
        }, status = status_code)

    # me данные текущего пользователя
    # login для авторизации
    # logout