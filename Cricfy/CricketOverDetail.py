#This code provides a live commentary feed for a selected cricket match, displaying over details, titles, runs, and commentary text if available.
import requests
import time

url="https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"

Data = requests.get(url).json()
'''
ALITER: W/O USING List COMPREHENSION
__________________________________________________________________________

for match in Data['matches']:
        if match['status'] == "Live":
            #print(match)
            alive = []
            live_match = alive.append(match['series']['longName'])
            for i in alive:
                print(f"Live {j} ->> ",i)
                j+1
______________________________________________________________________________ 
'''           

live = [[match['scribeId'], match['series']['objectId'], match['series']['longName'], match['teams'][0]['team']['longName'],match['teams'][1]['team']['longName']] for match in Data['matches'] if match['status'] == "Live" ]
print(live) #print the live cricket matches
if live == []:
    print("No Live Matches".upper())
    
else:
    for i,live_match in enumerate(live):#allows you to access both the index and the value of each element in the live list during the loop iteration.
        selected_live = f"Live {i+1} ->> "+str(live_match[2])+'\n'
        print(selected_live)
        
    selected_match =input("Select Your Live match: ").lower()
    #if the user enters a string like "live 3" or "live3", strip("live ") will remove the prefix "live "
    user_input = selected_match.strip("live ") or selected_match.strip("live") or selected_match
    user_input = int(user_input)
    m = live[0][2]
    vs = str(live[0][3]) + " VS " + str(live[0][4]) + "\n"
    print(m,"\n",vs)
    #print(user_input)
    
    sets = set({})
    dup = ""


    while True:
        current_match = live[user_input-1]
        #print(current_match)
        url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?&seriesId={live[user_input-1][1]}&matchId={live[user_input-1][0]}&latest=true"
        #print(url)
        data = requests.get(url).json()
        #print(data)
        

        c = data['recentBallCommentary']['ballComments'][0]
        #print(c['oversActual'],c['title'],c['totalRuns'])
        #o = data['over']
        #print(o)
        a = c['oversActual'],c['title'],c['totalRuns']
        # duplicate values are automatically eliminated, and only unique values are stored in the set. 
        # To track the unique over
        sets.add(a[0])
        #print(sets)
        if c:
            com= c['commentTextItems']
            #print(com)
            if com == None:       
                a = c['oversActual'],c['title'],c['totalRuns']
                #print("----------No Commentary Available----------")
                NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : "+ str(a[2]) + "\n"
                if dup == NCM:
                    time.sleep(15)
                else:              
                    print(NCM)
                    dup = NCM
                #time.sleep(15)
                '\n'
                        
                #print("\10n END OF OVER \10n")

            else:    
                a = c['oversActual'],c['title'],c['totalRuns']
                #print("---------Commentary Available-----------")                         
                NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(a[2]) + "\nCommentary: " + str(com[0]['html']) + "\n"
                if dup == NCM:
                    time.sleep(15)
                else:              
                    print(NCM)
                    dup = NCM
                #time.sleep(15)
                '\n'








