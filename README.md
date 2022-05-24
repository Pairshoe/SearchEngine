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
