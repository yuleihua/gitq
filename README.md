# gitq

Tools to query github project and download them.

下载github上项目到本地的工具，主要用python编写。



### **1. gitzip.py** 

Downloading  github project as zip file

查询github项目信息，并取最新的tag，如没有取master最新版本并下载到本地。

```
[ifts@localhost gitq]$ python3 gitzip.py  --help
usage: gitzip.py [-h] [-n NUMBER] [-l LANG] [-d DIRECTORY] [-q QUREY] [-f]
                 [-u USER] [-o ORG]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        mumber of download limit     ##下载数量限制
  -l LANG, --lang LANG  lang, like go, python, java  ##按照编程语查找并下载
  -d DIRECTORY, --directory DIRECTORY  
                        download directory
  -q QUREY, --qurey QUREY
                        query key                    ##关键词并查找并下载
  -f, --fetch           fetch lastest code from downloadFile
  -u USER, --user USER  user name                    ##某用户下所有仓库下载
  -o ORG, --org ORG     org name                     ##某组织机构下所有仓库下载

```

### **2. gitclone.py** 

Downloading  github project as git clone directory

使用git插件clone github 项目到本地。

```
[ifts@localhost gitq]$ python3 gitclone.py  --help
usage: gitclone.py [-h] [-n NUMBER] [-l LANG] [-d DIRECTORY] [-q QUERY]
                   [-u USER] [-o ORG]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        mumber of download limit  ##下载数量限制
  -l LANG, --lang LANG  lang, like go, python, java  ##按照编程语查找并clone
  -d DIRECTORY, --directory DIRECTORY
                        download directory
  -q QUERY, --query QUERY
                        query key     ##关键词查找并clone
  -u USER, --user USER  user name     ##某用户下所有仓库clone
  -o ORG, --org ORG     org name      ##某组织机构下所有仓库clone


```

