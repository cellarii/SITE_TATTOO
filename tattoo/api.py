from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from tattoo.models import Student
from tattoo.models import Profile
from tattoo.models import Service
from tattoo.models import Appointment
from tattoo.models import Review
from tattoo.models import Portfolio


from tattoo.serializers import StudentSerializer
from tattoo.serializers import GroupSerializer

class StudentsViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class Profile(mixins.ListModelMixin, GenericViewSet):
    queryset = Profile.objects.all()