from courses.views import CoursesViews
from django.urls import path


app_name='courses'

urlpatterns = [
    path('',CoursesViews.as_view(),)
]
