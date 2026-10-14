from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import TemplateView
from tattoo.models import Student
from typing import Any

# Create your views here.
class ShowStudentView(TemplateView):
    template_name = "tattoostudio/show_students.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()

        return context
        