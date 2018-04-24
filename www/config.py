import config_default


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super().__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v  # names每个元素为键,values对应位置元素为值

    # 可以dct.key或dct[key]获取或设置属性
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


# 合并设置
def merge(defaults, override):
    ret = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                ret[k] = merge(v, override[k])  # 若v是dict, 递归
            else:
                ret[k] = override[k]  # k有新值, 覆盖默认值
        else:
            ret[k] = v  # override没有k, 使用默认值
    return ret


def to_dict(configs):
    d = Dict()
    for k, v in configs.items():
        d[k] = to_dict(v) if isinstance(v, dict) else v  # 若v是dict, 递归
    return d


configs = config_default.configs
try:
    import config_override

    configs = merge(configs, config_override.configs)  # 获得合并的configsdict, dict类型
except ImportError:
    pass
configs = to_dict(configs)  # 将configs变为Dict类的实例, 可以通过configs.k直接获取v, 不是必要
if __name__ == '__main__':
    print(configs.db.user)  # hikari
    print(configs['db']['host'])  # 192.168.1.101
    print(configs.db['port'])  # 3306
