from setuptools import setup

setup(
    name='myblog',
    version='1.0',
    packages=['models', 'models.migrations', 'myblog', 'myblog.utils', 'myblog.templatetags', 'article',
              'article.migrations'],
    url='88cto.com',
    license='Apache License 2.0',
    author='panjing',
    author_email='newpanjing@163.com',
    description='个人博客系统',
    install_requires=[
        'django',
        'shortid8',
        'oss2',
        'requests',
        'pymysql',
        'whoosh',
        'django-haystack',
        'jieba',
        'redis'
    ],
)
