import time
import uuid
from orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():  # 生成唯一id
    # uuid4()通过伪随机数得到uuid,32位16进制
    return '{:015d}{}000'.format(int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):  # 用户模型
    __table__ = 'users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    pwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)  # 创建时间



class Blog(Model):  # 博客模型
    __table__ = 'blogs'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):  # 评论模型
    __table__ = 'comments'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)
