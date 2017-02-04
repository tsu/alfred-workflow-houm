# encoding: utf-8

import sys
from workflow import Workflow
from socketIO_client import SocketIO, LoggingNamespace

def main(wf):
  sitekey = wf.get_password('apikey')
  sceneId = wf.args[0]
  activateScene(sitekey, sceneId)

def activateScene(siteKey, sceneId):
   with SocketIO('houmi.herokuapp.com', 80, LoggingNamespace) as socketIO:
     socketIO.emit('clientReady', {'siteKey': siteKey})
     socketIO.emit('apply/scene', sceneId)

if __name__ == u"__main__":
  wf = Workflow()
  sys.exit(wf.run(main))
