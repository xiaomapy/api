# !/usr/bin/env python
# -*-coding:utf-8 -*-
import redis
import json

from django.conf import settings
from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser

from api import models
from api import serializer
from api.utils.response import BaseResponse


CONN = redis.Redis(host='192.168.11.183',port=6379)

class ShoppingCarView(ViewSetMixin,APIView):

    def list(self,request,*args,**kwargs):
        response = BaseResponse()
        try:
            shopping_car_list = []
            #  'shopping_car_%s_%s'
            pattern = settings.LUFFY_SHOPPING_CAR %(1,'*')  # 查询当前用户的所有的课程
            shopping_list = CONN.keys(pattern)
            for key in shopping_list:
                tamp = {
                    'id':CONN.hget(key,'id').decode('utf-8'),
                    'name':CONN.hget(key,'name').decode('utf-8'),
                    'img':CONN.hget(key,'img').decode('utf-8'),
                    'default_price_id':CONN.hget(key,'default_price_id').decode('utf-8'),
                    'price_policy_dict':json.loads(CONN.hget(key,'price_policy_dict').decode('utf-8')),
                }
                shopping_car_list.append(tamp)
                response.code = 200
                response.data = shopping_car_list
            # print(shopping_car_list)
        except Exception as e:
            response.code = 4004
            response.error = '查询购物车失败'

        return Response(response.dict)

    def create(self,request,*args,**kwargs):
        '''
        加入购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        1. 接受用户选中的课程ID和价格策略ID
        2. 判断合法性
            - 课程是否存在？
            - 价格策略是否合法？
        3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        '''
        response = BaseResponse()
        # 1.接受用户提交的课程ID和价格策略ID

        # 接受json数据后，只能在response.body中取数据；APIView对数据进行了封装，我们直接在request.data中取即可。
        course_id = request.data.get('courseId')
        price_id = request.data.get('priceId')


        # 2.1判断课程合法性
        course_obj = models.Course.objects.filter(id=course_id).first()

        if not course_obj:
            response.code = 4000
            response.error = '选择的课程不存在'
            return Response(response.dict)

        # 2.2判断价格合法性
        price_policy_list = course_obj.price_policy.all()

        price_policy_dict = {}
        for item in price_policy_list:
            temp = {
                    'id':item.id,
                    'price':item.price,
                    'valid_period':item.valid_period,
                    'valid_period_display':item.get_valid_period_display(),
            }

            price_policy_dict[item.id]=temp

        if price_id not in price_policy_dict:
            response.code = 4001
            response.error = '选择的价格不匹配，您已无权操作'
            return Response(response.dict)
        try:
            # 3 添加课程和对应的价格 到redis中
            '''
            购物车的redis表结构
            {
                shopping_car_'用户id'_'课程id':{
                    id:课程id
                    name:课程名
                    img:课程图片
                    default_price_id:课程默认价格id
                    price_policy_dict:课程所有价格列表
                }
            }
            '''
            key = settings.LUFFY_SHOPPING_CAR %(1,course_id)  # 'shopping_car_%s_%s'
            CONN.hset(key,'id',course_id)
            CONN.hset(key,'name',course_obj.name)
            CONN.hset(key,'img',course_obj.course_img)
            CONN.hset(key,'default_price_id',price_id)
            CONN.hset(key,'price_policy_dict',json.dumps(price_policy_dict))  # 需对字典序列化后保存

            response.code = 200
            response.data = '已添加到购物车'
        except Exception as e:
            response.code = 4003
            response.data = '添加购物车失败'
        return Response(response.dict)

    def update(self,request,*args,**kwargs):
        '''
        获取用户修改的课程价格
        :param request:
        :param args:
        :param kwargs:
        :return:
        1.获取修改课程的id和价格id
        2.做合法性校验；（在redis中校验即可）
        '''
        response = BaseResponse()
        # 获取用户修改的课程的id和价格id
        try:
            course_id = request.data.get('courseId')
            price_id = str(request.data.get('priceId')) if request.data.get('priceId') else None
            print(price_id,type(price_id))

            key = settings.LUFFY_SHOPPING_CAR %(1,course_id)
            print(key)
            if not CONN.exists(key):  # CONN.exists(key) 判断key存在于redis中
                response.code = 4005
                response.error = '修改的课程不存在'
                return Response(response.dict)
            # 修改价格

            price_policy_dict = json.loads(CONN.hget(key,'price_policy_dict').decode('utf-8'))

            if price_id not in price_policy_dict:
                response.code = 4006
                response.error = '修改的价格不存在'
                return Response(response.dict)
            CONN.hset(key,'default_price_id',price_id)
            response.code = 200
            response.data = '修改价格成功'
            return Response(response.dict)
        except Exception as e:
            response.code = 4007
            response.data = '修改价格失败'
            return Response(response.dict)

    def destroy(self,request,*args,**kwargs):
        '''
         删除购物车中的某个课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        response = BaseResponse()
        try:
            course_id = request.data.get('courseId')

            key = settings.LUFFY_SHOPPING_CAR %(1,course_id)  # 查出key值

            CONN.delete(key)    # 直接删除redis中key对应的整条记录
            response.code = 200
            response.data = '删除成功'
            return Response(response.dict)
        except Exception as e:
            response.code = 4008
            response.data = '删除失败'
            return Response(response.dict)


