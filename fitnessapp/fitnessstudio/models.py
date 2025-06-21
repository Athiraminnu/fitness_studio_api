from django.db import models


#db table 'Class' for  class details
class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)
    time = models.TimeField()
    available_slots = models.IntegerField()


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "classes"


#db table 'Instructor' for instructor details
class Instructor(models.Model):
    Instructor_name = models.CharField(max_length=100)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Instructor_name}"


#db table 'Bookings' for booking details
class Bookings(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=250)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)