from setuptools import setup, find_packages

str_version = '1.0.6'

setup(name='skyctl',
      version=str_version,
      description='联云迁移工具',
      author='XieJunWei',
      author_email='643657447@qq.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires= ['pypinyin', 'opencv-python'],
      python_requires='>=3')

