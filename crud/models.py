from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    city = models.CharField(max_length=100)

def create(self, validated_data):
    return Student.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.name = validated_data.get('name', instance.name)
    instance.roll = validated_data.get('roll', instance.roll)
    instance.city = validated_data.get('city', instance.city)
    instance.save()
    return instance
    