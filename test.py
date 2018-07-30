#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
**************************************************************************
 * Copyright (c) 2015-2017 Zhejiang TaChao Network Technology Co.,Ltd.
 * All rights reserved.
 *
 * 项目名称：浙江踏潮
 * 版权说明：本软件属浙江踏潮网络科技有限公司所有，在未获得浙江踏潮网络科技有限公司正式授权
 *           情况下，任何企业和个人，不能获取、阅读、安装、传播本软件涉及的任何受知
 *           识产权保护的内容。
 ***************************************************************************
'''

'''
 * 测试Flask
 * @author <a href="mailto:dh@zjtachao.com">duhao</a>
'''
import datetime ,time ,json
from flask import Flask , request , make_response
from flask_restful import reqparse , abort , Api , Resource
from flask_redis import FlaskRedis
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy

#redis
REDIS_URL = "redis://:zjtachao@192.168.1.12:6379/0"

app = Flask(__name__)
app.config['REDIS_URL'] = REDIS_URL
api = Api(app)
redis_store = FlaskRedis.from_custom_provider(StrictRedis , app)

#mysql
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://zjtachao:123456@192.168.1.11:3306/ww?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

def serialize_instance(obj):
  d = { '__classname__' : type(obj).__name__ }
  d.update(vars(obj))
  return d

class User(db.Model):
    __tablename__ = "demo_user"
    id = db.Column(db.Numeric , primary_key=True)
    user_code = db.Column(db.String , unique=True)
    user_nickname = db.Column(db.String)
    user_age = db.Column(db.Integer)

class HelloWorld(Resource):
    def get(self):
        data = redis_store.get('aaa')
        user = User.query.first()
        #print json.dumps(user, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        resp = make_response(data , 200 ,{'Content-Type': 'application/json'})
        resp.set_cookie('aaa','bbb')
        return resp

api.add_resource(HelloWorld , '/', '/hello')

if __name__ == '__main__':
    app.run()