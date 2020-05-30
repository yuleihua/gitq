# -*- coding:utf-8 -*-
import os
import sys
import time
import requests
import argparse
import json

try:
    import queue
except ImportError:
    import Queue as queue
import threading
import git

downloadLimit = 65535
downloadPath = os.path.abspath('.')
downloadFile = 'download.txt'
taskQueue = queue.Queue(65536)


# get_repository get github repository, but only top 30
def get_repository(key, types, current_page):
    url = ''
    if types == 0:
        url = "https://api.github.com/search/repositories?q=language:{0}&sort=stars&per_page=200&page={1}".format(key,current_page)
    elif types == 1:
        url = "https://api.github.com/search/repositories?q={0}&sort=stars&per_page=200&page={1}".format(key,current_page)
    elif types == 2:
        url = "https://api.github.com/orgs/{0}/repos?per_page=200&page={1}".format(key, current_page)
    elif types == 3:
        url = "https://api.github.com/users/{0}/repos?per_page=200&page={1}".format(key, current_page)

    r = requests.get(url)
    if r.status_code == 200:
        response_dict = r.json()
        if types == 0 or types == 1:
            repo_dicts = response_dict['items']
            print('repositories total ==> %d' % len(repo_dicts))
            return repo_dicts
        elif types == 2 or types == 3:
            print('repositories total ==> %d' % len(response_dict))
            return response_dict

    return []


def task_repository(repo_dicts):
    count = 0
    for repo_dict in repo_dicts:
        if repo_dict['name'] == 'requests':
            pass
        else:
            names = repo_dict['full_name'].replace("/", "@", 1)
            print("\n")
            print('name ==> ', repo_dict['full_name'])
            print('stars ==> ', repo_dict['stargazers_count'])

            url = repo_dict['clone_url']
            print('repository ==> ', url)
            print('description ==>', repo_dict['description'])
            fetch(names, url)
            count = count + 1
    print('handle count: ', count)


def fetch(name, url):
    line = name + ',' + url + '\n'
    taskQueue.put(line)
    write_file(os.path.join(downloadPath, downloadFile), line)


def write_file(file, content):
    with open(file, mode='a+', encoding='utf-8') as f:
        f.write(content)
        f.flush()


def clone_repo(clone_dir):
    print(clone_dir)

    try:
        if not os.path.exists(clone_dir):
            os.mkdir(clone_dir)
    except Exception:
        print("Error: There is an error in creating directories")

    while not taskQueue.empty():
        line = taskQueue.get()
        print(line)
        content = line.strip().split(',')
        repo_username = content[0]
        url = content[1]

        # try:
        #     if not os.path.exists(os.path.join(clone_dir, repo_username)):
        #         os.mkdir(os.path.join(clone_dir, repo_username))
        # except Exception:
        #     print("Error: There is an error in creating directories")

        fullpath = os.path.join(clone_dir, repo_username)
        print(fullpath)
        try:
            if os.path.exists(os.path.join(fullpath, ".git")):
                git.Repo(fullpath).remote().pull()
            else:
                git.Repo.clone_from(url, fullpath)
        except Exception as e:
            print(e)
            print("Error: There was an error in cloning [{}]".format(url))
        taskQueue.task_done()
        time.sleep(5)




def thread_clone_repos(dir, threads_limit=10):
    threads_state = []
    while taskQueue.empty() is False:
        if threading.active_count() < (threads_limit + 1):
            t = threading.Thread(target=clone_repo, args=(dir,))
            t.daemon = True
            t.start()
        else:
            time.sleep(10)
            threads_state.append(t)
    for _ in threads_state:
        _.join()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--number", type=int, default=150, help="mumber of download limit")
    ap.add_argument("-l", "--lang", help="lang, like go, python, java")
    ap.add_argument("-d", "--directory", help="download directory")
    ap.add_argument("-q", "--query", help="query key")
    ap.add_argument("-u", "--user", help="user name")
    ap.add_argument("-o", "--org", help="org name")
    args = ap.parse_args()

    if args.directory:
        if not os.path.exists(args.directory):
            os.makedirs(args.directory)

    downloadLimit = args.number
    downloadPath = args.directory
    resp = []
    current_page = 1
    count = 0

    if args.lang:
        while len(resp) != 0 or current_page == 1:
            resp = get_repository(args.lang, 0, current_page)
            task_repository(resp)
            thread_clone_repos(downloadPath)
            current_page += 1
            count = count + len(resp)
            if count > downloadLimit:
                break
            time.sleep(1)

    if args.query:
        while len(resp) != 0 or current_page == 1:
            resp = get_repository(args.qurey, 1, current_page)
            task_repository(resp)
            thread_clone_repos(downloadPath)
            current_page += 1
            count = count + len(resp)
            if count > downloadLimit:
                break
            time.sleep(1)

    if args.org:
        while len(resp) != 0 or current_page == 1:
            resp = get_repository(args.org, 2, current_page)
            task_repository(resp)
            thread_clone_repos(downloadPath)
            current_page += 1
            count = count + len(resp)
            if count > downloadLimit:
                break
            time.sleep(1)

    if args.user:
        while len(resp) != 0 or current_page == 1:
            resp = get_repository(args.user, 3, current_page)
            task_repository(resp)
            thread_clone_repos(downloadPath)
            current_page += 1
            count = count + len(resp)
            if count > downloadLimit:
                break
            time.sleep(1)
