# gitq

A tool to query github project by language and key word, then download them.

```
python3  gitq.py  --help
usage: gitq.py [-h] [-n NUMBER] [-l LANG] [-d DIRECTORY] [-q QUREY]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        mumber of download limit
  -l LANG, --lang LANG  lang, like go, python, java
  -d DIRECTORY, --directory DIRECTORY
                        download directory
  -q QUREY, --qurey QUREY
                        query key
```

### download by lang 

```
$ python3 gitq.py -n 1 -l python  -d /tmp/python
Repositories total ==> 30



Name ==>  vinta/awesome-python
Stars ==>  67827
Repository ==>  https://github.com/vinta/awesome-python
Description ==> A curated list of awesome Python frameworks, libraries, software and resources
handle count 1
download awesome-pythonMDEwOlJlcG9zaXRvcnkyMTI4OTExMA== url https://github.com/vinta/awesome-python/archive/master.zip
awesome-pythonMDEwOlJlcG9zaXRvcnkyMTI4OTExMA==
file:  awesome-pythonMDEwOlJlcG9zaXRvcnkyMTI4OTExMA==.zip

$ ls /tmp/python
awesome-python-master

```

### download by key word

```
$ python3 gitq.py -n 1 -l nginx  -d /tmp/nginx
Repositories total ==> 30



Name ==>  perusio/drupal-with-nginx
Stars ==>  866
Repository ==>  https://github.com/perusio/drupal-with-nginx
Description ==> Running Drupal using nginx: an idiosyncratically crafted bleeding edge configuration.
handle count 1
download drupal-with-nginxMDEwOlJlcG9zaXRvcnk4NTg4NzA= url https://github.com/perusio/drupal-with-nginx/archive/master.zip
drupal-with-nginxMDEwOlJlcG9zaXRvcnk4NTg4NzA=
file:  drupal-with-nginxMDEwOlJlcG9zaXRvcnk4NTg4NzA=.zip

$ ls /tmp/nginx
drupal-with-nginx-master

```