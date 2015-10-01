#external modules
import os
import time
import json
#internal moduels
from paths import *

def execute(subuserSubCommand,cwd=None,env=None,stdin=None,stdout=None,stderr=None):
  job = {}
  job["command"]=[subuserExecutable]+subuserSubCommand
  if cwd:
    job["cwd"]=cwd
  if env:
    job["env"]=env
  if stdin:
    job["stdin"] = stdin
  if stdout:
    job["stdout"] = stdout
  if stderr:
    job["stderr"] = stderr
  with open("/subuser/execute/spool","a") as execute:
    execute.write(json.dumps(job)+"\n")

def executeGetJson(subuserSubCommand,cwd=None):
  outputFilePath = "/subuser/execute/output"
  outputFilePathOnHost = "./output"
  execute(subuserSubCommand,cwd=cwd,stdout=outputFilePathOnHost)
  while not os.path.exists(outputFilePath):
    time.sleep(0.001)
  contents = ""
  with open(outputFilePath,"r") as outputFile:
    while True:
      try:
        contents += outputFile.read()
        dictionary = json.loads(contents)
        break
      except ValueError:
        pass
  os.remove(outputFilePath)
  return dictionary
