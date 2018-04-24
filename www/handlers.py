from coroweb import get, post
from models import User, Blog, Comment, next_id
import time
import re
from apis import APIValueError, APIError
import hashlib
from aiohttp import web
import json
from config import configs
import logging

_COOKIE_KEY = configs.session.secret
COOKIE_NAME = 'hikari_session'


def user2cookie(user, max_age):
    # 计算加密cookie, cookie字符串为: id-expires-sha1
    expires = str(int(time.time() + max_age))  # 当前时间+最大寿命即为过期时间
    s = '{}-{}-{}-{}'.format(user.id, user.pwd, expires, _COOKIE_KEY)
    lst = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(lst)


async def cookie2user(cookie_str):
    # 解析cookie
    if not cookie_str:
        return
    try:
        lst = cookie_str.split('-')

        if len(lst) != 3:
            return
        uid, expires, sha1 = lst

        if int(float(expires)) < time.time():
            print('过期啦')
            return
        user = await User.find(uid)
        if user is None:
            return
        s = '{}-{}-{}-{}'.format(uid, user.pwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return
        user.pwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return


# index change ---------------------------------
@get('/')
async def index(*, page='1'):
    # 获取所有blog分页显示
    page_index = get_page_index(page)
    num = await Blog.find_number('count(id)')
    page = Page(num, page_index)
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.find_all(order_by='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'myblog.html',
        'page': page,
        'blogs': blogs
    }


# change api/users----------------
@get('/api/users')
async def api_get_users(request, *, page='1'):
    check_admin(request)  # 非管理员不能直接访问显示
    # 获取所有用户信息分页显示
    page_index = get_page_index(page)
    num = await User.find_number('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.find_all(order_by='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.pwd = '******'
    return dict(page=p, users=users)


# -------------------------------------------------------------------------------------
# 注册

_re_email = r'^\w+@\w+(\.[a-z]{2,3}){1,2}$'
_re_sha1 = r'^[0-9a-f]{40}$'


@post('/api/users')
async def api_register_user(*, email, name, pwd):
    # 用户注册
    name = name.strip()
    if not name:
        raise APIValueError('name')
    if not email or not re.match(_re_email, email):
        raise APIValueError('email')
    if not pwd or not re.match(_re_sha1, pwd):
        raise APIValueError('password')
    users = await User.find_all('email=?', [email])  # 查询邮箱是不是已经存在
    if len(users) > 0:  # 邮箱已经存在用户
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    new_pwd = '{}:{}'.format(uid, pwd)
    user = User(id=uid, name=name, email=email, pwd=hashlib.sha1(new_pwd.encode('utf-8')).hexdigest(),
                image='http://www.gravatar.com/avatar/{}?s=80&d=identicon&r=g'.format(
                    hashlib.md5(email.encode('utf-8')).hexdigest()))
    await user.save()  # 注册用户信息保存至数据库
    # 创建session的cookie
    res = web.Response()
    res.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.pwd = '******'
    res.content_type = 'application/json'
    res.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return res


# --------------------------------------------------------------------------------------
# 登录认证
@post('/api/authenticate')
async def authenticate(*, email, pwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not pwd:
        raise APIValueError('password', 'Invalid password.')
    users = await User.find_all('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # 检查密码
    new_pwd = '{}:{}'.format(user.id, pwd)
    if user.pwd != hashlib.sha1(new_pwd.encode('utf-8')).hexdigest():
        raise APIValueError('password', 'Invalid password.')
    # 登录成功,设置cookie
    res = web.Response()
    res.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.pwd = '******'
    res.content_type = 'application/json'
    res.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return res


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@get('/signout')
def signout(request):  # 登出,重定向首页
    referer = request.headers.get('Referer')
    res = web.HTTPFound(referer or '/')
    res.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return res


# --------------------------------------
from apis import APIPermissionError


# 检查是不是管理员,有没有权限
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


# REST API, 用于创建一个Blog
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)  # 管理员才能创建blog
    # name,summary, content都不能为空
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    # 创建blog对象, 保存到数据库
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@get('/manage/blogs/create')  # 创建blog的视图函数
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/api/blogs/{id}')
async def api_get_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    return blog


def text2html(text):
    # text按行拆成列表, 滤去空字符, 将特殊字符转义, 加上p标签, 再拼接字符串
    lines = map(lambda s: '<p>{}</p>'.format(s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


import markdown


@get('/blog/{id}')
async def get_blog(id):  # 获取指定id的blog
    blog = await Blog.find(id)
    comments = await Comment.find_all('blog_id=?', [id], order_by='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    # 需要添加扩展的列表
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    blog.html_content = markdown.markdown(blog.content, extensions=exts)
    return {
        '__template__': 'blog.html',  # 需要写一个blog.html模板
        'blog': blog,
        'comments': comments
    }


#  -----------------------------------------------------------
# 分页----------------

def get_page_index(page_str):
    # 字符串页数变为整数, 非法页数全变为 1
    p = 1
    try:
        p = int(page_str)
    except ValueError:
        pass
    if p < 1:
        p = 1
    return p


from apis import Page


@get('/api/blogs')
async def api_blogs(request, *, page='1'):
    check_admin(request)
    page_index = get_page_index(page)  # 指定页数
    num = await Blog.find_number('count(id)')  # 总条目数?
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    # 从offset开始limit条
    blogs = await Blog.find_all(order_by='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


# add -------------------
@get('/manage/')  # 点击管理默认重定向到博客管理页面
def manage():
    return 'redirect:/manage/blogs'


# add-------------
@get('/manage/comments')
def manage_comments(*, page='1'):  # 管理评论
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }


# add--------
@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/{}'.format(id)
    }


# add--------------
@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }


# add------------
@get('/api/comments')
async def api_comments(request, *, page='1'):
    check_admin(request)
    # 获取所有评论分页显示
    page_index = get_page_index(page)
    num = await Comment.find_number('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.find_all(order_by='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


# add---------
from apis import APIResourceNotFoundError


@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:  # 未登录不能评论
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():  # 没有内容
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image,
                      content=content.strip())
    await comment.save()
    return comment


# add------------
@post('/api/comments/{id}/delete')
async def api_delete_comments(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    await c.remove()
    return dict(id=id)


@post('/api/blogs/{id}/delete')
async def api_delete_blog(id, request):
    # 删除指定id的blog
    check_admin(request)
    b = await Blog.find(id)
    if b is None:
        raise APIResourceNotFoundError('Blog')
    await b.remove()
    return dict(id=id)


@post('/api/blogs/{id}')
async def api_update_blog(id, *, name, summary, content):
    # 获取指定id的blog修改
    blog = await Blog.find(id)
    blog.name = name
    blog.summary = summary
    blog.content = content
    await blog.update()
    return blog


@get('/api/test')
def api_get():
    return {'name': 'hikari', 'age': 25, 'school': '皇家幼稚园', 'job': '搬砖'}


@get('/test')
def test():
    return {'__template__': 'test.html'}
