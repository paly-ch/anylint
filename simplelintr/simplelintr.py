__author__ = 'pl'

# import threading

from flask import Flask, jsonify

from flask.ext.mako import MakoTemplates, render_template
from flask.ext.socketio import SocketIO
from utils import getContainers, getImages, isDockerRunning, fetchGitThread

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.template_folder = "templates"

mako = MakoTemplates(app)
socketio = SocketIO(app)


@socketio.on('connect')
@socketio.on('connected')
def connected(event):
    print("SimpleLintr connected")


@socketio.on('fetchgit')
def fetchGit(gitOptions):
    """ Build a new docker image
    """
    gitUrl = gitOptions['url']
    socketio.emit('log', {"log": "Started cloning from %s" % gitUrl, "status": 1})
    # threading.Thread(target=fetchGitThread, args=(gitOptions, socketio)).start()
    fetchGitThread(gitOptions, socketio)
    print("Build running")

#
# @app.route('/images')
# def images():
#     """ View for docker images
#     """
#     images = {"images": getImages()}
#     return jsonify(images)
#
#
# @app.route('/containers')
# def containers():
#     """ View for docker containers
#     """
#     containers = {"containers": getContainers(all=True)}
#     return jsonify(containers)


@app.route('/status')
def status():
    """ Gets the status of docker.
    """
    isUp = isDockerRunning()
    status = "Running" if isUp == 1 else "Stopped" if isUp == 0 else "Error"
    statusColour = "green" if isUp ==1 else "orange" if isUp == 0  else "red"

    return jsonify({"status": status, "colour": statusColour})

@app.route('/')
def index():
    """ Homepage
    """
    return render_template('index.mako')


if __name__ == '__main__':
    socketio.run(app)


