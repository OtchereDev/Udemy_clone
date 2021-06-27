from courses.views import CourseManage, CoursesHomeViews,CourseManageCourseList
from django.urls import path


app_name='courses'

urlpatterns = [
    path('',CoursesHomeViews.as_view(),),
    path('course_management/',CourseManageCourseList.as_view()),
    path('course_management/<str:course_uuid>/',CourseManage.as_view()),
]
