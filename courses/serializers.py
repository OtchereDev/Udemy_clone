from rest_framework import serializers
from users.serializers import UserSerializer
from courses.models import Comment, Course, CourseSection, Episode, Sector
from rest_framework.serializers import ModelSerializer

class EpisodePaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    file=serializers.CharField(source='get_absolute_url')
    class Meta:
        model=Episode
        fields=[
            "title",
            "file",
            "length",
        ]

class CourseSectionPaidSerializer(ModelSerializer):
    episodes=EpisodePaidSerializer(many=True)
    total_duduration=serializers.CharField(source='total_length')
    class Meta:
        model=CourseSection
        fields=[
            "section_title",
            "section_number",
            "episodes",
            "total_duduration"
        ]

class EpisodeUnPaidSerializer(ModelSerializer):
    length=serializers.CharField(source='get_video_length_time')
    
    
    class Meta:
        model=Episode
        fields=[
            "title",
            "length",
            'id',
            
        ]

class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes=EpisodeUnPaidSerializer(many=True)
    total_duration=serializers.CharField(source='total_length')
    
    class Meta:
        model=CourseSection
        fields=[
            "section_title",
            "section_number",
            "episodes",
            "total_duration"
        ]

class CommentSerializer(ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=[
            'user',
            'message',
            'created',
            'id'
        ]

class CourseUnPaidSerializer(ModelSerializer):

    comment=CommentSerializer(many=True)
    author=UserSerializer()
    course_sections=CourseSectionUnPaidSerializer(many=True)
    student_rating=serializers.IntegerField(source='get_rating')
    student_rating_no=serializers.IntegerField(source='get_no_rating')
    student_no=serializers.IntegerField(source='get_enrolled_students')
    total_lectures=serializers.IntegerField(source="get_total_lectures")
    total_duration=serializers.CharField(source='total_course_length')
    class Meta:
        model=Course
        exclude=[
            'rating',
            
        ]

class CoursePaidSerializer(ModelSerializer):
    
    comment=CommentSerializer(many=True)
    author=UserSerializer()
    course_sections=CourseSectionPaidSerializer(many=True)
    student_rating=serializers.IntegerField(source='get_rating')
    student_rating_no=serializers.IntegerField(source='get_no_rating')
    student_no=serializers.IntegerField(source='get_enrolled_students')
    total_lectures=serializers.IntegerField(source="get_total_lectures")
    total_duration=serializers.CharField(source='total_course_length')
    class Meta:
        model=Course
        exclude=[
            'rating',
           
        ]

class SectorSerializer(ModelSerializer):
    class Meta:
        model=Sector
        exclude=[
            'related_courses',
        ]

class CourseDisplaySerializer(ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    student_no=serializers.IntegerField(source='get_enrolled_students')
    author=UserSerializer()
    class Meta:
        model=Course
        fields=['course_uuid',"title",'rating','student_no',"author","price","image_url"]


class CartItemSerializer(ModelSerializer):
    author=UserSerializer()
    class Meta:
        model=Course
        # add price later,image url
        fields=['course_uuid','title',"author","price","image_url"]

class CourseListSerializer(ModelSerializer):
    rating=serializers.IntegerField(source='get_rating')
    student_no=serializers.IntegerField(source='get_enrolled_students')
    author=UserSerializer()
    description=serializers.CharField(source='get_brief_description')
    total_lectures=serializers.IntegerField(source="get_total_lectures")
    class Meta:
        model=Course
        fields=['course_uuid',"title",'rating','student_no',"author","price","image_url",'description','total_lectures']

        