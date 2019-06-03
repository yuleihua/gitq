# -*- coding:utf-8 -*-
import os
import time
import requests
import zipfile
import aiohttp
import asyncio
import argparse

downloadLimit = 5
downloadPath = os.path.abspath('.')
unzipFlag = True
downloadFile = 'download.txt'
jobFile = 'job.txt'


# get_repository get github repository, but only top 30
def get_repository(key, types):
    url = ''
    if types == 0:
        url = 'https://api.github.com/search/repositories?q=language:'+key+'&sort=stars'
    elif types == 1:
        url = 'https://api.github.com/search/repositories?q='+key+'&sort=stars&type=Repositories'

    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
        repo_dicts = response_dict['items']
        print('repositories total ==> %d' % len(repo_dicts))
        return repo_dicts
    return []


# get_tags get tag url
def get_tags(name):
    url = 'https://api.github.com/repos/' + name + '/tags'
    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
        if response_dict:
            zip_url = response_dict[0]['zipball_url']
            return zip_url
    return ''


# get_latest get latest url
def get_latest(name):
    url = 'https://api.github.com/repos/' + name + '/releases/latest'
    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
        if response_dict:
            zip_url = response_dict['zipball_url']
            return zip_url
    return ''


def handle_repository(repo_dicts):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_repository(repo_dicts))


def handle_file(files):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task_file(files))


async def task_repository(repo_dicts):
    tasks = []
    count = 0
    for repo_dict in repo_dicts:
        if repo_dict['name'] == 'requests':
            pass
        else:
            names = repo_dict['full_name'].replace("/", "@", 1)
            if not os.path.exists(os.path.join(downloadPath, names + '.zip.ok')):
                print("\n")
                print('name ==> ', repo_dict['full_name'])
                print('stars ==> ', repo_dict['stargazers_count'])

                url = get_latest(repo_dict['full_name'])
                if not url:
                    url = repo_dict['html_url'] + '/archive/master.zip'

                print('repository ==> ', url)
                print('description ==>', repo_dict['description'])
                tasks.append(fetch(names, url, repo_dict['stargazers_count'], False))
                count = count + 1

                if count >= downloadLimit:
                    break

    print('handle count: ', count)
    if tasks:
        await asyncio.wait(tasks)


async def task_file(file):
    infile = open(file, 'r')
    tasks = []
    count = 0
    # 0-1, name, repository, stars,
    for line in infile:
        content = line.strip().split(',')
        if content and content[0] != '0':
            if not os.path.exists(os.path.join(downloadPath, content[1] + '.zip.ok')):
                count = count + 1
                print('\nname ==> ', content[1])
                print('repository ==> ', content[2])
                print('stars ==> ', content[3])
                tasks.append(fetch(content[1], content[2], content[3], True))

    print('handle job file count: ', count)
    if tasks:
        await asyncio.wait(tasks)


def write_file(file, content):
    with open(file, mode='a+', encoding='utf-8') as f:
        f.write(content)
        f.flush()


async def fetch(name, url, stars, file):
    if not file:
        write_file(os.path.join(downloadPath, downloadFile), '1,' + name + ',' + url + ',' + str(stars) + '\n')

    try:
        async with aiohttp.request('GET', url) as resp:
            content = await resp.read()
            with open(os.path.join(downloadPath, name + '.zip'), 'wb') as fd:
                fd.write(content)
    except Exception as e:
        print(e)
        write_file(os.path.join(downloadPath, jobFile), '1,' + name + ',' + url + ',' + str(stars) + '\n')


def unzip():
    file_list = os.listdir(downloadPath)
    for file_name in file_list:
        paths = os.path.splitext(file_name)
        if paths[1] == '.zip':
            try:
                print('\nfile: ', file_name)
                file_zip = zipfile.ZipFile(os.path.join(downloadPath, file_name), 'r')
                for file in file_zip.namelist():
                    out = paths[0].split('@', 1)
                    file_zip.extract(file, os.path.join(downloadPath, out[0]))
                file_zip.close()
                # os.remove(os.path.join(downloadPath, file_name))
                os.rename(os.path.join(downloadPath, file_name), os.path.join(downloadPath, file_name + '.ok'))
            except Exception as e:
                print(e)
                os.remove(os.path.join(downloadPath, file_name))
                recovery_file(os.path.join(downloadPath, downloadFile), paths[0])


def recovery_file(file, name):
    infile = open(file, 'r')
    # 0-1, name, repository, stars,
    for line in infile:
        content = line.strip().split(',')
        if content and content[0] != '0':
            if name == content[1]:
                write_file(os.path.join(downloadPath, jobFile), line)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--number", type=int, help="mumber of download limit")
    ap.add_argument("-l", "--lang", help="lang, like go, python, java")
    ap.add_argument("-d", "--directory", help="download directory")
    ap.add_argument("-q", "--qurey", help="query key")
    args = ap.parse_args()

    downloadLimit = args.number
    if downloadLimit > 30:
        downloadLimit = 30

    if args.directory:
        if not os.path.exists(args.directory):
            os.makedirs(args.directory)

    downloadPath = args.directory

    job = os.path.join(downloadPath, jobFile)
    if os.path.exists(job):
        new = job + time.strftime('%Y%m%d%H%M%S', time.localtime())
        os.rename(job, new)
        handle_file(new)
        os.remove(new)

    if args.lang:
        dicts = get_repository(args.lang, 0)
        handle_repository(dicts)

    if args.qurey:
        dicts = get_repository(args.qurey, 1)
        handle_repository(dicts)

    if unzipFlag:
        unzip()
