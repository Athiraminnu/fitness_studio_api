from rest_framework import serializers
from .models import Class, Instructor, Bookings


class BookingsSerializer(serializers.ModelSerializer): #serializer for the Booking model
    class Meta:
        model = Bookings
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer): #serializer for the Instructor model
    class Meta:
        model = Instructor
        fields = ['id', 'Instructor_name']


class ClassSerializer(serializers.ModelSerializer): #serializer for the Class model
    instructors = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'name', 'time', 'available_slots', 'instructors']

    def get_instructors(self, obj):
        instructors = Instructor.objects.filter(class_assigned=obj)
        return InstructorSerializer(instructors, many=True).data
