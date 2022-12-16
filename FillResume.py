# -*- coding: utf-8 -*-
"""
Created on Sun May 27 13:05:50 2018

@author: anandrathi
"""



def dictObjListChk(MT,ORes,wede, logging):
  try:
    if not MT in ORes:
      ORes[MT]=[]
    if ORes[MT] is None:
      ORes[MT]=[]
    ORes[MT].append(wede)
    wed =  ORes[MT][-1]
  except Exception as e:
    logging.error("{}".format(e))
    logging.error("ORes = {}".format(ORes))
    logging.error("wede = {}".format(wede))
  return wed


def dictObjChk(MT,ORes,wede,logging):
  try:
    if not MT in ORes:
      ORes[MT]=wede
    if ORes[MT] is None:
      ORes[MT]=wede
    if not isinstance(ORes[MT],dict) :
      ORes[MT]=wede
  except Exception as e:
    logging.error("{}".format(e))
    logging.error("ORes = {}".format(ORes))
    logging.error("wede = {}".format(wede))
  return ORes[MT]

def fillObjL1(v, wed , d, logging):
  try:
    wed[v[1]] =  wed[v[1]] + " " + d
  except Exception as e:
    logging.error("{}".format(e))
    logging.error("wed = {}".format(wed))
    logging.error("v[] = {}".format(v))
    logging.error("v[1] = {}".format(v[1]))
    logging.error("d = {}".format(d))


def fillObjL2(v, wed , d, logging):
  try:
    wed[ v[1] ][ v[2] ] =   wed[ v[1] ][ v[2] ] + " "+ d
  except Exception as e:
    logging.error("fillObjL2 {}".format(e))
    logging.error("wed = {}".format(wed))
    logging.error("v[] = {}".format(v))
    logging.error("fillObjL2 v[1] = {}".format(v[1]))
    logging.error("fillObjL2 v[2] = {}".format(v[2]))

def fillSkills(v, ORes, d, logging):
  MT ="skills"
  wede = {
      "level": "",
      "keywords": ""
  }
  dictObjChk(MT=MT,ORes=ORes,wede=wede, logging=logging)
  wed =  ORes[MT]
  fillObjL1(v, wed , d, logging)

def fillLanguage(v, ORes, d, logging):
  MT ="languages"
  wede = {
      "language": "",
      "fluency": ""
  }
  dictObjChk(MT=MT,ORes=ORes,wede=wede, logging=logging)
  wed =  ORes[MT]
  fillObjL1(v, wed , d, logging)


def fillBasic(v, ORes, d, logging):
  MT ="basics"
  wede = {
      "name": "",
      "personal":"",
      "other": "",
      "label": "",
      "dob": "",
      "email": "" ,
      "phone": "",
      "marital Status": "",
      "gender": "",
      "nationality": "",
      "summary": "",
      "profiles":"",
      "location": {
        "address": "",
        "postalCode": "",
        "city": "",
        "countryCode": "",
        "region" : ""
        },
      "profiles" : ""
    }
  dictObjChk(MT=MT,ORes=ORes,wede=wede, logging=logging)
  wed =  ORes[MT]
  if v[1]=="location":
    fillObjL2(v, wed , d, logging)
  else :
    fillObjL1(v, wed , d, logging)

def fillEdu(v, ORes, d, logging):
  MT ="education"
  wede = {
      "education":"",
      "institution": "",
      "area": "",
      "studyType": "",
      "startDate": "",
      "endDate": "",
      "gpa": "",
      "courses": "",
	  "others":"",
	  "projects":""          
  }
  wed = dictObjListChk(MT=MT, ORes=ORes, wede=wede, logging=logging)
  fillObjL1(v, wed , d, logging)


def fillWorkExp(v, ORes, d, logging):
  MT ="work experience"
  wede = {
    "project":"",
    "experience":"",
    "organization":"",
    "location":"",
    "description":"",
    "roles":"",
    "highlights":"",
    "url":"",
    "duration":"",
    "startDate":"",
    "endDate":"",
    "teamsize":"",
    "summary":"",
    "roles":"",
    "highlights":""
  }

  wed =  dictObjListChk(MT=MT,ORes=ORes,wede=wede, logging=logging)
  fillObjL1(v, wed , d, logging)
