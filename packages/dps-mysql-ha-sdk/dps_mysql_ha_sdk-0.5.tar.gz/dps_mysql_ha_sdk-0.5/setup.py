import setuptools
from setuptools import setup

setup(
    name='dps_mysql_ha_sdk',
    version='0.5',
    packages=setuptools.find_packages(),
    package_data={'': ['dynamic_pooled_db.py','test_demo.py']},
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
