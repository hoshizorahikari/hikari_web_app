# import json, logging, inspect, functools


class APIError(Exception):
    # APIError父类
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message


class APIValueError(APIError):
    # 输出值错误或无效
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value : invalid', field, message)


class APIResourceNotFoundError(APIError):
    # 资源没有找到
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value : not found', field, message)


class APIPermissionError(APIError):
    # api没有权限
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission : forbidden', 'permission', message)


# -----------------------------------------------------

class Page(object):
    # Page类用于存储分页信息
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count  # 总条目数
        self.page_size = page_size  # 一页的条目数
        # 总共多少页
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        # 如果总条目数为0或当前页数超过总页数
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index  # 当前页数
            self.offset = self.page_size * (page_index - 1)  # 偏移, 当前页之前总条目数
            self.limit = self.page_size
        # 是否有前一页或后一页
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: {}, page_count: {}, page_index: {}, page_size: {}, offset: {}, limit: {}'.format(
            self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
