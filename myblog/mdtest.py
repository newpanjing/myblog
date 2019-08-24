import markdown

print(markdown.markdown('''
[TOC]
# 这是什么操作
这是一个无人机

## 后来
```python
aa=123
print(aa)
for i in range(1,100):
   print(i)
```
''', extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc',
]))
