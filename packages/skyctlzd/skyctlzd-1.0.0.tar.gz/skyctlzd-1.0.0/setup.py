from setuptools import setup, find_packages

str_version = '1.0.0'

setup(name='skyctlzd',
      version=str_version,
      description='联云迁移工具',
      author='xiejunwei',
      author_email='xiejunwei@qq.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires= ['pypinyin', 'opencv-python'],
      python_requires='>=3')

