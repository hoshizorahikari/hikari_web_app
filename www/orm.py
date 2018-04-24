import asyncio
import logging
import aiomysql


def log(sql, args=()):  # 控制台打印SQL语句
    logging.info('SQL: {}'.format(sql))


async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


async def destroy_pool():  # 程序结束之前手动关闭mysql连接池
    global __pool
    if __pool:
        __pool.close()
        await __pool.wait_closed()


async def select(sql, args=(), size=None):  # 查询
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # SQL语句的占位符是?,而MySQL的占位符是%s
            await cur.execute(sql.replace('?', '%s'), args)
            # if size:
            #     ret = await cur.fetchmany(size)
            # else:
            #     ret = await  cur.fetchall()
            # 获取指定数量的数据,若未指定获取全部
            # 调用子协程(在一个协程中调用另一个协程)并获得子协程的返回结果
            ret = await cur.fetchmany(size) if size else await cur.fetchall()
        logging.info('rows returned: {}'.format(len(ret)))
        return ret


async def execute(sql, args=(), autocommit=True):  # 增删改
    log(sql, args)
    async with __pool.get() as conn:
        if not autocommit:  # 如果不是自动提交,手动开始提交回滚
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount  # 影响的行数
            if not autocommit:
                await conn.commit()
        except BaseException:
            if not autocommit:
                await conn.rollback()
            raise  # 有异常,回滚并抛出异常
        return affected


# 可用函数或类当做元类,此处用类继承于type
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):  # 3个参数分别为类名,父类,类属性和值的字典
        if name == 'Model':  # Model类是父类,没有字段,不需要处理
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name  # 获取表名,没有就用类名做表名
        logging.info('found model: {} (table: {})'.format(name, table_name))
        mappings = dict()  # 保存所有字段的映射
        fields = []  # 保存非主键字段
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):  # 类属性值是字段的实例
                logging.info('  found mapping: {} ==> {}'.format(k, v))
                mappings[k] = v  # 保存字段的映射
                if v.primary_key:  # 找到主键保存
                    if primary_key:  # 若之前已经找到主键,又发现主键,则主键不唯一,抛出异常
                        raise RuntimeError('Duplicate primary key for field: {}'.format(k))
                    primary_key = k
                else:
                    fields.append(k)  # 保存非主键字段
        if not primary_key:  # 遍历完所有字段没有发现主键
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():  # 将原来字典字段属性清空
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`{}`'.format(f), fields))
        # 重新设置类属性与值的字典,将新创建的类返回
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系,如'name':StringField('name')
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # 以下四种方法保存了默认的增删改查操作,反引号``是为了避免与sql关键字冲突,否则sql语句会执行出错
        attrs['__select__'] = 'select `{}`, {} from `{}`'.format(primary_key, ', '.join(escaped_fields), table_name)
        attrs['__insert__'] = 'insert into `{}` ({}, `{}`) values ({})'.format(
            table_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `{}` set {} where `{}`=?'.format(
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'delete from `{}` where `{}`=?'.format(table_name, primary_key)
        return type.__new__(cls, name, bases, attrs)


# 这样，任何继承自Model的类（比如User），会自动通过ModelMetaclass扫描映射关系，
# 并存储到自身的类属性如__table__、__mappings__中。

class Model(dict, metaclass=ModelMetaclass):
    # 所有ORM映射的基类Model
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __getattr__(self, item):  # 获取值
        try:
            return self[item]
        except KeyError:
            raise AttributeError("'Model' object has no attribute '{}'".format(item))

    def __setattr__(self, key, value):  # 设置值
        self[key] = value

    def get_value(self, key):  # 获取值,没有此key则为None
        return getattr(self, key, None)

    def get_value_or_default(self, key):  # 使用默认值
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]  # 获取字段对应实例类型
            if field.default is not None:  # 如果此类型有默认值,采用该默认值
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for {}: {}'.format(key, value))
                setattr(self, key, value)
        return value

    # Model从dict继承，所以具备所有dict的功能，同时又实现了
    # 特殊方法__getattr__()和__setattr__()，因此又可以像引用普通字段那样写
    # user['id']或user.id
    # 定义类方法
    @classmethod
    async def find_all(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:  # where条件查询
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        order_by = kw.get('order_by', None)
        if order_by:  # order排序
            sql.append('order by')
            sql.append(order_by)
        limit = kw.get('limit', None)
        if limit is not None:  # 指定偏移,限制查询条数
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: {}'.format(limit))
        ret = await select(' '.join(sql), args)  # 拼接sql语句,查询
        return [cls(**i) for i in ret]

    @classmethod
    async def find_number(cls, select_field, where=None, args=None):
        sql = ['select {} _num_ from `{}`'.format(select_field, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        ret = await select(' '.join(sql), args, 1)
        if len(ret) == 0:
            return None
        return ret[0]['_num_']

    @classmethod
    async def find(cls, pk):
        # 根据主键寻找对象
        ret = await select('{} where `{}`=?'.format(cls.__select__, cls.__primary_key__), [pk], 1)
        if len(ret) == 0:
            return None
        return cls(**ret[0])

    # 实例方法
    # 插入数据到数据库
    async def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: {}'.format(rows))

    # 修改数据
    async def update(self):
        args = list(map(self.get_value, self.__fields__))
        args.append(self.get_value(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warning('failed to update by primary key: affected rows: {}'.format(rows))

    # 删除数据
    async def remove(self):
        args = [self.get_value(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: {}'.format(rows))


# ----------------------------------------------------------------
# 字段
def create_args_string(num):  # sql语句占位符字符串
    # L = []
    # for n in range(num):
    #     L.append('?')
    # return ', '.join(L)
    return ', '.join(['?'] * num)


class Field(object):  # 字段父类

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{}, {}:{}>'.format(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):  # 映射varchar的StringField

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


# --------------------------------------------------
# 测试


class User(Model):
    __table__ = 'user'
    id = IntegerField('id', primary_key=True)
    name = StringField('name')


async def test(loop, db, lst):
    await create_pool(loop, **db)
    for i in range(len(lst)):
        user = User()
        user.id = i + 1
        user.name = lst[i]
        await user.save()
    print('test insert over!')


async def show(loop, db):
    # await create_pool(loop, **db)
    await asyncio.sleep(1)
    ret = await User.find_all('id between 3 and 5')
    print(ret)
    await destroy_pool()
    print('show over!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    database = {
        'user': 'root',
        'password': 'mysql',
        'db': 'test'
    }
    lst = ['rin', 'maki', 'nozomi', 'nico', 'umi', 'kotori']
    task = [test(loop, database, lst), show(loop, database)]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()
