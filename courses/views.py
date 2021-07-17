from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from courses.serializers import CartItemSerializer, CommentSerializer, CourseDisplaySerializer, CourseListSerializer, CoursePaidSerializer, CourseUnPaidSerializer, SectorSerializer
from courses.models import Course, Sector

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from decimal import Decimal
import json


class CoursesHomeViews(APIView):
    def get(self,request,*args, **kwargs):
        sectors=Sector.objects.order_by('?')[:6]

        sector_response=[]

        for sector in sectors:
            sector_courses=sector.related_courses.order_by('?')[:4]
            courses_serializer=CourseDisplaySerializer(sector_courses,many=True)
            sector_obj={
                "sector_name": sector.name,
                "sector_uuid": sector.sector_uuid,
                "featured_courses": courses_serializer.data,
                "sector_image":sector.sector_image.url
            }
            sector_response.append(sector_obj)

        # serializer=SectorSerializer(sectors=sector_response,many=True)
        
        return Response(data=sector_response,status=status.HTTP_200_OK)


# not used yet
class CourseCreateView(APIView):
    permission_classes=[IsAuthenticated]
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

        sector_courses=sector[0].related_courses.all()

        serializer=CourseListSerializer(sector_courses,many=True)

        total_students=0

        for course in sector_courses:
            total_students+=course.get_enrolled_students()

        

        return Response({'data':serializer.data,
                        'sector_name':sector[0].name,
                        'total_students':total_students,
                        'image':sector[0].sector_image.url},
                        status=status.HTTP_200_OK)


class CourseDetail(APIView):
    def get(self,request,course_uuid,*args, **kwargs):
        try:
            
            course=Course.objects.filter(course_uuid=course_uuid)
        except ValidationError:
            return HttpResponseBadRequest('Invalid Course uuid')
        
        if not course:
            return HttpResponseBadRequest('Course does not exist')
        
        serializer=CourseUnPaidSerializer(course[0])
        
        
        return Response(serializer.data,status=status.HTTP_200_OK)

        


class CourseStudy(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,course_uuid):
        check_course=Course.objects.filter(course_uuid=course_uuid)

        if not check_course:
            
            return HttpResponseBadRequest('Course does not exist')

        user_course=request.user.paid_course.filter(course_uuid=course_uuid)
        

        if not user_course:
            
            return HttpResponseNotAllowed("User has not purchased this course")

        course=Course.objects.filter(course_uuid=course_uuid)[0]

        serializer=CoursePaidSerializer(course)
        
        
        
        return Response(serializer.data,status=status.HTTP_200_OK)


# not used yet
class CourseManageCourseList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args, **kwargs):
        courses=Course.objects.filter(author=request.user)
        serializer=CoursePaidSerializer(courses,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)


# not used yet
class CourseManage(APIView):
    permission_classes=[IsAuthenticated]

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


class GetCartDetail(APIView):
    def post(self,request,*args, **kwargs):

        try:
            body =  json.loads(request.body)
        
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()

        if type(body.get('cart')) != list:
            return HttpResponseBadRequest()


        if len(body.get("cart")) ==0:
            return Response(data=[])

        courses=[]

        for uuid in body.get("cart"):
            item = Course.objects.filter(course_uuid=uuid)

            if not item:
                return HttpResponseBadRequest()
            
            courses.append(item[0])

            # serializer for cart
        serializer =CartItemSerializer(courses,many=True)

        # TODO : After you have added the price field
        cart_cost=Decimal(0.00)

        for item in serializer.data:
           
            cart_cost+=Decimal(item.get("price"))


        return Response(data={"cart_detail":serializer.data,"cart_total":str(cart_cost)})


    
class SearchCourse(APIView):

    def get(self,request,search_term):
        matches= Course.objects.filter(Q(title__icontains=search_term)|
            Q(description__icontains=search_term))

        serializer=CourseListSerializer(matches,many=True)

        return Response(data=serializer.data)



class AddComment(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,course_uuid,*args, **kwargs):
        try:
            course=Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        content=json.loads(request.body)

        if not content.get('message'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=content)

        if serializer.is_valid():
            comment=serializer.save(user=request.user)

            course.comment.add(comment)

            return Response(status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

