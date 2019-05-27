# -*- coding:utf-8 -*-
import os
import requests
import zipfile
import aiohttp
import asyncio
import argparse

downloadLimit = 5
downloadPath = os.path.abspath('.')
uzipFlag = True

# only top 30
def getDicts(key, types):
    # key is lang or word
    url = ''
    if types == 0:
        url = "https://api.github.com/search/repositories?q=language:"+key+"&sort=stars"
    elif types == 1:
        url = "https://api.github.com/search/repositories?q="+key+"&s=stars&type=Repositories"

    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
        repo_dicts = response_dict['items']
        print("Repositories total ==> %d\n" % len(repo_dicts))
        return repo_dicts

    return []


def handleDicts(repo_dicts):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(taskmain(repo_dicts))

async def taskmain(repo_dicts):
    tasks = []
    count = 0
    for repo_dict in repo_dicts:
        if repo_dict['name'] == 'requests':
            pass
        else:
            item = repo_dict['html_url'] + '/archive/master.zip'
            if not os.path.exists(os.path.join(downloadPath, repo_dict['name'] + repo_dict['node_id'] + '.zip')):
                print("\n")
                print('Name ==> ', repo_dict['full_name'])
                print('Stars ==> ', repo_dict['stargazers_count'])
                print('Repository ==> ', repo_dict['html_url'])
                print('Description ==>', repo_dict['description'])
                [tasks.append(fetch(repo_dict['name'] + repo_dict['node_id'], item))]
                count = count +1

                if count >= downloadLimit:
                    break

    print('handle count', count)
    await asyncio.wait(tasks)


async def fetch(name, url):
    print('download ' + name + ' url ' + url)
    async with aiohttp.request('GET', url) as resp:
        # content = await resp.read()
        print(name)
        content = await resp.read()
        with open(os.path.join(downloadPath, name + '.zip'), 'wb') as fd:
            fd.write(content)

        # chunk_size = 81920
        # with open(name+'.zip', 'wb') as fd:
        #     while True:
        #         chunk = await resp.content.read(chunk_size)
        #         if not chunk:
        #             break
        #         fd.write(chunk)


def unzip():
    file_list = os.listdir(downloadPath)
    for file_name in file_list:
        print("file: ",file_name)
        if os.path.splitext(file_name)[1] == '.zip':
            try:
                file_zip = zipfile.ZipFile(os.path.join(downloadPath, file_name), 'r')
                for file in file_zip.namelist():
                    file_zip.extract(file, downloadPath)
                file_zip.close()
                os.remove(os.path.join(downloadPath, file_name))
            except:
                continue

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

    if args.lang:
        dicts = getDicts(args.lang, 0)
        handleDicts(dicts)

    if args.qurey:
        dicts = getDicts(args.qurey, 1)
        handleDicts(dicts)

    if uzipFlag:
        unzip()
