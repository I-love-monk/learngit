#!/usr/bin/env python
#--*-- coding:utf-8--*--
from django.utils.safestring import mark_safe
import datetime
import json

def checkint(page):
    try:
        page = int(page)
    except:
        page = 1
    return page


def pagerange(all_count,page,per_num=6):
    
    range_list = []
    all_page = divmod(all_count, per_num)
    if all_page[1] == 0:
        all_page = all_page[0]
    else:
        all_page = all_page[0] + 1
    
    start = (page-1)*per_num
    end = page*per_num 
    if end > all_count:
        end = all_count
    
    range_list.append(start)
    range_list.append(end)
    range_list.append(all_page)
    
    return range_list


def pagelist(page,all_page):
    page_list = []
    page_list.append("<a >总共%d <i class='label-arrow'></i></a>"%all_page)
    first_page = "<a href='/index/1'>首页 <i class='label-arrow'></i></a>"
    page_list.append(first_page)
    if page <= 1:
        prev_page = "<a href='/index/%d'>上一页 <i class='label-arrow'></i></a>"%page
    else:
        prev_page = "<a href='/index/%d'>上一页 <i class='label-arrow'></i></a>"%(page-1)
    page_list.append(prev_page)
    if page >= all_page:
        next_page = "<a href='/index/%d'>下一页 <i class='label-arrow'></i></a>"%(page)
    else:
        next_page = "<a href='/index/%d'>下一页 <i class='label-arrow'></i></a>"%(page+1)
    page_list.append(next_page)
    last_page = "<a href='/index/%d'>尾页 <i class='label-arrow'></i></a>"%all_page
    page_list.append(last_page)
    page_list.append("当前<a id='current_page'>%d <i class='label-arrow'></i></a>"%page)
    page_list = mark_safe(''.join(page_list))
    return page_list

def pagelist_type(type_id,page,all_page):
    type_id = int(type_id)
    page_list = []
    page_list.append("<a >总共%d <i class='label-arrow'></i></a>"%all_page)
    first_page = "<a href='/index_type/%d/1'>首页 <i class='label-arrow'></i></a>"%type_id
    page_list.append(first_page)
    if page <= 1:
        prev_page = "<a href='/index_type/%d/%d'>上一页 <i class='label-arrow'></i></a>"%(type_id,page)
    else:
        prev_page = "<a href='/index_type/%d/%d'>上一页 <i class='label-arrow'></i></a>"%(type_id,page-1)
    page_list.append(prev_page)
    if page >= all_page:
        next_page = "<a href='/index_type/%d/%d'>下一页 <i class='label-arrow'></i></a>"%(type_id,page)
    else:
        next_page = "<a href='/index_type/%d/%d'>下一页 <i class='label-arrow'></i></a>"%(type_id,page+1)
    page_list.append(next_page)
    last_page = "<a href='/index_type/%d/%d'>尾页 <i class='label-arrow'></i></a>"%(type_id,all_page)
    page_list.append(last_page)
    page_list.append("当前<a id='current_page'>%d <i class='label-arrow'></i></a>"%page)
    page_list = mark_safe(''.join(page_list))
    return page_list


class CJenoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)
        
'''        
import re
content = "afa\nsafd\n<pre>\nasassd\n</pre>\nqcqcwq"
pattern = re.compile(r"<pre>[\s\S]*?</pre>")
code_list = pattern.findall(content)
print(code_list)
for i in code_list:
    content.replace(i,'code')
print(content.split("\n"))
'''
