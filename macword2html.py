# -*- coding: utf-8 -*-
import codecs
import os
import shutil
from pydocx import PyDocX
import re
from bs4 import BeautifulSoup, Comment
from pydocx.export import PyDocXHTMLExporter
from pydocx.export.numbering_span import BaseNumberingSpanBuilder


class CustomExporter(PyDocXHTMLExporter):
    numbering_span_builder_class = BaseNumberingSpanBuilder


def init():
    path = os.getcwd()  # 文件夹目录
    word_path = os.path.join(path, 'word')
    files = os.listdir(word_path)  # 得到文件夹下的所有文件名称
    html_dir = os.path.join(path, 'html')
    # 如果目录存在，直接删除
    if os.path.exists(html_dir):
        shutil.rmtree(html_dir)

    os.mkdir(html_dir)
    for file in files:  # 遍历文件夹
        file_split = file.split('.')
        # os.path.isfile 需要传入文件的绝对路径
        if (os.path.isfile(os.path.join(word_path, file))) and (
                file_split[len(file_split) - 1] == 'doc' or file_split[len(file_split) - 1] == 'docx'):
            main(word_path, html_dir, file)


def main(word_dir, html_dir, word_name):
    word_name_split = word_name.split('.')
    word_name_split.pop()
    html_name = '.'.join(word_name_split) + '.html'
    html = word_to_html(os.path.join(word_dir, word_name), os.path.join(html_dir, html_name))
    html = format_html(html)
    html = my_beautiful_soup(html)
    html = re.sub(r'\s+', r' ', html)  # 多个空格合并成一个 nbsp;被删除问题

    html = re.sub(r'<p>\s*?(\S*?)\s*?</p>', r'<p>\1</p>', html)  # 删除p元素首尾空格
    html = re.sub(r'<strong>\s*?(\S*?)\s*?</strong>', r'<strong>\1</strong>', html)  # 删除strong元素首尾空格
    # 在我们的需求里，只需要body内的内容，所以这样；不是这样的情况下，应该去掉这句
    html = re.sub(r'(.*?)<body(.*?)>(.*)<\/body>(.*)', r'<!-- () -->\3', html, flags=re.S)
    html = format_html1(html)
    html = format_html1(html)
    save_file(html, os.path.join(html_dir, html_name))


# doc_path - word 文档地址 export_path - 导出的 html 地址
def word_to_html(doc_path, export_path):
    # html = PyDocX.to_html(doc_path)
    print(CustomExporter.numbering_span_builder_class)
    exporter = CustomExporter(doc_path)
    html = exporter.export()
    return html
    # f = open(export_path, 'w', encoding="utf-8")
    # f.write(html)
    # f.close()
    # fr = open(export_path, 'r')
    # str = fr.read()
    # fr.close()
    # return str


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


def my_beautiful_soup(html):
    soup = BeautifulSoup(html, "html5lib")

    # 遍历节点
    for tag in soup.find_all(True):
        # if not tag.get('style') is None:
        #     tag_style = tag['style']
        #     del tag['style']  # 删除元素的 style
        #     del tag['align']  # 删除元素的 align
        #     # 增加居中样式
        #     if 'text-align:center' in tag_style:
        #         tag['style'] = 'text-align:center;'
        #     # 增加右对齐样式
        #     elif 'text-align:right' in tag_style:
        #         tag['style'] = 'text-align:right;'
        if not tag.get('class') is None:
            tag_class = tag['class']
            # 删除 class
            del tag['class']
            # 增加居中样式
            if 'pydocx-center' in tag_class:
                tag['style'] = 'text-align:center;'
            elif 'pydocx-right' in tag_class:
                tag['style'] = 'text-align:right;'

    # 删除span标签
    spans = soup.find_all('span')
    for span in spans:
        if (not span.get('style') is None) and (span.parent is not None):
            span.parent['style'] = span['style']
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

    # 删除注释
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()

    return str(soup).encode().decode('utf-8')


# 保存格式化好的文件
def save_file(res, html_path):
    with codecs.open(html_path, 'w+', 'utf-8') as out:
        out.write(res)
        out.close()


init()
