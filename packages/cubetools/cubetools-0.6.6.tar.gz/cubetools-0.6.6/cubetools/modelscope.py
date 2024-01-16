import os
import getpass
import subprocess
import fnmatch
from argparse import ArgumentParser

CACHE_DIR = os.path.join(os.path.expanduser('~'), '.modelscope_cache')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


def download_model(model_id, threads=10, exclude=None):
    clone_url = 'https://www.modelscope.cn/{}.git'
    file_url = 'http://www.modelscope.cn/api/v1/models/{}/repo?FilePath={}'

    if model_id.find('/') < 1:
        print('model_id格式不对！')
        return None

    model_dir = os.path.join(CACHE_DIR, model_id)
    if os.path.exists(model_dir):
        print('模型 {} 已存在！'.format(model_id))
        return model_dir

    # install aria2 and git
    username = getpass.getuser()
    cmd_prefix = '' if username == 'root' else 'sudo '
    status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt update')
    if status != 0:
        print('apt update 失败！')

    status, _ = subprocess.getstatusoutput('command -v aria2c')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y aria2')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y aria2')
            if status != 0:
                print('安装 aria2 失败！')
                return None

    status, _ = subprocess.getstatusoutput('command -v git')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y git')
            if status != 0:
                print('安装 git 失败！')
                return None

    status, _ = subprocess.getstatusoutput('command -v git-lfs')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git-lfs')
        if status != 0:
            status, _ = subprocess.getstatusoutput(cmd_prefix + 'yum install -y git-lfs')
            if status != 0:
                print('安装 git-lfs 失败！')
                return None

    cwd = os.getcwd()
    model_owner, model_name = model_id.split('/')
    owner_dir = os.path.join(CACHE_DIR, model_owner)
    if not os.path.exists(owner_dir):
        os.mkdir(owner_dir)
    os.chdir(owner_dir)

    # Clone模型代码（不下载长文件）
    url = clone_url.format(model_id)
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'
    status, _ = subprocess.getstatusoutput('git clone ' + url)
    if status != 0:
        print('克隆 {} 失败！'.format(url))
        os.chdir(cwd)
        return None

    # 找出所有长文件
    os.chdir(model_dir)
    status, output = subprocess.getstatusoutput('git lfs ls-files')
    output = output.split('\n')
    ls_files = []
    for line in output:
        file = line.split(' ')[2]
        ls_files.append(file)
        os.system('truncate -s 0 ' + file)

    # 下载所有长文件
    for file in ls_files:
        url = file_url.format(model_id, file)
        file_dir = subprocess.getoutput('dirname ' + file)
        file_name = subprocess.getoutput('basename ' + file)

        if exclude is not None:
            match = False
            for pattern in exclude:
                if fnmatch.fnmatch(file_name, pattern):
                    match = True
                    os.system('rm ' + file)
                    break
            if match:
                continue

        os.system('mkdir -p ' + file_dir)
        os.system('aria2c -x {} -s {} -k 1M -c {} -d {} -o {}'.format(threads, threads, url, file_dir, file_name))

    os.chdir(cwd)
    return os.path.join(CACHE_DIR, model_id)


def download_model_cmd():
    parser = ArgumentParser()
    parser.add_argument('model_id', default=None, help='ModelScope model ID, like: model_owner/model_name')
    parser.add_argument('--threads', default=10, type=int, help='Number of download threads for aria2c')
    parser.add_argument('--exclude', default=None,
                        help='The patterns to match against filenames for exclusion, seperated with ","')
    args = parser.parse_args()

    if args.model_id is None:
        parser.print_usage()
        return

    exclude = None if args.exclude is None else args.exclude.split(',')
    download_model(model_id=args.model_id, threads=args.threads, exclude=exclude)


if __name__ == '__main__':
    download_model('cubeai/pangu2b6-cpu')
