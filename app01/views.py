from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from api import models

def query(request):

    # a.查看所有学位课并打印学位课名称以及授课老师
    DegreeCourse_list = models.DegreeCourse.objects.all().values('name','teachers__name')


    # b. 查看所有学位课并打印学位课名称以及学位课的奖学金
    DegreeCourse_scholarship_list = models.DegreeCourse.objects.all().values('name', 'total_scholarship')


    # c.展示所有的专题课
    Course_list = models.Course.objects.filter(degree_course__isnull=True)


    # d.查看id = 1的学位课对应的所有模块名称
    degree_course = models.DegreeCourse.objects.filter(id=1).values('course__name')



    # e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    Course_obj = models.Course.objects.filter(id=1).values(
            'name',
            'level',
            'coursedetail__why_study',
            'coursedetail__what_to_study_brief',
            'coursedetail__recommend_courses'
        )



    # f.获取id = 1的专题课，并打印该课程相关的所有常见问题
    obj = models.Course.objects.filter(id=1).first()
    all_question = obj.asked_question.all()


    # g.获取id = 1的专题课，并打印该课程相关的课程大纲
    CourseOutlines = models.Course.objects.filter(id=1).values('coursedetail__courseoutline__title')


    # h.获取id = 1的专题课，并打印该课程相关的所有章节
    coursechapters = models.Course.objects.filter(id=1).values('coursechapters__name')



    # i.获取id = 1的专题课，并打印该课程相关的所有课时
    # 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    CourseSections = models.Course.objects.filter(id=1).values('coursechapters__coursesections__name','coursechapters__coursesections__video_time')


    # j.获取id = 1的专题课，并打印该课程相关的所有的价格策略
    obj = models.Course.objects.filter(id=1).first()
    PricePolicys = obj.price_policy.all()
    print(PricePolicys)






    # return HttpResponse('ok')
    return render(request,'queryORM.html',locals())