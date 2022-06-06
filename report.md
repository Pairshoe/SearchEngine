# <center>搜索引擎实验报告</center>
<center>王拓为 2018011917  罗富文 2019011409</center>

## 1. 问题描述
本作业要求实现司法搜索引擎。

本搜索引擎共索引约 68000 条数据，每条数据均为一个司法判例，包含案号、时间、法官、法院和文本等内容。用户在搜索框输入关键词或文本后，展示搜索结果。

## 2. 实现模块
### 2.1. 搜索库 Elastic Search 的使用
Elastic Search 是用 Java 语言编写的搜索引擎库，功能丰富且性能好。该库可以采用网络请求的形式进行交互，且提供了 Python 库对网络请求进行封装。本项目主要由 Python 语言编写，采用了上述与 Elastic Search 库的交互形式。

### 2.2. 数据导入模块
运行搜索引擎前，首先需要导入数据。本次实验每条数据均为一个 `xml` 文件，我们用 `Beautiful Soup` 库识别 `xml` 标签，并提取案号、立案时间、适用法律、适用法条、相关罪名、法官、法院、文档类型和判决书文本等相关信息，导入 Elastic Search 数据库中。除立案时间以整数形式保存外，其余字段均以字符串形式保存。

### 2.3. 搜索模块
搜索模块主要调用 Elastic Search 库完成。根据任务需求和 Elastic Search 特点，本模块主要对外提供 3 个接口。

#### 2.3.1. 查询接口
接口形式如下。

```python
def make_query(self, content: str, accurate_mode: bool = False, case_mode: bool = False, conditions: dict = dict(), sort_key: str = '')
```

该方法用于描述一次查询，无返回值。其中 `accurate_mode` 和 `case_mode` 参数控制搜索模式； `conditions` 参数控制高级搜索，描述额外的搜索条件； `sort_key` 参数控制排序。关于这些功能的详细介绍可参考 `关键功能` 模块。

#### 2.3.2. 搜索接口
接口形式如下。

```python
def search_case(self, page: int)
```

该方法用于获取查询结果，返回结果列表。调用本函数前需要先调用 `make_query` 函数。

#### 2.3.3. 详细内容接口
接口形式如下。

```python
def get_case(self, id: str)
```

该方法用于获取关于案例的详细信息和相关案例推荐，返回包含结果内容的字典。其中输入的 `id` 为数据的唯一标识符而非案号。相关案例推荐详见 `关键功能` 模块。

### 2.4. 前端展示模块

## 3. 关键功能
### 3.1. 搜索功能
我们共提供 3 种不同的功能，分别是普通关键词检索、高级检索和案例检索，下面对他们进行逐一介绍。
 - 普通关键词检索：用 `jieba` 库的搜索引擎模式对输入内容进行分词，以分词后的词为单位进行严格匹配，要求结果与关键词匹配度不低于 85% 。
 - 高级检索：输入时以空格分隔关键词，不对关键词进行分词，对每个关键词进行严格匹配，要求结果与所有关键词匹配。除此以外，高级搜索支持以案号、时间、相关法律、法官等作为关键字进行检索。

### 3.2. 结果高亮与标签显示

### 3.3. 搜索结果排序

### 3.4. 相似案例推荐

### 3.5. 司法判决书结构化展示

## 4. 测试结果和样例分析

## 5. 参考资料
 - Elastic Search 简体中文教程： https://www.elastic.co/guide/cn/index.html ；
 - Python Elastic Search 文档： https://elasticsearch-py.readthedocs.io/en/v8.2.2/ ；
 - Django 文档： https://docs.djangoproject.com/zh-hans/4.0/ 。
