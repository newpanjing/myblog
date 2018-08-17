from django.test import TestCase

# Create your tests here.
import re

p = re.compile(r'(&\w+;|(\w+;))')
aa = re.sub(p, '',
            '')
print(aa)