from rest_framework import serializers
from .models import Class, Instructor


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'Instructor_name']


class ClassSerializer(serializers.ModelSerializer):
    instructors = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'time', 'available_slots', 'instructors']

    def get_instructors(self, obj):
        instructors = Instructor.objects.filter(class_assigned=obj)
        return InstructorSerializer(instructors, many=True).data
