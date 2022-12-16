# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:08:00 2018

@author: anandrathi
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 13 22:14:40 2018

@author: anandrathi
"""
import pandas as pd
import re
import numpy as np
import json
import nltk
import MainHeaders

#xpath = "D:/Users/anandrathi/Documents/personal/Bussiness/Aleep/"
xpath = "C:/temp/DataScience/Aleep/GIT/RESUMEParse/"

nltk.download('punkt')


import logging
logging.basicConfig(
    handlers=[logging.FileHandler(xpath + '/log.log', 'w', 'utf-8')],
    format='%(levelname)s: %(message)s',
    level=logging.WARNING #CRITICAL ERROR WARNING  INFO    DEBUG    NOTSET 
)

EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+'
NO_NAME = set(["phone","resume", "vitae" , "of", "curriculum", "curriculam"," carriculum", "curriculum-vitae",
              "profile", "email", "gmail", "com", "yahoo" , "vitae", "mail", "area", "experties", "telecommunication"
               "electronics",   "tele munication", "engineer" , "with",
               "yrs", "experience", "exp", "_", "engineer", "name", "career",
               "vision", "btech", "apartment", "analyst",
                'databae', 'developer',  'adminisrator', "release" "years" "contact", "details"
                 "objectives", "achieving", "challenging", "position", "field",
                 "database", "best", "knowledge", "creative", ",mind", ",synergistic", "whole", "strive",
                 ",excellence" ,"highest", "echelons", "technical", "level",
                  "professional", "summary","pic", "b tech"
               ,"\t"])
len(NO_NAME)

PAT = re.compile(EMAIL_PATTERN)

resdfInit = pd.read_json(xpath + "ALLRES.json", orient='records')
list(resdfInit.columns)
resdfInit.head(1).index


##################################################################
###################### empty Resume ############################
##################################################################
EmpryResumeJSON = None
with open(xpath + "RESUME_JSON_EMPTY.json") as RM:
  try:
    EmpryResumeJSON =  json.load( RM )
  except Exception as e:
    logging.debug(" load ResumeJSON {} ".format(e))

def GetHeadingsSets():
  from itertools import chain
  Headings=MainHeaders.getMainHeaders()
  HList =  [ htokl.split(",") for htokl in  list(Headings)  ]
  HList =  [ Hitem.strip().lower() for Hitem in list(chain(*HList)) if Hitem.strip().lower() !="" ]
  return set( HList[:] )

#from nameparser.parser import HumanName

HeadSet = GetHeadingsSets()
type(HeadSet)

HeadSet

"project" in HeadSet


textSer = resdfInit['RESUME_TEXT']

def GetAvgLineDetails(textSer, avgHeaderWords,  avgHeaderLen):
  rlines=[]
  for item in textSer.iteritems():
    rlines.extend(item[1].splitlines() )

  avgWordLen = np.mean([ len(rline) for rline in rlines if len(rline.strip())>avgHeaderWords ])
  stdWordLen = np.std([ len(rline) for  rline in rlines if len(rline.strip())>avgHeaderWords ])
  avgWordCount = np.mean([ len(rline.split()) for  rline in rlines if len(rline.strip())>avgHeaderLen ])
  stdWordCount = np.std([ len(rline.split()) for  rline in rlines if len(rline.strip())>avgHeaderLen ])
  return avgWordLen,stdWordLen ,avgWordCount, stdWordCount



def CreateAllHeadRegExp(HeadSet):
  regList = []
  for h in HeadSet:
    HeadExtraxtRe = re.compile(h, flags= re.I)
    regList.append(HeadExtraxtRe)
  return regList

def MatchRegExp(text, cregs,  ):
  matchcount = 0
  for hr in cregs:
    m = hr.match( text)
    if m:
      matchcount += 1
  return matchcount

def CreateHeadRegExp(HeadSet):
  HeadExtraxtRegStr = r"(" + r"|".join(HeadSet) +   r")[: ]*" + r"(.*?)" + r"(" + r"|".join(HeadSet) +   r")"
  HeadExtraxtRe = re.compile(HeadExtraxtRegStr, flags= re.I | re.DOTALL )
  return HeadExtraxtRe



from scipy import stats
np.random.seed(7654567)


def HeaderStats(line,
                avgWordCount,
                rvsWord,
                rvsHeader,
                rvsWordLen,
                rvsHeaderLen ):
   isHeader=0
   words = line.split()
   wcnt = len(words)
   pval = stats.ttest_1samp(rvsWord, wcnt)
   if abs(pval.pvalue) < 0.05:
     if wcnt< avgWordCount:
       isHeader+=1
       if False:
         logging.debug("This is header rvsWord test :{} pval={} wcnt={}".format(isHeader,
             abs(pval.pvalue), wcnt))
   wpval = stats.ttest_1samp(rvsHeader, wcnt)
   if abs(wpval.pvalue) > 0.05:
     isHeader+=1
     if False:
       logging.debug("This is header rvsHeader test :{} pval={} wcnt={}".format(isHeader,
           abs(wpval.pvalue), wcnt))

   pval = stats.ttest_1samp(rvsWordLen, len(line))
   if abs(pval.pvalue) < 0.05 :
     if(len(line)< avgWordLen):
       isHeader+=1
       if False:
         logging.debug("This is header rvsWordLen test :{} pval={}  len(line)={}".format(isHeader,
           abs(pval.pvalue), len(line) ) )
   wpval = stats.ttest_1samp(rvsHeaderLen, len(line))
   if abs(wpval.pvalue) > 0.05:
     isHeader+=1
     if False:
       logging.debug("This is header rvsHeaderLen test :{} pval={}  len(line)={}".format(isHeader, abs(wpval.pvalue), len(line) ) )
   return isHeader



import MainHeaders
oldHeaders  = list(set(MainHeaders.getMainHeaders()) - set("co") )
oldHeaders = sorted(oldHeaders, key=lambda x: (-len(x), x) )
oldHeaders = [ h.replace("(", r"\(" ).replace(")", r"\)" )  for h in oldHeaders ]
"challenges" in set(oldHeaders)
"objective" in set(oldHeaders)


HeadMatchpattern=r"\s*" + r"?("  + "|".join(oldHeaders) + r")[:\.-\t\n]+"
HeadSplitpattern=r"\s*" + r"?("  + "|".join(oldHeaders) + r")\s*[:-\\t]+\s*"
hregall =  CreateAllHeadRegExp(oldHeaders)

antiHeaders = MainHeaders.getAntiHeaders()
AntiHeadMatchpattern=r"\s*" + r"?("  + "|".join(antiHeaders) + r")"




avgHeaderLen = np.mean([ len(head) for  head in oldHeaders if len(head.strip())>0 ])
stdHeaderLen = np.std([ len(head) for  head in oldHeaders if len(head.strip())>0 ])
avgHeaderWords = np.mean([ len(head.split()) for  head in oldHeaders if len(head.strip())>0 ])
stdHeaderWords = np.std([ len(head.split()) for  head in oldHeaders if len(head.strip())>0 ])

AllresumesPara=[]

if False:
  avgWordLen,stdWordLen ,avgWordCount, stdWordCount = GetAvgLineDetails(textSer=textSer, avgHeaderWords=avgHeaderWords, avgHeaderLen=stdHeaderLen)
else:
  avgWordLen,stdWordLen ,avgWordCount, stdWordCount = (56.257, 57.566, 7.79, 8.369)

rvsWord = stats.norm.rvs(loc=avgWordCount, scale=stdWordCount, size=(50))
rvsHeader = stats.norm.rvs(loc=avgHeaderWords, scale=stdHeaderWords, size=(50))
rvsWordLen = stats.norm.rvs(loc=avgWordLen, scale=stdWordLen, size=(50))
rvsHeaderLen = stats.norm.rvs(loc=avgHeaderLen, scale=stdHeaderLen, size=(50))

from collections import Counter

MYDEBUG=False
#Word Frequncy
#Heads per line
#Head List Order
#Head new lines
from nltk import word_tokenize
def FindHeadersInSingleLine(line):
  HeaderStack=[]
  parasDict=[]
  ParaLines=[]
  m = re.findall(HeadSplitpattern,  line)
  if len(m)>1:
    witerator = iter(line.split())
    for word in witerator:
      if re.match(HeadSplitpattern, word, flags=re.IGNORECASE) and (not re.match(AntiHeadMatchpattern, word, flags=re.IGNORECASE)) :
        if MYDEBUG:
          logging.debug("FindHeadersInSingleLine::HeadSplitpattern {}".format(word))
        if len(HeaderStack) >0:
          lastHeader=HeaderStack.pop()
        if len(ParaLines) >0:
          if MYDEBUG:
            logging.debug("FindHeadersInSingleLine::ParaLines {}".format(ParaLines))
          parasDict.append({ lastHeader : " ".join(ParaLines)})
          lastHeader=""
          ParaLines=[]
        HeaderStack.append(word )
      elif len(HeaderStack) >0:
        ParaLines.append( word )
        if MYDEBUG:
          logging.debug("FindHeadersInSingleLine::ParaLines.append {}".format(word))
    if len(HeaderStack) >0 :
      ParaLines.append( word )
      lastHeader=HeaderStack.pop()
      parasDict.append({ lastHeader : " ".join(ParaLines)})

  if len(parasDict) >0:
    return  parasDict
  else:
    return None

def SplitHeader(hline):
  header = re.split(r':|:-|:--|\n|\t',hline)
  return header[0], " ".join(header[1:])


res1 = resdfInit['RESUME_TEXT'].loc[18]
#logging.debug(res1)

import ResumeMapper
revHash = ResumeMapper.getRevKeyHash(xpath=xpath)
#ORes = ResumeMapper.GetEmptyRes(xpath=xpath)
#logging.debug("Init ORes = {} ".format(ORes))

import FillResume

def FFillResume(resDict, revHash, ORes, logging):
  #ORes["basics"]=None
  ORes["profiles"]=[]
  ORes["work experience"]=[]
  ORes["references"]=[]
  ORes["volunteer"]=[]
  ORes["education"]=[]
  ORes["awards"]=[]
  ORes["publications"]=[]
  ORes["languages"]=[]
  ORes["references"]=[]

  for hi in resDict["Headers"]:
    for h,d in hi.items():
      for k,v in revHash.items():
        #logging.debug("FillResume SEARCH HEADER {} HASH {}" .format(h, k) )
        k=k.strip()
        h=h.strip()
        sr = re.fullmatch(k,h, re.IGNORECASE)
        if not sr is None: # FOUND!!
          logging.debug("=================================")
          v = v.replace("'", '').replace('[', '').replace(']', '')
          v =  [  vs.strip()  for vs in v.split(",") ]
          tORes=ORes
          logging.debug("FillResume SEARCH Result:{} pattern:{} hash:{} vec:{}" .format(sr, k, h, v) )
          #logging.debug("FillResume FOUND HEADER {} HASH {}" .format(h, v) )
          lastvi=None
          if v[0] == "basics":
            FillResume.fillBasic(v, ORes, d, logging)
          if v[0] == "profiles":
              ORes["profiles"].append( {"url" : d })

              ORes["profiles"].append( {"url" : d })

          if v[0] == "work experience":
            FillResume.fillWorkExp(v, ORes, d, logging)

          if v[0] == "volunteer":
            #fillWorkExp(v, ORes, d)
            pass
          if v[0] == "education":
            FillResume.fillEdu(v, ORes, d, logging)
          if v[0] == "awards":
            #fillWorkExp(v, ORes, d)
            pass
          if v[0] == "publications":
            #fillWorkExp(v, ORes, d)
            pass
          if v[0] == "skills":
            FillResume.fillSkills(v, ORes, d, logging)
          if v[0] == "languages":
            #fillWorkExp(v, ORes, d)
            pass
          if v[0] == "interests":
            #fillWorkExp(v, ORes, d)
            pass
          if v[0] == "references":
            #fillWorkExp(v, ORes, d)
            pass

          break

  return ORes

OResfillList=[]
resume=[]
for item in resdfInit.loc[1:3000].iterrows():
  rtxt = item[1]['RESUME_TEXT']
  rlines = rtxt.splitlines()
  resDict={
      "RESUME_PATH" : item[1]["RESUME_PATH"],
      "TEXT": item[1]['RESUME_TEXT'],
      'RESUME_TYPE' : item[1][ 'RESUME_TYPE' ]
         }
  parasDict=[]
  ##Extract TOP
  AllHeadersList=[]
  HeaderStack=[]
  ParaLines=[]
  for line in rlines:
    isHeader=0
    isMatch=0
    para=""
    line=line.strip()
    ParaLinesw = FindHeadersInSingleLine(line)
    if MYDEBUG:
      logging.debug(" ParaLinesw  {} ".format(ParaLinesw))
    if not (ParaLinesw is None):
      parasDict.extend(ParaLinesw)
      continue

    isHeader += HeaderStats(line, avgWordCount, rvsWord, rvsHeader, rvsWordLen, rvsHeaderLen)
    if MYDEBUG:
      logging.debug("")
      logging.debug("============Stats==isHeader={}".format(isHeader))
    if MatchRegExp(text=line, cregs=hregall)>0:
        #most probablity this is an header line
        lheader, restofLine = SplitHeader(line)
        if not re.match(AntiHeadMatchpattern, lheader, flags=re.IGNORECASE):
            isHeader+=2
            isMatch=1
        #logging.debug("is in header list :{}   {}".format(line, isHeader))
    if isHeader>=3 and isMatch:
         #logging.debug("This is header :{}".format(line))
         if len(HeaderStack) >0:
           lastHeader=HeaderStack.pop()
         if len(ParaLines) >0:
           parajoin = " ".join(ParaLines).strip()
           if(len(parajoin)>0):
             parasDict.append( {lastHeader : " ".join(ParaLines)})
           AllHeadersList.append(lastHeader)
           lastHeader=""
           ParaLines=[]

         lheader, restofLine = SplitHeader(line)
         HeaderStack.append(lheader)
         ParaLines.append(restofLine)
         if MYDEBUG:
           logging.debug("")
           logging.debug("==============isHeader={}".format(isHeader))
           logging.debug(line)
           logging.debug("============================")
    elif isHeader>2:
        if MYDEBUG:
          logging.debug("")
          logging.debug("===== Sub Header==============isHeader={}".format(isHeader))
          logging.debug(line)
          logging.debug("============================")
          logging.debug("")
    else:
        if len(HeaderStack) >0:
          ParaLines.append(line)

  if len(HeaderStack) >0:
    lastHeader=HeaderStack.pop()
  if len(ParaLines) >0:
    parajoin = " ".join(ParaLines).strip()
    if(len(parajoin))>0:
      parasDict.append( {lastHeader : " ".join(ParaLines)})
      #parasDict.append( { lastHeader: " ".join(ParaLines)} )
      lastHeader=""
      ParaLines=[]

  wordcount = Counter(word_tokenize(rtxt))
  #resDict["Headers"]="{}".format(parasDict)
  #resDict["HeadersList"]="{}".format(AllHeadersList)
  #resDict["Wordcount"]="{}".format(wordcount)
  resDict["Headers"] = parasDict
  resDict["HeadersList"] = AllHeadersList
  resDict["Wordcount"] =  wordcount

  ORes = ResumeMapper.GetEmptyRes(xpath=xpath)
  OResfill =  FFillResume(resDict=resDict, revHash=revHash, ORes=ORes, logging=logging)
  resDict["OResfill"] =  OResfill
  OResfillList.append(OResfill)
  resume.append(resDict)

resumeDF = pd.DataFrame(OResfillList)

resumeDF.to_csv()

list(resumeDF.columns)
