import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def getTeamData(teamname, year):
    base_url = 'https://understat.com/team/'
    url = base_url+teamname+'/'+year

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")

    script = soup.find_all('script')
    for x in script:
        if 'datesData' in str(x):
            string_with_json_obj = str(x).strip()
            
    ind_start = string_with_json_obj.index("('")+2
    ind_end = string_with_json_obj.index("')")
    json_data = string_with_json_obj[ind_start:ind_end]

    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    cols = ['side', 'Home', 'Away', 'goals-H', 'goals-A', 'xG-H', 'xG-A', 'odds - w', 'odds - d', 'odds - l', 'result']
    games = {}
    for colname in cols:
        games[colname] = []

    for match in data:
        games['side'].append(match['side'])
        games['Home'].append(match['h']['short_title'])
        games['Away'].append(match['a']['short_title'])
        games['goals-H'].append(int(match['goals']['h']))
        games['goals-A'].append(int(match['goals']['a']))
        games['xG-H'].append(float(match['xG']['h']))
        games['xG-A'].append(float(match['xG']['a']))
        games['odds - w'].append(match['forecast']['w'])
        games['odds - d'].append(match['forecast']['d'])
        games['odds - l'].append(match['forecast']['l'])
        games['result'].append(match['result'])

    finalData = pd.DataFrame(games)
    return finalData

print("Enter team name - Use underscores instead of spaces")
team = input()
print("Enter year season started")
year = input()
print("Filename?")
filename = input()
getTeamData(team, year).to_excel(filename+'.xlsx')
'''
try:
    getTeamData(team, year).to_excel(filename+'.xlsx')
    print("Success!")
except():
    print(e)
    print("An error occured")'''




