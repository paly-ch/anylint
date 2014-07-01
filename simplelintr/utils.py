import hashlib
import json
import docker
import datetime
import subprocess
import os
from giturlparse import parse

def datetimeFromTimestamp(timestamp):
    """ Returns a datetime object from a given timestamp
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def getContainers(all=False, statusCheck=False):
    """ Returns a list of container objects in JSON
    """
    client = docker.Client()
    containers = []

    try:
        containers = client.containers(all=all)
        if not statusCheck:
            for container in containers:
                container['Id'] = container['Id'][:12]
                container['Created'] = datetime.datetime.fromtimestamp(container['Created']).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass

    return containers


def getImages():
    """ Returns a list of image objects in JSON
    """
    client = docker.Client()
    images = []

    try:
        currentImages = client.images()
        for image in currentImages:
            betterImage = {}
            betterImage['Repositories'] = list(set([repo.split(':')[0] for repo in image['RepoTags']]))
            betterImage['Tags'] = [repo.split(':')[1] for repo in image['RepoTags']]
            betterImage['Image'] = image['Id'][:12]
            betterImage['Created'] = datetimeFromTimestamp(image['Created'])
            betterImage['Size'] = "{0:.1f} MB".format(image['VirtualSize'] / 1000.0 / 1000.0)
            images.append(betterImage)
    except Exception:
        pass

    return images

def getGitHash(url):
    p = parse(url)
    u=url
    if p.valid:
        u = "%s:%s/%s" % (p.domain,p.owner,p.repo)
    return hashlib.sha224(u).hexdigest()

def fetchGitThread(gitOptions, socketio):

    tmpdir = '/tmp/lintr/'
    repodir = 'lintr/repos'
    url = gitOptions['url'].strip()
    # (protocol, host, user, pwd, folder, repo) = parseGitUrl(url)
    try:
        urlhash = getGitHash(url)
        newPath = '/tmp/lintr/repo_%s' % urlhash
        print [urlhash,newPath, url]
        if os.path.exists(newPath) & os.path.isdir(newPath):
            cmd = ['git','pull']
            tmpdir = newPath
        else:
            cmd = ['git','clone',url,newPath]
    #        cmd = ['git','clone','--depth','1','-n',url,newPath]
        # cmd = 'git'
        # gitProc = subprocess.Popen(cmd, shell=False)
        print cmd
        gitProc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=tmpdir)

        while True:
            out = gitProc.stdout.readline()
            if out == '' and gitProc.poll() != None:
                break
            if out != '':
                socketio.emit('log', {"log": out, "status": 1})
                print out
        socketio.emit('log', {"log": '', "status": 0})
    except Exception as e:
        socketio.emit('log', {"log": 'ERROR: %s' % e.message, "status": 0})
        print e.message



    # client = docker.Client()
    # buildLog = client.build(path=dockerDirectory,
    #                         tag=tag,
    #                         nocache=nocache,
    #                         rm=rm,
    #                         quiet=quiet,
    #                         stream=True)
    #
    # for line in buildLog:
    #     line = json.loads(line)['stream']
    #     socketio.emit('log', {"log": line})
    #
    # socketio.emit('log', {"log": "\nBuild finished."})


def isDockerRunning():
    """ Returns True if docker is running
    """
    isUp = 0
    client = docker.Client()

    try:
        client.containers(all=all)
        isUp = 1
    except Exception as e:
        if e.message.reason.errno == 13:
            return -1

    return isUp
