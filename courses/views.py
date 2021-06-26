from courses.serializers import CoursePaidSerializer, CourseUnPaidSerializer
from courses.models import Course
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class CoursesViews(APIView):
    def get(self,request,*args, **kwargs):
        courses=Course.objects.all()
        serializer=CourseUnPaidSerializer(courses,many=True)

        return Response(data=serializer.data,status=200)



    def post(self,request,*args, **kwargs):
        serializer=CoursePaidSerializer(request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            obj=serializer.save(author=request.user)
            print(obj)

            return Response(obj,status=201)
        else:

            return Response(data=serializer.errors,status=400)
            
    
