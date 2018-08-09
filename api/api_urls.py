# !/usr/bin/env python
# -*-coding:utf-8 -*-

from django.conf.urls import url
from api.views import course
from api.views import shoppingcar

urlpatterns = [
    url(r'^degreeTeacher/$',course.DegreeCourseTeacherView.as_view()),  # all学位课与老师
    url(r'^degreeScholarship/$',course.DegreeCourseScholarshipView.as_view()),  # all学位课与奖金
    url(r'^degreecourses/(?P<pk>\d+)/$',course.DegreeCourseDetailView.as_view()),  #id=1的学位课模块
    url(r'^courses/$',course.CourseView.as_view()),  # all专题课
    url(r'^courses/(?P<pk>\d+)/$',course.CourseFirstView.as_view()),  # id=1专题课的级别，why_study,,
    url(r'^courseQuestion/$',course.CourseQuestionView.as_view()),  # id=1专题课 all常见问题
    url(r'^courseCourseOutline/$',course.CourseOutlineView.as_view()),  # id=1专题课 all课程大纲
    url(r'^courseChapter/$',course.CourseChapterView.as_view()),  # id=1专题课 all 章节


    url(r'^shoppingcar/$',shoppingcar.ShoppingCarView.as_view({'get':'list','post':'create','put':'update','delete':'destroy'})),
    # url(r'^shoppingcar/(?P<pk>\d+)$',shoppingcar.ShoppingCarView.as_view({})),



]
