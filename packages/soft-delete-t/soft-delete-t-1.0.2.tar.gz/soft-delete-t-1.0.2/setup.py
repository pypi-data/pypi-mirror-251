from setuptools import setup, find_packages

setup(name='soft-delete-t',
      version='1.0.2',
      description='django soft delete',
      author='meihai',
      author_email='864561183@qq.com',
      requires=['django'],  # 定义依赖哪些模块
      url='https://gitee.com/hai_hpy/soft_delete.git',
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # packages=['models','admin','__init__'],  #指定目录中需要打包的py文件，注意不要.py后缀
      python_requires='>=3.9',
      )
'''
pypi-AgENdGVzdC5weXBpLm9yZwIkYmQxOGE0NDktYzI1Ni00N2E4LTk3MjQtOTliYTZhZjNlZWE4AAIqWzMsIjA2YzNkNjRkLWEyZmItNGM1My1hZmIyLTdmZTIxZmZmOWNlOSJdAAAGICvv91C-3BKySotjF3EvrTwT453VjX9NOHmAgRp8xcHv
'''
