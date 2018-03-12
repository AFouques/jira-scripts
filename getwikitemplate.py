#!/usr/bin/python2

import sys
from jiraauth import jclient as jira

'''
Synopsis:  This script runs a JQL search to get the "Done" issues in the
last x weeks in the project y and format it in a wiki template
Example: getwikitemplate.py [projectName] [iteration number of week OR since date in format YYYY-MM-DD_HH:mm]
'''

project = None
time = 0
date = None

if len(sys.argv) > 1:
    project = sys.argv[1]
else:
    project = raw_input("Project Name: ")

if len(sys.argv) > 2:
    time = sys.argv[2]
else:
    time = raw_input("iteration length in weeks OR since date in format YYYY-MM-DD_HH:mm : ")
if len(time) <= 3:
    date = "-" + time + "w"
else:
    date = "'" + time.replace("_", " ") + "'"



issues = jira.search_issues("project = " + project + " AND issuetype in (Story, Bug) AND status = Done AND resolved > " + date + " ORDER BY resolved ASC")

print "\nList of issues\n------------------------------"

teamsStory = {}
teamsBug = {}

for x in issues:
    if x.fields.customfield_11400 == None:
        sys.exit("Issue " + x.key + " has no Team! Fill it and run the script again --> https://genymobile.atlassian.net/browse/" + x.key)
    print x.key + " | " + x.fields.summary + " | " + x.fields.issuetype.name + " | " + x.fields.customfield_11400[0]
    if x.fields.issuetype.name == "Story":
        if not teamsStory.has_key(x.fields.customfield_11400[0]):
            teamsStory[x.fields.customfield_11400[0]] = [x]
        else:
            teamsStory[x.fields.customfield_11400[0]].append(x)
    else:
        if not teamsBug.has_key(x.fields.customfield_11400[0]):
            teamsBug[x.fields.customfield_11400[0]] = [x]
        else:
            teamsBug[x.fields.customfield_11400[0]].append(x)
        

print "------------------------------"
print "         Wiki Template"
print "------------------------------"
print ""
print "[[Accueil]] > [[Genymotion]] > [[Genymotion Product Management and Scrum]] > [[Genymotion Demos and Retros]] >> [[GenymotionNAME OF THE ITERATIONDemo]]"
print ""
print "==Main facts=="
print ""
print "* TODO: FILL THIS"
print ""
print "==Features=="
print ""
for team_key in teamsStory.keys():
    print "------------------------------------------"
    print ""
    print "===[Motion " + team_key + "]==="
    print "'''FO: TODO: FILL THIS'''<br/>"
    print "'''TODO: FILL TEAM MEMBERS'''"
    print ""
    print "TODO: FILL TEAM GOAL"
    print ""
    print "'''What was Done?'''"
    if teamsBug.get(team_key) != None:
        print "* Bug Fixed : " + str(len(teamsBug.get(team_key)))
    if teamsStory.get(team_key) != None:
        print "{| class='wikitable'"
        print "|-"
        print "! Jira Key !! Summary !! Demo?"
        print "|-"
        for x in teamsStory.get(team_key):
            description = x.fields.description.split("\r\n")
            print "| [https://genymobile.atlassian.net/browse/" + x.key + " " + x.key +"] || '''" + x.fields.summary + "'''<br />"
            if len(description) > 0: print "" + description[0] + "<br />"
            if len(description) > 1: print "" + description[1] + "<br />"
            if len(description) > 2: print "" + description[2]
            print "| -" # TODO FILL WHO :<br />
            # TODO FILL WHERE print [https://drive.google.com/open?id=0B0InYU6y8GpUQXBPSUNMbUNKWk0 Video]
            print "|-"
        print "|}"
