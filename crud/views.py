from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import io
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from rest_framework.renderers import json
from .models import Student
from django.http import HttpResponse, JsonResponse

# Create your views here.
@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            try:
                stu = Student.objects.get(id=id)
                serializer = StudentSerializer(stu)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            except Student.DoesNotExist:
                res = {'msg': 'Student not found'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')

        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')
    
    elif request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        try:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu, data=pythondata, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'Data Updated now'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')
        except Student.DoesNotExist:
            res = {'msg': 'Student not found'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
    
    elif request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        try:
            stu = Student.objects.get(id=id)
            stu.delete()
            res = {'msg': 'Data Deleted'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        except Student.DoesNotExist:
            res = {'msg': 'Student not found'}
            # json_data = JSONRenderer().render(res)
            # return HttpResponse(json_data, content_type='application/json')
            return JsonResponse(res, safe=False)