'''
Articles of Lu'Xun Search Program
By Ginchung@Github
On May 8th, 2019@Hefei

转载请标明出处：本Notebook使用MIT许可(MIT License)

Dependencies：
Python3 Platform
Whoosh (检索)
Jieba (用于分词)
Ac-heron Depo: luxun  鲁迅文集相关资料

Welcome STARS ME!
'''

#coding='utf-8'
# 文章保存的根目录
ARTICLE_LOCATION = 'article'


import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 创建schema, stored为True表示能够被检索
schema = Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=False),content=TEXT(stored=True, analyzer=analyzer))

# 存储schema信息至'indexdir'目录下
ix_path = 'indexdir/'
ix_name = 'luxun_index_name'

from IPython.core.display import display, HTML

import whoosh
from whoosh.filedb.filestore import FileStorage
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer

storage = FileStorage(ix_path)  #idx_path 为索引路径

with storage.open_index(indexname=ix_name).searcher() as searcher:
    # 检索标题中出现'文档'的文档
    results = searcher.find("content",input("请输入你要检索的文字："))
    # 检索出来的第一个结果，数据格式为dict{'title':.., 'content':...}
    for r in results:
        print('文章：%s'%r.get('title'))
        print('文字：%s'%r.get("content")) 
        # 高亮标题中的检索词
        print('相似度评分：%.2f'%r.score)  
        # 准确度分数
        print('文章序号：%d'%r.docnum)
        
        doc = r.fields()
        jsondoc = json.dumps(doc, ensure_ascii=False)
        # display(jsondoc)  
        # 打印出检索出的文档全部内容
