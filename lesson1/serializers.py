from rest_framework import serializers

from lesson1.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = 'id name age'.split()


class CourseSerializer(serializers.ModelSerializer):
    # students = StudentSerializer(many=True)
    students = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = 'id name students count'.split()

    def get_count(self, obj):
        return Student.objects.filter(course=obj).count()

    def get_students(self, obj):
        students = Student.objects.filter(course=obj, age__gt=30)
        return StudentSerializer(students, many=True).data
