# !/usr/bin/env python
# -*-coding:utf-8 -*-

from api import models
from rest_framework import serializers
from rest_framework.validators import ValidationError

class DegreeCourseSTeachererializer(serializers.ModelSerializer):
    '''
    查看所有学位课并打印学位课名称以及授课老师的序列化类
    '''
    # teachers=serializers.CharField(source='teachers.all')
    teachers=serializers.SerializerMethodField()  # 多对多字段通过定义一个方法，来取值

    class Meta:
        model = models.DegreeCourse
        fields = ['name','teachers']

    def get_teachers(self,row):  # 对应方法名：get_'SerializerMethodField()'的名
        teacher_list = row.teachers.all()  # 正向查询直接.字段.all()
        return [{'name':item.name,'id':item.id} for item in teacher_list]


class DegreeCourseScholarshipSerializer(serializers.ModelSerializer):
    '''
    所有学位课和奖学金
    '''
    scholarship = serializers.SerializerMethodField()
    # scholarship = serializers.CharField(source='scholarship.all')
    class Meta:
        model =models.DegreeCourse
        fields = ['name','scholarship']

    def get_scholarship(self,row):
        scholarship_list = row.scholarship_set.all()  # 反向查询表名小写_set.all()
        return [{'time_percent':item.time_percent,'value':item.value} for item in scholarship_list]

class DegreeCourIdseSerializer(serializers.ModelSerializer):
    '''
    学位课id=1的所有模块名
    '''
    class Meta:
        model = models.Course
        fields = ['id','name']

class CourseSerializer(serializers.ModelSerializer):
    '''
    展示所有专题课
    '''
    class Meta:
        model = models.Course
        fields = ['id','name']

class CourseFirstSerializer(serializers.ModelSerializer):
    '''
    专题课id=1的课程名、级别(中文)、why_study、、、
    '''
    # 枚举显示信息，定义CharField；用source='get_字段名_display()'
    level_name = serializers.CharField(source='get_level_display')
    # 一对一可以省去_set；表名小写.字段
    why_study = serializers.CharField(source='coursedetail.why_study')
    what_to_study_brief = serializers.CharField(source='coursedetail.what_to_study_brief')
    recommend_courses = serializers.SerializerMethodField()
    class Meta:
        model = models.Course
        fields = ['id','name','level_name','why_study','what_to_study_brief','recommend_courses']

    def get_recommend_courses(self,row):
        remomend_list = row.coursedetail.recommend_courses.all()
        return [{'id':item.id,'name':item.name} for item in remomend_list]

class CourseQuestionSerializer(serializers.ModelSerializer):
    '''
    专题课id=1的所有常见问题
    '''
    # questions = serializers.CharField(source='asked_question.all')
    questions = serializers.SerializerMethodField()
    class Meta:
        model = models.Course
        fields = ['questions']

    def get_questions(self,row):
        return [{'question': item.question, 'answer': item.answer} for item in row.asked_question.all()]

class CourseOutlineSerializer(serializers.ModelSerializer):
    '''
    专题课id=1所有课程大纲
    '''
    courseoutline = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['courseoutline']

    def get_courseoutline(self,row):
        courseoutlines = row.coursedetail.courseoutline_set.all()
        return [{'title': item.title} for item in courseoutlines]

class CourseChapterSerializer(serializers.ModelSerializer):
    '''
    专题课id=1所有章节
    '''
    courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['courses']

    def get_courses(self,row):
        coursechapters = row.coursechapters.all()
        return [{'name': item.name} for item in coursechapters]