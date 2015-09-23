#external modules
import os
import time
import json
#internal moduels
from paths import *

def execute(subuserSubCommand):
  with open("/subuser/execute","a") as execute:
    execute.write(subuserExecutable+" "+subuserSubCommand+"\n")

def executeGetJson(subuserSubCommand):
  outputFilePath = os.path.join(communicationsDir,"output")
  outputFilePathOnHost = os.path.join(communicationsDirOnHost,"output")
  with open("/subuser/execute","a") as execute:
    execute.write(subuserExecutable+" "+subuserSubCommand+" >> "+outputFilePathOnHost+"\n")
  while not os.path.exists(outputFilePath):
    time.sleep(0.01)
  contents = ""
  with open(outputFilePath,"r+") as outputFile:
    while True:
      try:
        contents += outputFile.read()
        dictionary = json.loads(contents)
        break
      except ValueError:
        pass
  os.remove(outputFilePath)
  return dictionary
