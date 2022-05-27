# 搜索引擎课程大作业
## 依赖及安装方法
- python3 库
```sh
pip install bs4
pip install elasticsearch
pip install django
```
- java jdk
- Elastic Search
```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.2.0-linux-x86_64.tar.gz
tar -xvf elasticsearch-8.2.0-linux-x86_64.tar.gz
mv elasticsearch-8.2.0 elasticsearch
cd elasticsearch/bin/
./elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.2.0/elasticsearch-analysis-ik-8.2.0.zip
./elasticsearch
# 首次运行后需修改 config/elasticsearch.yml 中 xpack.security.enabled 为 false
```

## 数据预处理
在本目录下新建 `raw_data` 文件夹，把所有 `xml` 文件置于 `raw_data` 文件夹下，然后运行如下命令。
```sh
python3 data_preprocess.py
```

## 数据返回格式
 - search_case() ：列表，每项包含如下内容
    - id ：案件在搜索引擎中的编号
    - case_id ：案号
    - filing_time ：立案年份， 0 表示无该项
    - law ：与该案件相关的法律
    - law_detailed ：与该案件相关的法条
    - crime ：与该案件相关的罪名
    - judge ：法官
    - court ：法院
    - document_type ：文档类型，如刑事判决书、民事判决书等
    - browse_count ：浏览次数
    - highlight ：列表，高亮显示

 - get_case() ：包含如下内容
    - title ：标题，通常形式为“ xx 法院 xx 判决书”
    - meta ：元数据
       - case_id ：案号
       - filing_time ：立案年份， 0 表示无该项
       - law ：与该案件相关的法律
       - law_detailed ：与该案件相关的法条
       - crime ：与该案件相关的罪名
       - judge ：法官
       - court ：法院
       - document_type ：文档类型，如刑事判决书、民事判决书等
       - browse_count ：浏览次数
    - content ：内容
       - header ：列表，原告被告等
       - body ：列表，内容
       - judge ：列表，法官
       - time ：判决日期
       - secretary ：列表，书记员
       - laws ：列表，与本案相关的法律
    - recommends ：列表，内容相似案件，每项包含如下内容
       - id ：案件在搜索引擎中的编号
       - case_id ：案号
       - filing_time ：立案年份， 0 表示无该项
       - law ：与该案件相关的法律
       - law_detailed ：与该案件相关的法条
       - crime ：与该案件相关的罪名
       - judge ：法官
       - court ：法院
       - document_type ：文档类型，如刑事判决书、民事判决书等
       - browse_count ：浏览次数
       - content_abstract ：内容摘要，已截去过长的部分
    - recommends_judge ：列表，同法官案件，每项结构同上
    - recommends_law ：列表，同法律案件，每项结构同上
