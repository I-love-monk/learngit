#!/usr/bin/env python
#coding:utf-8
from django import template


register = template.Library()

@register.simple_tag
def content_summary(content):
    content=content.repalce("<P>")
    content=content.repalce("</P>")
    return content

