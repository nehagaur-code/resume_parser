#!/usr/bin/python3
import os
import sys
import textract
import pathlib
import shlex
import json

class MyEncoder(json.JSONEncoder):
  def default(self, o):  
    if type(o) is bytes:
      return o.decode("latin-1")
    return super(MyEncoder, self).default(o)
      

rootdir = sys.argv[1]
def ReadData(filepath):
  text="NOT FOUND"
  try:
    with open(filepath, 'r') as source:
      text = source.read()
  except Exception as e:
    print("Parse {} exception {}".format(filepath,e))
  return text


inpath = str(pathlib.Path(rootdir).parent)
opath = inpath + "/ANALYSIS/"
if not os.path.exists(opath):
  os.mkdir(opath)

resdict = {}
print(rootdir)
for folder, subs, files in os.walk(rootdir):
  for filename in files:
    #print(filename)
    #opath2 = opath + pathlib.Path(folder).stemcd 
    #print(opath2)
    #print(filename)
    filepath=os.path.join(folder, filename)
    text=ReadData(filepath=filepath)
    resdictItem = {
        "RESUME_PATH": filepath,
        "RESUME_TYPE": pathlib.Path(folder).stem, 
        "RESUME_NAME" : filename,
        "RESUME_TEXT" : text
     }
    resdict[filepath] = resdictItem
    #break
#json_string=json.dumps(resdict, indent=2)   
#jsData = json.loads(json_string)
#print(json.dumps(resdictItem, ensure_ascii=False))
with open(opath + "/ALLRES.json", "w" ) as OJSON:
  OJSON.write( json.dumps(resdictItem,indent=1))
  
