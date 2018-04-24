# 导入Fabric API
from fabric.api import *
from datetime import datetime
import os
import re

# 服务器登录用户名
env.user = 'hikari'
# sudo用户为root
env.sudo_user = 'root'
# 服务器地址可以有多个, 依次部署
env.hosts = ['192.168.1.101']

# 服务器MySQL用户名和口令
db_user = 'root'
db_password = 'mysql'


# --------------------------
def _current_path():
    return os.path.abspath('.')


def _now():
    return datetime.now().strftime('%Y-%m-%d_%H.%M.%S')


# ---------------


_TAR_FILE = 'myblog.tar.gz'


def build():
    # 打包任务
    includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/{}'.format(_TAR_FILE))
    # 把当前命令的目录设定为lcd()指定的目录
    with lcd(os.path.join(_current_path(), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/{}'.format(_TAR_FILE)]
        cmd.extend(['--exclude=\'{}\''.format(x) for x in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))  # local()运行本地命令


# -----------------------------


_REMOTE_TMP_TAR = '/tmp/{}'.format(_TAR_FILE)
_REMOTE_BASE_DIR = '/srv/hikari_web_app'


def deploy():
    newdir = 'www-{}'.format(_now())
    # run()函数执行的命令是在服务器上运行
    run('rm -f {}'.format(_REMOTE_TMP_TAR))  # 删除已有的tar文件
    put('dist/{}'.format(_TAR_FILE), _REMOTE_TMP_TAR)  # 上传新的tar文件
    # 根据时间创建新目录
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir {}'.format(newdir))
    # 解压到新目录
    with cd('{}/{}'.format(_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf {}'.format(_REMOTE_TMP_TAR))
    # 重置软链接
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s {} www'.format(newdir))
        # 将www的拥有者设为users群体的hikari
        sudo('chown hikari:users www')
        sudo('chown -R hikari:users {}'.format(newdir))  # -R对指定目录递归改变拥有者
    # 重启Python服务和nginx服务器
    with settings(warn_only=True):
        sudo('supervisorctl stop hikari_web_app')
        sudo('supervisorctl start hikari_web_app')
        sudo('/etc/init.d/nginx reload')


# -------------------
def backup():
    # Dump entire database on server and backup to local.
    dt = _now()
    f = 'backup-hikari_web_app-{}.sql'.format(dt)
    with cd('/tmp'):
        run(
            'mysqldump --user={} --password={} --skip-opt --add-drop-table --default-character-set=utf8 --quick hikari_web_app > {}'.format(
                db_user, db_password, f))
        run('tar -czvf {}.tar.gz {}'.format(f, f))
        get('{}.tar.gz'.format(f), '{}/backup/'.format(_current_path()))
        run('rm -f {}'.format(f))
        run('rm -f {}.tar.gz'.format(f))


def rollback():
    # rollback to previous version
    with cd(_REMOTE_BASE_DIR):
        r = run('ls -p -1')
        files = [s[:-1] for s in re.split(p, r) if s.startswith('www-') and s.endswith('/')]
        files.sort(reverse=True)
        r = run('ls -l www')
        ss = r.split(' -> ')
        if len(ss) != 2:
            print('ERROR: \'www\' is not a symbol link.')
            return
        current = ss[1]
        print('Found current symbol link points to: {}\n'.format(current))
        try:
            index = files.index(current)
        except ValueError:
            print('ERROR: symbol link is invalid.')
            return
        if len(files) == index + 1:
            print('ERROR: already the oldest version.')
        old = files[index + 1]
        print('==================================================')
        for f in files:
            if f == current:
                print('      Current ---> {}'.format(current))
            elif f == old:
                print('  Rollback to ---> {}'.format(old))
            else:
                print('                   {}'.format(f))
        print('==================================================')
        print()
        yn = input('continue? y/N ')
        if yn != 'y' and yn != 'Y':
            print('Rollback cancelled.')
            return
        print('Start rollback...')
        sudo('rm -f www')
        sudo('ln -s {} www'.format(old))
        sudo('chown hikari:users www')
        with settings(warn_only=True):
            sudo('supervisorctl stop hikari_web_app')
            sudo('supervisorctl start hikari_web_app')
            sudo('/etc/init.d/nginx reload')
        print('ROLLBACKED OK.')


def restore2local():
    # Restore db to local
    backup_dir = os.path.join(_current_path(), 'backup')
    fs = os.listdir(backup_dir)
    files = [f for f in fs if f.startswith('backup-') and f.endswith('.sql.tar.gz')]
    files.sort(reverse=True)
    if len(files) == 0:
        print('No backup files found.')
        return
    print('Found {} backup files:'.format(len(files)))
    print('==================================================')
    n = 0
    for f in files:
        print('{}: {}'.format(n, f))
        n += 1
    print('==================================================')
    print()
    try:
        num = int(input('Restore file: '))
    except ValueError:
        print('Invalid file number.')
        return
    restore_file = files[num]
    yn = input('Restore file {}: {}? y/N '.format(num, restore_file))
    if yn != 'y' and yn != 'Y':
        print('Restore cancelled.')
        return
    print('Start restore to local database...')
    p = input('Input mysql root password: ')
    sqls = [
        'drop database if exists hikari_web_app;',
        'create database hikari_web_app;',
        'grant select, insert, update, delete on awesome.* to \'{}\'@\'localhost\' identified by \'{}\';'.format(
            db_user, db_password)
    ]
    for sql in sqls:
        local(r'mysql -u root -p{} -e "{}"'.format(p, sql))
    with lcd(backup_dir):
        local('tar zxvf {}'.format(restore_file))
    local(r'mysql -u root -p{} hikari_web_app < backup/{}'.format(p, restore_file[:-7]))
    with lcd(backup_dir):
        local('rm -f {}'.format(restore_file[:-7]))
