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
articles=[]
dirs = os.listdir(ARTICLE_LOCATION)
for ARTICLE_DIR in dirs:
    # 在文章的根目录下寻找发表的文集名目录
    NAME_ARR=os.listdir('%s/%s'%(ARTICLE_LOCATION,ARTICLE_DIR))
    for name in NAME_ARR:
        # 文件名包含“简介”或者“目录”二字，不是鲁迅作
        if '简介' not in name and '目录' not in name:
            articles.append('%s/%s/%s'%(ARTICLE_LOCATION,ARTICLE_DIR,name))
print('文章数量有：%d篇'%len(articles))

# 代码快速实现参考：https://cloud.tencent.com/developer/article/1374967

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

if not os.path.exists(ix_path):
    os.mkdir(ix_path)
ix = create_in(ix_path, schema,indexname=ix_name)
ix.close()

from whoosh.filedb.filestore import FileStorage
import re

# Replace pattern
rpp=re.compile('[\u3000※·\n\r〔〕 ]')

storage = FileStorage(ix_path)  #idx_path 为索引路径
ix = storage.open_index(indexname=ix_name)
# 按照schema定义信息，增加需要建立索引的文档
# 注意：字符串格式需要为unicode格式
with ix.writer() as w:
    for article in articles:
        with open(article,'r',encoding='utf-8') as f:
            arr=f.read()
        subs=re.split(rpp,arr)
        art=''.join(subs)
        length=len(art)
        ind=art[::-1].find('〔１〕')
        if ind>0:
            art=art[:length-ind-1]
            art=re.split('[\d]',art)
            art=''.join(art[1:])
        name_arr=article.split('/')
        w.add_document(title='集名：%s 篇名：%s'%(name_arr[1],name_arr[-1][:-3]),content=art)
        print("已引入文章：%s"%article)
        
ix.close()
print("索引已建立好")