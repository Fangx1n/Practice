# -*- coding: utf-8 -*-
import time

#13位 一般是10位
comment_time=1536142474051
print(int(time.time()))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment_time/1000)))
