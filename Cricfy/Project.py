import logging
import requests
import time
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5068695480:AAGFjq07b11NkmxMOSRNCZBhCv5_gmiU4Bs'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


url="https://hs-consumer-api.espncricinfo.com/v1/pages/matches/current?lang=en&latest=true"

Data = requests.get(url).json()

def batsmen(data,c):
    
    bat = data['supportInfo']['liveSummary']['batsmen']
    name = bat[0]['player']['longName']
    if c['isFour'] == True:
        score= "FOUR " + " From " + str(name)
        #print(score)
        time.sleep(15)
        return score

    if c['isSix'] == True:
        score= "SIX " + " From " + str(name)
        #print(score)
        time.sleep(15)
        return score

def bowler(data,w):
    bowl = data['supportInfo']['liveSummary']['bowlers']
    name = bowl[0]['player']['longName']
    wicket = str(name) + " TOOK THE WICKET OF " + str(data['supportInfo']['liveSummary']['batsmen'][0]['player']['longName'])
    #print(wicket)
    time.sleep(15)
    return wicket
           

live = [[match['scribeId'], match['series']['objectId'], match['series']['longName']] for match in Data['matches'] if match['status'] == "Live" ]
#print(live)
selected_live = ""
for i,live_match in enumerate(live):
            selected_live += f"Live {i+1} ->> "+str(live_match[2])+'\n' 
            #print(selected_live)
            


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    
    if live == []:
        await message.reply("No Live Matches".upper())
    
    else:
        await message.reply(selected_live)
        

            
        
@dp.message_handler()
async def echo(message: types.Message):

            selected_match = message.text
            #selected_match =input("Select Your Live match: ").lower()
            #await message.answer(selected_match)

            user_input = selected_match.strip("live ") or selected_match.strip("live") or selected_match
            user_input = int(user_input)
            current_match = live[user_input-1]
            #print(current_match)
            while True:
                url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?&seriesId={live[user_input-1][1]}&matchId={live[user_input-1][0]}&latest=true"
                
                data = requests.get(url).json()
                #print(data)
                
                #batsmen(data)

                c = data['recentBallCommentary']['ballComments'][0]    
                s = c['isFour'] or c['isSix'] 
                w =  c['isWicket']
                if c:
                    com= c['commentTextItems']
                    
                    if s:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        #NC = "----------No Commentary Available----------"
                        if com != None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(batsmen(data,w))
                            NC = "Commentary: ",com[0]['html']                        
                            await bot.send_message(-644768316,NCM)
                            await bot.send_message(-644768316,NC)
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(batsmen(data,w))
                            await bot.send_message(-644768316,NCM)
                        time.sleep(20)
                        

                    elif w:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        #NC = "----------No Commentary Available----------"
                        if com != None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nWicket : " + bowler(data,w)
                            NC = "Commentary: ",com[0]['html']                        
                            await bot.send_message(-644768316,NCM)
                            await bot.send_message(-644768316,NC)
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nWicket : " + bowler(data,w)
                            await bot.send_message(-644768316,NCM)
                        time.sleep(25)
                        

                    else:
                        a = c['oversActual'],c['title'],c['totalRuns']
                        NC = "----------No Commentary Available----------"
                        if com!=None:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(a[2])
                            NC = "Commentary: ",com[0]['html']                        
                            await bot.send_message(-644768316,NCM)
                            await bot.send_message(-644768316,NC)
                        else:
                            NCM = "Over : " + str(a[0]) +"\nTitle : " + str(a[1]) +"\nRuns : " + str(a[2])
                            await bot.send_message(-644768316,NCM)
                        time.sleep(18)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)