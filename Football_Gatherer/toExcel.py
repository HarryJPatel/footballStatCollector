from allHistory import getData
from lastMW import lastMWs
import sys
import pandas as pd
import numpy as np


print("All history from a particular season(A)")
print("or")
print("Recent games(R)")
print("or")
print("Exit(E)")
try:
    inp = input().upper()
except:
    print("Invalid Input")
    sys.exit()
leagues = ['La_liga', 'EPL', 'Bundesliga', 'Serie_A', 'Ligue_1', 'RFPL']
if inp == 'E':
    sys.exit()
elif inp == "A":
    print("Enter Number of interested league")
    print('1 - La_liga\n2 - EPL\n3 - Bundesliga\n4 - Serie_A\n5 - Ligue_1\n6 - RFPL\n')
    try:
        x = int(input())
    except:
        print("Please enter a valid choice")
        sys.exit()

    x-=1
    try:
        league = leagues[x]
    except:
        print("Please enter a valid choice")
        sys.exit()

    
    print("Which season? (YYYY)")
    print("Enter the year the season started.")
    try:
        year = int(input())
    except:
        print("Please enter a valid choice")
        sys.exit()
    
    data = getData(league, year)
   

    print("Filename? (w/o extension)")
    filename = input()

elif inp == "R":
    print("Enter Number of interested league")
    print('1 - La_liga\n2 - EPL\n3 - Bundesliga\n4 - Serie_A\n5 - Ligue_1\n6 - RFPL\n')
    try:
        x = int(input())
    except:
        print("Please enter a valid choice")
        sys.exit()

    x-=1
    try:
        league = leagues[x]
    except:
        print("Please enter a valid choice")
        sys.exit()

    print("How many GW's back would you like to go?(Max limit is the number of games played so far)")
    try:
        matches = int(input())
    except:
        print("Please enter a valid choice")
        sys.exit()

    data = lastMWs(league, matches)

    print("Filename? (w/o extension)")
    filename = input()

else:
    print("Invalid Choice!")
    sys.exit()

for id in data.keys():
    data[id] = pd.DataFrame(data[id])


with pd.ExcelWriter(filename+'.xlsx') as writer:
    for id in data.keys():
        data[id].to_excel(writer, sheet_name=id)

print("Data Gathered!")
