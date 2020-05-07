# -*- coding: utf-8 -*-
import codecs
import re
import chardet
from bs4 import BeautifulSoup, Comment
import os
import shutil


def init():
    path = os.getcwd()  # 文件夹目录
    html_dir = os.path.join(path, 'html')
    files = os.listdir(html_dir)  # 得到文件夹下的所有文件名称
    format_dir = os.path.join(path, 'format_html')

    # 如果目录存在，直接删除
    if os.path.exists(format_dir):
        shutil.rmtree(format_dir)

    os.mkdir(format_dir)

    for file in files:  # 遍历文件夹
        file_split = file.split('.')
        # os.path.isfile 需要传入文件的绝对路径
        if (os.path.isfile(os.path.join(html_dir, file))) and (file_split[len(file_split)-1] == 'html'):
            main(format_dir, html_dir, file)


def main(format_dir, html_dir, html_name):
    html = get_html(os.path.join(html_dir, html_name))

    html = format_html(html)
    html = my_beautiful_soup(html)

    # html = re.sub(r'&nbsp;{2,}', r'&nbsp;', html)  # 去空格
    html = re.sub(r'\s+', r' ', html)  # 多个空格合并成一个 nbsp;被删除问题

    html = re.sub(r'<p>\s*?(\S*?)\s*?</p>', r'<p>\1</p>', html)  # 删除p元素首尾空格
    html = re.sub(r'<strong>\s*?(\S*?)\s*?</strong>', r'<strong>\1</strong>', html)  # 删除strong元素首尾空格
    # 在我们的需求里，只需要body内的内容，所以这样；不是这样的情况下，应该去掉这句
    html = re.sub(r'(.*?)<body(.*?)>(.*)<\/body>(.*)', r'<!-- () -->\3', html, flags=re.S)
    html = format_html1(html)
    html = format_html1(html)
    html = format_dp(html) # 删除档铺的标记
    # print(html)
    # pattern = re.compile(r'<p.*?><\/p>')
    # print(pattern.findall(html))

    save_file(html, os.path.join(format_dir, html_name))


# html_path - html 文档地址 export_path - 导出的 html 地址
def get_html(html_path):
    f = open(html_path, 'r')
    str = f.read()
    f.close()
    return str


# 格式化html
# res - 导出的 html
def format_html(res):
    # 在我们的需求里，只需要body内的内容，所以去掉；不是这样的情况下，应该恢复使用
    # res = re.sub(r'<html.*?>', r'<!DOCTYPE html>', res, flags=re.S)

    # 去掉批注
    res = re.sub(r'<div>.*?<hr\s+class=msocomoff.*?<\/body>', r'</body>', res, flags=re.S)
    res = re.sub(r'<a\s+class=msocomanchor.*?<\/a>', r'', res, flags=re.S)

    res = re.sub(r'\s+>', r'>', res)  # 标签结尾的空格
    res = re.sub(r'>\s+<', r'><', res)  # 去除标签之间的空格

    res = re.sub(r'<b>(.*?)<\/b>', r'<strong>\1</strong>', res, flags=re.S)

    return res


def format_html1(res):
    res = re.sub(r'</u><u>', r'', res)  # 合并连续的u元素
    res = re.sub(r'</strong><strong>', r'', res)  # 合并连续的strong元素
    res = re.sub(r'<strong>\s*?</strong>', '', res)
    res = re.sub(r'<p>\s*?</p>', r'', res)  # 空的p标签
    res = re.sub(r'<h\d><\/h\d>', '', res)  # 空的标题元素
    res = re.sub(r'<p align="center" style="text-align:center;"></p>', '', res)  # 空的标题元素
    return res


# 删除档铺的标记
def format_dp(res):
    res = re.sub(r'<div>档铺网——在线文档免费处理</div>', '', res)
    res = re.sub(r'<div id="_cmnt(.*?)</div>', '', res)
    return res

def my_beautiful_soup(html):
    soup = BeautifulSoup(html, "html5lib")

    # 在我们的需求里，只需要body内的内容，所以去掉；不是这样的情况下，应该恢复使用
    # head_tag = soup.new_tag('head')
    # meta1 = soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no'})
    # meta2 = soup.new_tag('meta', attrs={'content': 'text/html', 'charset': 'utf-8', 'http-equiv': 'Content-Type'})
    # title = soup.new_tag('title')
    # head_tag.append(meta1)
    # head_tag.append(meta2)
    # head_tag.append(title)
    # soup.head.replace_with(head_tag)

    # 遍历节点
    for tag in soup.find_all(True):
        # 删除 class
        del tag['class']

        if not tag.get('style') is None:
            tag_style = tag['style']
            del tag['style']  # 删除元素的 style
            del tag['align']  # 删除元素的 align
            # 增加居中样式
            if 'text-align:center' in tag_style:
                tag['style'] = 'text-align:center;'
            # 增加右对齐样式
            elif 'text-align:right' in tag_style:
                tag['style'] = 'text-align:right;'

    # 删除span标签
    spans = soup.find_all('span')
    for span in spans:
        span.unwrap()

    # 删除a标签
    atags = soup.find_all('a')
    for atag in atags:
        atag.unwrap()

    # 删除font标签
    font_tags = soup.find_all('font')
    for font_tag in font_tags:
        font_tag.unwrap()

    # 删除ins标签
    ins_tags = soup.find_all('ins')
    for ins_tag in ins_tags:
        ins_tag.unwrap()

    # 删除i标签
    i_tags = soup.find_all('i')
    for i_tag in i_tags:
        i_tag.unwrap()

    # 删除<o:p>标签
    op_tags = soup.find_all('o:p')
    for op_tag in op_tags:
        op_tag.unwrap()

    # 删除<del>标签及内容
    del_tags = soup.find_all('del')
    for del_tag in del_tags:
        del_tag.decompose()

    # 删除<script>标签及内容
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        script_tag.decompose()

    # 删除<meta>标签及内容
    meta_tags = soup.find_all('meta')
    for meta_tag in meta_tags:
        meta_tag.decompose()

    # 删除<title>标签及内容
    title_tags = soup.find_all('title')
    for title_tag in title_tags:
        title_tag.decompose()

    # 删除注释
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()

    return str(soup).encode().decode('utf-8')


def my_beautiful_soup_after(html):
    soup = BeautifulSoup(html, "html5lib")
    for tag in soup.find_all(True):
        if tag.string is None and len(tag.contents) == 0:
            tag.replace_with('')
    return str(soup).encode().decode('utf-8')


# 保存格式化好的文件
def save_file(res, html_path):
    with codecs.open(html_path, 'w+', 'utf-8') as out:
        out.write(res)
        out.close()

init()