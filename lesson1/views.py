import json
from django.forms import model_to_dict
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lesson1.models import Course

from lesson1.serializers import CourseSerializer


@api_view(['GET'])  # initializing request method
def get_all_courses(request):
    courses = Course.objects.all()  # get all data
    data = CourseSerializer(courses, many=True).data  # serialization
    return Response(data=data)


@api_view(['GET'])  # initializing request method
def get_course(request, id):
    try:
        courses = Course.objects.get(id=id)  # get by id
    except Course.DoesNotExist:
        return Response(data={'result': 'item not found'}
                        , status=status.HTTP_404_NOT_FOUND)
    data = CourseSerializer(courses).data  # serialization
    return Response(data=data, status=status.HTTP_200_OK)


def get_all_course(request):
    courses = []
    for i in Course.objects.all():
        courses.append(model_to_dict(i))
    json_data = json.dumps(courses)
    return HttpResponse(json_data)
