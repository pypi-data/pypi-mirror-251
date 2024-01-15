import setuptools
from setuptools import setup, find_packages

setup(
    name='dps_mysql_ha_sdk',
    version='1.3',
    packages=setuptools.find_packages(),
    package_data={'': ['dynamic_pooled_db.py']},  # 包含根目录下的 ab.py 文件
    # package_dir={'': 'src'},
    install_requires=[
        # List your dependencies here
    ],
    # Other project metadata
    author='daijiacong',
    description='高可用数据库连接',
    # url='https://github.com/daijiacong/your-sdk',
    license='MIT',
)
