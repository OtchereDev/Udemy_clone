from courses.views import AddComment, CourseDetail, CourseManage, CourseSearch, CourseStudy, CoursesHomeViews,CourseManageCourseList, GetCartDetail, SearchCourse
from django.urls import path


app_name='courses'

urlpatterns = [
    
    path('cart/',GetCartDetail.as_view()),
    path('detail/<uuid:course_uuid>/',CourseDetail.as_view()),
    path("search/<str:search_term>/",SearchCourse.as_view()),
    path("study/<uuid:course_uuid>/",CourseStudy.as_view()),
    path('comment/<uuid:course_uuid>/',AddComment.as_view()),
    path('course_management/',CourseManageCourseList.as_view()),
    path('course_management/<uuid:course_uuid>/',CourseManage.as_view()),
    path('',CoursesHomeViews.as_view(),),
    path('<uuid:sector_uuid>/',CourseSearch.as_view()),
]
