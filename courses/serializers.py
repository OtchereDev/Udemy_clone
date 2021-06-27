from users.serializers import UserSerializer
from courses.models import Comment, Course, CourseSection, Episode, Sector
from rest_framework.serializers import ModelSerializer

class EpisodePaidSerializer(ModelSerializer):
    class Meta:
        model=Episode
        fields=[
            "title",
            "file",
            "length",
        ]

class CourseSectionPaidSerializer(ModelSerializer):
    episodes=EpisodePaidSerializer(many=True)
    class Meta:
        model=CourseSection
        fields=[
            "section_title",
            "section_number",
            "episodes",
        ]

class EpisodeUnPaidSerializer(ModelSerializer):
    class Meta:
        model=Episode
        fields=[
            "title",
            "length",
        ]

class CourseSectionUnPaidSerializer(ModelSerializer):
    episodes=EpisodeUnPaidSerializer(many=True)
    class Meta:
        model=CourseSection
        fields=[
            "section_title",
            "section_number",
            "episodes",
        ]

class CommentSerializer(ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Comment
        fields=[
            'user',
            'message',
            'created'
        ]

class CourseUnPaidSerializer(ModelSerializer):

    comment=CommentSerializer(many=True)
    author=UserSerializer()
    course_sections=CourseSectionUnPaidSerializer(many=True)
    class Meta:
        model=Course
        exclude=[
            'rating',
            
        ]

class CoursePaidSerializer(ModelSerializer):
    
    comment=CommentSerializer(many=True)
    author=UserSerializer()
    course_sections=CourseSectionPaidSerializer(many=True)
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