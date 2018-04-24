import logging;

logging.basicConfig(level=logging.INFO)
import os
from jinja2 import Environment, FileSystemLoader


def init_jinja2(app, **kw):
    logging.info('init jinja2...')

    # ① 配置options参数,字典形式,是Environment(**options)的参数
    options = dict(
        # 自动转义xml/html的特殊字符
        autoescape=kw.get('autoescape', True),
        # 代码块的开始、结束标志
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        # 变量的开始、结束标志
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        # 自动加载修改后的模板文件
        auto_reload=kw.get('auto_reload', True)
    )

    path = kw.get('path', None)  # 获取模板文件目录路径
    if not path:
        # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        path = os.path.join(os.path.abspath('.'), 'templates')
    # Environment类是jinja2的核心类,用来保存配置、全局对象、模板文件的路径
    # ② 模板加载器FileSystemLoader类加载path路径中的模板文件
    env = Environment(loader=FileSystemLoader(path), **options)
    # ③ 创建Environment对象, 添加过滤器
    ft = kw.get('filters', None)
    if ft:
        for name, f in ft.items():
            env.filters[name] = f  # filters是Environment类的属性, 过滤器字典

    # jinja2的环境配置都在env对象中, 把env对象添加到app类字典对象中,
    # 这样app就知道模板的路径和解析模板的方法
    app['__template__'] = env  # app是一个dict-like对象


import time
from datetime import datetime


def datetime_filter(t):  # 模板语言的过滤器, 用于时间戳转为字符串, 显示博客发表时间
    delta = int(time.time() - t)
    # if delta < 0:  # 所以不可能未来发表的...此句注释吧
    #     return u'未来的某天'
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


# -------------------------------------------------------------------------------
from handlers import cookie2user, COOKIE_NAME
from aiohttp import web


# 利用中间件在处理URL之前, 把cookie解析, 并将登录用户绑定到request对象上
# 这样后续的视图就可以直接拿到登录用户
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: {} {}'.format(request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: {}'.format(user.email))
                request.__user__ = user
        if request.path.startswith('/manage/'):
            if request.__user__ is None or not request.__user__.admin:
                return web.HTTPFound('/signin')
        return await handler(request)

    return auth


# 编写一个用于打印日志的middleware, 和装饰器类似
async def logger_factory(app, handler):  # handler是视图函数

    async def logger(request):
        logging.info('Request: {} {}'.format(request.method, request.path))
        return await handler(request)

    return logger


# 打印日志的中间件, 打印POST请求json或表单数据
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: {}'.format(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: {}'.format(request.__data__))
        return await handler(request)

    return parse_data


# 响应对象response的处理工序：
# ① 由视图函数处理request后返回数据
# ② @get@post装饰器在返回对象上附加'__method__'和'__route__'属性，使其附带URL信息
# ③ response_factory对处理后的对象, 经一系列类型判断, 构造真正的web.Response对象


import json


# response中间件把返回值转换为web.Response对象再返回,保证满足aiohttp的要求
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        res = await handler(request)
        if isinstance(res, web.StreamResponse):  # StreamResponse是所有Response对象的父类
            return res
        if isinstance(res, bytes):
            # Response继承于StreamResponse, 接收body参数, 构造HTTP响应内容
            res = web.Response(body=res)
            res.content_type = 'application/octet-stream'
            return res
        if isinstance(res, str):
            if res.startswith('redirect:'):  # 若返回重定向字符串, 重定向至目标url
                return web.HTTPFound(res[9:])
            res = web.Response(body=res.encode('utf-8'))
            res.content_type = 'text/html;charset=utf-8'  #  utf-8编码的text格式
            return res
        if isinstance(res, dict):
            # 视图函数返回值会带有__template__值, 表示选择渲染的模板
            template = res.get('__template__')
            if template is None:  # 不带模板信息返回json对象
                res = web.Response(
                    body=json.dumps(res, ensure_ascii=False, default=lambda obj: obj.__dict__).encode('utf-8'))
                res.content_type = 'application/json;charset=utf-8'
                return res
            else:  # 带模板信息, 渲染模板
                # 获取已初始化的Environment对象, 调用get_template()返回Template对象
                # 调用Template对象的render()方法, 传入res渲染模板, 返回unicode格式字符串,用utf-8编码
                print('request.__user__', request.__user__)

                res['__user__'] = request.__user__
                tpl = app['__template__'].get_template(template)
                res = web.Response(body=tpl.render(**res).encode('utf-8'))
                # res = web.Response(body=app['__templating__'].get_template(template).render(**res).encode('utf-8'))
                res.content_type = 'text/html;charset=utf-8'
                return res
        if isinstance(res, int) and 100 <= res < 600:
            return web.Response(status=res)  # 返回响应码
        if isinstance(res, tuple) and len(res) == 2:
            code, msg = res  # 返回了响应码和原因的元组, 如(200, 'OK'), (404, 'Not Found')
            if isinstance(code, int) and 100 <= code < 600:
                return web.Response(status=code, text=msg)
        # 均以上条件不满足, 默认返回
        res = web.Response(body=str(res).encode('utf-8'))
        res.content_type = 'text/plain;charset=utf-8'
        return res

    return response


# ---------------------------------------------------------------------------------------
import asyncio
from coroweb import add_routes, add_static
import orm
from config import configs


async def init(loop):
    await orm.create_pool(loop, **configs.db)  # 从配置文件获取数据库信息,创建连接池
    app = web.Application(loop=loop, middlewares=[logger_factory, auth_factory, response_factory])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')  # 将handlers的视图函数添加路由
    add_static(app)  # 需要创建static目录
    server = await loop.create_server(app.make_handler(), 'localhost', 8000)
    logging.info('server started at http://127.0.0.1:8000...')
    return server


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

# def index(req):
#     return web.Response(body='<h1 style="color:red">hikari\'s web</h1>', content_type='text/html')
#
#
# # @asyncio.coroutine
# async def init(loop):
#     app = web.Application(loop=loop)
#     app.router.add_route('GET', '/', index)
#     server = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
#     logging.info('Server started at http://127.0.0.1:8000...')
#     return server
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()
