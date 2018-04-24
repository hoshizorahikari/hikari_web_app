import functools


# def get(path):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kw):
#             return func(*args, **kw)
#
#         wrapper.__method__ = 'GET'
#         wrapper.__route__ = path
#         return wrapper
#
#     return decorator

# def post(path):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kw):
#             return func(*args, **kw)
#
#         wrapper.__method__ = 'POST'
#         wrapper.__route__ = path
#         return wrapper
#
#     return decorator


# 建立视图函数装饰器，用来存储、附带URL信息
def handler_decorator(path, *, method):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = method
        wrapper.__route__ = path

        return wrapper

    return decorator


# 偏函数。GET POST 方法的路由装饰器
get = functools.partial(handler_decorator, method='GET')
post = functools.partial(handler_decorator, method='POST')

# -------------------------------------------------------------------------------------------------

import inspect  # 使用inspect模块，检查视图函数的参数


def get_required_kw_args(f):  # 获取无默认值的关键字参数
    args = []
    params = inspect.signature(f).parameters
    for name, param in params.items():
        # 如果视图函数存在关键字参数,且无默认值,获取它的参数名
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)


def get_named_kw_args(f):  # 获取关键字参数
    args = []
    params = inspect.signature(f).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)


def has_named_kw_arg(f):  # 判断是否有关键字参数
    params = inspect.signature(f).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True


def has_var_kw_arg(f):  # 判断是否有可变关键词参数**kwargs
    params = inspect.signature(f).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True


def has_request_arg(f):  # 判断是否有名叫request的参数,且位置在最后
    sig = inspect.signature(f)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == 'request':
            found = True
            continue
        if found and (
                            param.kind != inspect.Parameter.VAR_POSITIONAL and
                            param.kind != inspect.Parameter.KEYWORD_ONLY and
                        param.kind != inspect.Parameter.VAR_KEYWORD):
            # param是POSITIONAL_OR_KEYWORD参数,但param位于request之后,即request位置不在最后,报错
            raise ValueError(
                'request parameter must be the last named parameter in function:{}{}'.format(f.__name__, sig))
    return found


# --------------------------------------------------------------------------------------------
from aiohttp import web
from urllib.parse import parse_qs
import logging
from apis import APIError


# 定义RequestHandler类,从视图函数中分析其需要接受的参数,
# 从web.Request中获取必要的参数,调用视图函数,把结果转换
# 为web.Response对象,符合aiohttp框架要求
class RequestHandler(object):
    def __init__(self, app, f):
        self._app = app
        self._func = f
        self._required_kw_args = get_required_kw_args(f)
        self._named_kw_args = get_named_kw_args(f)
        self._has_request_arg = has_request_arg(f)
        self._has_named_kw_arg = has_named_kw_arg(f)
        self._has_var_kw_arg = has_var_kw_arg(f)

    async def __call__(self, request):

        kw = None  # ① 定义kw，用于保存request中参数
        # ② 判断视图函数是否存在关键字参数,如果存在根据POST或者GET方法将request请求内容保存到kw
        if self._has_named_kw_arg or self._has_var_kw_arg:  # 若视图函数有关键字参数
            if request.method == 'POST':
                # 根据request参数中的content_type使用不同解析方法：
                if not request.content_type:  # 如果content_type不存在返回400错误
                    return web.HTTPBadRequest(text='Missing Content_Type.')
                ct = request.content_type.lower()  # 统一小写,便于检查
                if ct.startswith('application/json'):  # json格式数据
                    params = await request.json()  # 仅解析body字段的json数据
                    if not isinstance(params, dict):  # request.json()返回dict对象,若不是返回错误
                        return web.HTTPBadRequest(text='JSON body must be object.')
                    kw = params
                # form表单请求的编码形式
                elif ct.startwith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()  # 返回post的内容中解析后的数据,dict-like对象。
                    kw = dict(**params)  # 组成dict,统一kw格式
                else:
                    return web.HTTPBadRequest(text='Unsupported Content-Type: {}'.format(request.content_type))
            if request.method == 'GET':
                qs = request.query_string  # url查询字符串
                if qs:
                    kw = dict()
                    """
                    >>> qs='a=1&b=2&b=3&c=haha'
                    >>> parse_qs(qs,True)
                        {'a': ['1'], 'b': ['2', '3'], 'c': ['haha']}
                    """
                    # 值v是一个list,第2个参数keep_blank_values为True表示不忽略空格
                    for k, v in parse_qs(qs, True).items():  # 返回查询字符串键值对,dict对象
                        kw[k] = v[0]
        # ③ 如果kw为空,说明request无请求内容,则将match_info里的资源映射给kw;若不为空,把关键字参数内容给kw
        if kw is None:
            # request.match_info返回dict对象,键为可变路由中可变字段{variable}的参数名,
            # 值为传入request请求的path的对应值,比如路由为/user/{name},请求path为
            # /user/hikari,匹配路由,则request.match_info返回{'name':'hikari'}
            kw = dict(**request.match_info)
        else:
            if self._has_named_kw_arg and (not self._has_var_kw_arg):  # 若视图函数只有命名关键字参数没有可变关键词参数
                tmp = dict()
                for name in self._named_kw_args:
                    if name in kw:
                        tmp[name] = kw[name]
                kw = tmp  # 只保留命名关键字参数
            # 将request.match_info中的参数传入kw
            for k, v in request.match_info.items():
                # 检查kw中的参数是否和match_info中的重复
                if k in kw:  # 貌似和 if k in kw.keys() 一样
                    logging.warning('Duplicate arg name in named arg and kw args: {}'.format(k))
                kw[k] = v
        # ④ 善后工作
        if self._has_request_arg:  # 视图函数存在request参数
            kw['request'] = request
        if self._required_kw_args:  # 视图函数存在无默认值的关键字参数
            for name in self._required_kw_args:
                if name not in kw:  # 若未传入必须关键字参数值,报错
                    return web.HTTPBadRequest(text='Missing argument: {}'.format(name))
        # 至此kw为视图函数f真正能调用的参数
        # 也就是request请求中的参数终于传递给了视图函数
        logging.info('call with args: {}'.format(str(kw)))
        try:
            return await self._func(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)



            # return await self._func(**kw)


# ------------------------------------------------------------------

import asyncio


def add_route(app, f):  # 注册一个视图函数
    method = getattr(f, '__method__', None)
    path = getattr(f, '__route__', None)
    # 验证视图函数是否有method和path参数
    if method is None or path is None:
        raise ValueError('@get or @post not defined in {}.'.format(f.__name__))
    # 判断视图函数是否协程并且是生成器
    if not asyncio.iscoroutinefunction(f) and not inspect.isgeneratorfunction(f):
        # 将视图函数转为协程
        f = asyncio.coroutine(f)
    logging.info(
        'add route {} {} --> {}({})'.format(method, path, f.__name__,
                                            ','.join(inspect.signature(f).parameters.keys())))
    # 在app中注册经RequestHandler类封装的视图函数
    app.router.add_route(method, path, RequestHandler(app, f))


# 导入模块,批量注册视图函数
def add_routes(app, module_name):
    n = module_name.rfind('.')  # 从右侧检索返回索引
    # 导入整个模块
    if n == -1:
        # __import__ 作用同import语句,但__import__是一个函数,参数为模块的字符串名字
        # __import__('urllib',globals(),locals(),['request'], 0)等价于from urllib import request
        mod = __import__(module_name, globals(), locals())
    else:
        # 比如'urllib.request'->name='request',获取urllib模块对象的request属性得到urllib.request模块对象
        name = module_name[(n + 1):]
        # 获取对应的模块对象
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name], 0), name)
    # dir()获取模块所有类、实例、函数等对象的str形式
    for attr in dir(mod):
        if attr.startswith('_'):
            continue  # 忽略'_'开头的对象
        f = getattr(mod, attr)
        if callable(f):  # 可以被调用
            # 确保视图函数存在method和path
            method = getattr(f, '__method__', None)
            path = getattr(f, '__route__', None)
            if method and path:
                add_route(app, f)  # 注册视图函数


import os


# 添加静态文件，如image, css, js等文件
def add_static(app):
    # 获取本文件绝对路径-->获取根目录-->拼接同目录的static目录
    # path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    # 上面太麻烦了,abspath('.')可以直接获取当前文件根目录的绝对路径
    path = os.path.join(os.path.abspath('.'), 'static')

    app.router.add_static('/static/', path)  # 注册静态文件
    logging.info('add static {} --> {}'.format('/static/', path))
