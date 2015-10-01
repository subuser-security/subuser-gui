import tempfile
import os
import inspect

try:
  subuserExecutable = os.environ["SUBUSER_EXECUTABLE"]
except KeyError:
  subuserExecutable = "subuser"

sourceDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

icons = {"subuser-logo":"data/subuser.png"
         ,"subuser":"data/vibrant-icons/subuser.svg"
         ,"repository":"data/vibrant-icons/repository.svg"
         ,"image-source":"data/vibrant-icons/image-source.png"}
for name,path in icons.items():
  icons[name] = os.path.join(sourceDir,path)
