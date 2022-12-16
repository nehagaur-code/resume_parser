from flask import Flask, jsonify, request

app = Flask(__name__)

API_KEY = "1234@aleeph"

#education details
education =  {"educationType":"", "discipline":"", "minor":"", "institute":"", "university":"",
              "performanceScale":"", "achieved":"", "startYear":"", "endYear":"", "currentlyPursuing":""}

#skill details
skill = {"skill_name":"", "proficiency_level":"", "self_rate":"", "years_used":"", "last_used_year":""}

#work details
work_history = {"employer_name":"" , "start_date":"", "end_date":"", "current_employer":"true/false", "designation":"", "jobType":"",
        "job_description":""}

# education profile
# array of education details
education_profile=[]
education_profile.append(education)

# skill profile
# array of skill details
skill_profile=[]
skill_profile.append(skill)

# works profile
# array of work details
works_profile=[]
works_profile.append(work_history)

profile = {"title":"", "score":"", "education_profile":education_profile, "skill":skill_profile, "work_history":works_profile}


import os
import sys
import textract
import pathlib
import shlex
rootdir = sys.argv[1]

import ResumeParseStandAlone

def Convert2Text(filepath):
  text="NOT FOUND"
  try:
    #filepath = shlex.quote(filepath)
    #ofile = shlex.quote(ofile)
    text = textract.process(filepath)
  except Exception as e:
    print("Parse {} exception {}".format(filepath,e))
  return text


@app.route('/')
def get_incomes():
  return jsonify(profile)

@app.route('/convert', methods=['POST'])
def get_profile_json():
    file_location = {"file_location": request.json['file_location']}
    rtxt = Convert2Text(filepath=file_location)
    jsontxt =  ResumeParseStandAlone.GetResumeTxt2JSON(rtxt=rtxt)
    return jsonify(jsontxt)

if __name__ == '__main__':
    app.run(debug=True)

