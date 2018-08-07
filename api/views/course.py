from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api import models
from api import serializer
# Create your views here.


class DegreeCourseTeacherView(APIView):
    '''
    查询所有学位课和老师
    '''
    def get(self,request,*args,**kwargs):
        res = {'code':1000,'data':None}
        try:
            degree_course_list = models.DegreeCourse.objects.all()  # 数据库取数据
            ser_obj = serializer.DegreeCourseSTeachererializer(degree_course_list,many=True)  # serializer序列化数据
            res['data'] = ser_obj.data  # 取出序列化后的数据
        except Exception as e:
            res['code'] = 1001
            res['error'] = '获取数据失败'

        return Response(res)

class DegreeCourseScholarshipView(APIView):
    '''
    所有学位课和奖学金
    '''
    def get(self,request,*args,**kwargs):
        res = {'code':1000,'data':None}
        try:
            degree_course_list = models.DegreeCourse.objects.all()
            ser_obj = serializer.DegreeCourseScholarshipSerializer(degree_course_list, many=True)
            res['data'] = ser_obj.data
        except Exception as e:
            res['code'] = 1001
            res['error'] = '获取数据失败'
        return Response(res)

class DegreeCourseDetailView(APIView):
    '''
    学位课id=1的所有模块名
    '''
    def get(self,request,pk,*args,**kwargs):
        res = {'code': 1000, 'data': None}
        try:
            Degree_obj = models.DegreeCourse.objects.filter(pk=pk).first()
            course_list = Degree_obj.course_set.all()
            ser_obj = serializer.DegreeCourIdseSerializer(course_list,many=True)
            res['data'] = ser_obj.data
        except Exception as e:
            res['code'] = 1001
            res['error'] = '获取数据失败'
        return Response(res)

class CourseView(APIView):
    '''
    展示所有专题课
    '''
    def get(self,request,*args,**kwargs):
        res={'code':1000,'data':None}
        try:
            course_list = models.Course.objects.filter(degree_course__isnull=True)
            ser_obj = serializer.CourseSerializer(course_list,many=True)
            res['data'] = ser_obj.data
            res['Access-Control-Allow-Origin'] = "*"
        except Exception as e:
            res['code'] = 1001
            res['error'] = '数据查询失败'

        return Response(res)

class CourseFirstView(APIView):
    '''
    专题课id=1的课程名、级别(中文)、why_study、、、
    '''
    def get(self,request,pk,*args,**kwargs):
        res = {'code': 1000, 'data': None}
        try:
            course_id = models.Course.objects.filter(pk=pk).first()
            ser_obj = serializer.CourseFirstSerializer(course_id)
            res['data'] = ser_obj.data
        except Exception as e:
            res['code'] = 1001
            res['error'] = '数据查询失败'
        return Response(res)

class CourseQuestionView(APIView):
    '''
    专题课id=1的所有常见问题
    '''
    def get(self,request,*args,**kwargs):
        res = {'code': 1000, 'data': None}
        try:
            course_id = models.Course.objects.filter(pk=1).first()
            ser_obj = serializer.CourseQuestionSerializer(course_id)
            res['data'] = ser_obj.data
        except Exception as e:
            res['code'] = 1001
            res['error'] = '数据查询失败'
        return Response(res)

class CourseOutlineView(APIView):
    '''
    专题课id=1所有课程大纲
    '''
    def get(self,request,*args,**kwargs):
        res = {'code': 1000, 'data': None}
        try:
            course_obj = models.Course.objects.filter(pk=1)
            ser_obj = serializer.CourseOutlineSerializer(course_obj,many=True)
            res['data'] = ser_obj.data
        except Exception as e:
            res['code'] = 1001
            res['error'] = '数据查询失败'
        return Response(res)

class CourseChapterView(APIView):
    '''
    专题课id=1所有章节
    '''
    def get(self,request,*args,**kwargs):
        res = {'code': 1000, 'data': None}
        course_obj = models.Course.objects.filter(pk=1)
        ser_obj = serializer.CourseChapterSerializer(course_obj,many=True)
        res['data'] = ser_obj.data
        return Response(res)