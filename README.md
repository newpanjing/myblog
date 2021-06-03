# myblog
simpleui官方博客，利用django+django-simpleui

## 友情提示

如果你在使用过程中遇到任何问题，可以联系我们付费提供技术支持，并且可以定制开发。价格实惠。

联系QQ： 599194993

邮箱： newpanjing@icloud.com

# 演示地址
https://www.88cto.com

# 安装步骤
## 第一步

使用豆瓣源安装依赖包

```shell
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -r requirements.txt 
```

## 第二步
请在`settings.py`中配置你的数据库连接，创建个空数据库就可以了

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'myblog',
        'PASSWORD': '5rWEu98A',
        'HOST': 'mysql.oracle.com',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
        'CONN_MAX_AGE': 600
    }
}

```

## 第三步

执行数据库迁移，自动创建表

```shell
python3 manage.py migrate
```

## 第四步

创建一个超级用户名和密码，按提示输入用户名和密码即可

```shell
python3 manage.py createsuperuser
```

## 第五步
```shell
python manage.py runserver 8000
```

## 第六步
打开浏览器 访问前台地址和后台地址

+ 前台地址

[http://localhost:8000](http://localhost:8000)

+ 后台地址

[http://localhost:8000/admin](http://localhost:8000/admin)

打开后台之后，输入第四步创建的用户名和密码即可
