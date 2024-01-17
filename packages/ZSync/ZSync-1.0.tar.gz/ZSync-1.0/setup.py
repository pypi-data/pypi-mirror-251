from setuptools import setup, find_packages

setup(
    name='ZSync',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='ZhouXin',
    author_email='zhou.xin2000@outlook.com',
    description='',
    entry_points={
            'console_scripts': [
                'zsync=zsync.ZSync:main',  # 'sync'是命令名，'your_package.sync'是模块名，'main'是你的脚本中用于启动程序的函数
            ],
        },
)
