from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from tattoo.models import Student
from tattoo.serializers import StudentSerializer
from tattoo.serializers import GroupSerializer

class StudentsViewset(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer