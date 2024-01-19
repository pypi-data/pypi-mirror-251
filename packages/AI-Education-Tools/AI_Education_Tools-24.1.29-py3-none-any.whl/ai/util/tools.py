import os
import shutil
from importlib.abc import Traversable
from importlib.resources import files
from pathlib import Path

ai_home = Path.home() / 'ai_home'
ai_home.mkdir(parents=True, exist_ok=True)
ai_desktop = Path.home() / 'Desktop/零基础入门机器学习-从机器模型到Web应用集成实践'
def download_codes(dst=ai_desktop):
    """
    将教学案例拷贝到用户桌面
    :param dst: 拷贝文件的目标目录，默认是用户桌面
    :return:
    """
    src: Traversable = files('ai.codes')
    print('Copying,please wait....')
    shutil.copytree(str(src), dst, dirs_exist_ok=True)
    print('done!!')
    os.startfile(dst)