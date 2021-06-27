from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from courses.serializers import CoursePaidSerializer, CourseUnPaidSerializer, SectorSerializer
from courses.models import Course, Sector
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

class CoursesHomeViews(APIView):
    def get(self,request,*args, **kwargs):
        sector=Sector.object.all()
        serializer=SectorSerializer(sector,many=True)
        
        return Response(data=serializer.data,status=status.HTTP_200_OK)


class CourseCreateView(APIView):

    def post(self,request,*args, **kwargs):
        serializer=CoursePaidSerializer(request.data)

        if serializer.is_valid():
            print(serializer.validated_data)
            obj=serializer.save(author=request.user)
            print(obj)

            return Response(obj,status=status.HTTP_201_CREATED)
        else:

            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    
class CourseSearch(APIView):
    def get(self,request,sector_uuid,*args, **kwargs):
        sector=Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest("Course sector does not exist")

        sector_courses=sector.objects.all()

        serializer=CourseUnPaidSerializer(sector_courses,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


class CourseDetail(APIView):
    def get(self,request,course_uuid,*args, **kwargs):
        
        course=Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest('Course does not exist')

        serializer=CourseUnPaidSerializer(course[0])

        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)

        return HttpResponseBadRequest('Course does not exist')


class CourseStudy(APIView):
    def get(self,request,course_uuid,test=None):
        check_course=Course.objects.filter(course_uuid=course_uuid)

        if check_course:
            return HttpResponseBadRequest('Course does not exist')

        user_course=request.user.paid_course.objects.filter(course_uuid=course_uuid)

        if user_course:
            return HttpResponseNotAllowed("User has not purchased this course")

        course=Course.objects.filter(course_uuid=course_uuid)[0]

        serializer=CoursePaidSerializer(course[0])
        
        if serializer.is_valid():
            return Response(serializer.validated_data,status=status.HTTP_200_OK)


        return HttpResponseBadRequest()


class CourseManageCourseList(APIView):
    def get(self,request,*args, **kwargs):
        courses=Course.objects.filter(author=request.user)
        serializer=CoursePaidSerializer(courses,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)


class CourseManage(APIView):

    def patch(self,request,course_uuid,*args, **kwargs):
        course=Course.objects.filter(course_uuid=course_uuid,author=request.user)

        if not course:
            return HttpResponseBadRequest()

        serializer=CoursePaidSerializer(request.data,instance=course[0])

        if serializer.is_valid():
            data=serializer.save()
        
        return Response(data=data,status=status.HTTP_201_CREATED)


    def delete(self,request,course_uuid,*args, **kwargs):

        course=Course.objects.filter(course_uuid=course_uuid,author=request.user)

        if not course:
            return HttpResponseBadRequest()

        course[0].delete()

        return Response(data={
            "status":"successfull",
            "course":course[0]
        },status=status.HTTP_204_NO_CONTENT)

