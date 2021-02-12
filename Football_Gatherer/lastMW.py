import requests
from bs4 import BeautifulSoup
import json
import datetime


def lastMWs(league, games=1):

    x = datetime.datetime.now()
    base_url = 'https://understat.com/league'
    url = base_url+'/'+league+'/'+str(x.year)

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")


    scripts = soup.find_all('script')
    string_with_json_obj = ''

    # Find data for teams
    for el in scripts:
        if 'teamsData' in str(el):
            string_with_json_obj = str(el).strip()
      

    # strip unnecessary symbols and get only JSON data
    ind_start = string_with_json_obj.index("('")+2
    ind_end = string_with_json_obj.index("')")
    json_data = string_with_json_obj[ind_start:ind_end]

    json_data = json_data.encode('utf8').decode('unicode_escape')

    data = json.loads(json_data)
    

    teams = {}
    for id in data.keys():
        teams[id] = data[id]['title']

    columns = []
    for id in data.keys(): 
        columns = list(data[id]['history'][0].keys()) 
        break

    columns.append('ppda_coef')
    columns.append('oppda_coef')


    cols_sum = ['Team', 'xG', 'xGA', 'npxG', 'npxGA', 'deep', 'deep_allowed', 'scored', 'missed', 'xpts', 'wins', 'draws', 'loses', 'pts', 'npxGD', 'ppda_coef', 'oppda_coef']
    #To sum - [1,2,3,4,7,8,9,10,11,14,15,16,17,18]
    #To mean - [19,20]

    sumind = [1,2,3,4,7,8,9,10,11,14,15,16,17,18,19,20]
    all_data = {}
    all_data['net'] = []
    
    for id in data.keys():
        all_data[teams[id]] = []
        for row in data[id]['history'][::-1][:min(games, len(data[id]['history']))]:
            all_data[teams[id]].append(list(row.values()))
        team_sums = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        team_sums = [teams[id]]+team_sums
        all_data[teams[id]] = [columns]+all_data[teams[id]]
        for i in range(1, len(all_data[teams[id]])):
            all_data[teams[id]][i].append(all_data[teams[id]][i][5]['att']/all_data[teams[id]][i][5]['def'] if all_data[teams[id]][i][5]['def'] != 0 else 0)
            all_data[teams[id]][i].append(all_data[teams[id]][i][6]['att']/all_data[teams[id]][i][6]['def'] if all_data[teams[id]][i][6]['def'] != 0 else 0)
            for j, k in enumerate(sumind):
                team_sums[j+1]+=all_data[teams[id]][i][k]
                
            
        team_sums[15]/=(len(all_data[teams[id]])-1)
        team_sums[16]/=(len(all_data[teams[id]])-1)

        all_data['net'].append(team_sums)
    all_data['net'] = sorted(all_data['net'], key=lambda x: x[13], reverse=True)
    all_data['net'] = [cols_sum]+ all_data['net']

    return(all_data)