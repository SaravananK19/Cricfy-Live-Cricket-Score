import logging
import requests
import time
from aiogram import Bot, Dispatcher, executor, types
#dispatcher-  used to handle updates and route them to the appropriate handlers. 
#Handlers are used to define how your bot should respond to different types of user input or system events.

API_TOKEN = '5068695480:AAGFjq07b11NkmxMOSRNCZBhCv5_gmiU4Bs'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
#The Dispatcher is responsible for handling updates from Telegram and directing them to the appropriate handlers.
#Dispatcher is then initialized with the Bot object. The Dispatcher is responsible for handling updates from Telegram and directing them to the appropriate handlers.


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
            
#These handle commands that users send to the bot, usually starting with a '/'
#The @dp.message_handler() decorator is used to register a function (send_welcome in this case) as a handler for incoming messages.
#The decorator specifies that the function should be called when a message is received.
#The send_welcome function takes a types.Message object as a parameter, which represents the incoming message from the user.
#Inside this function, you have logic to handle the /start and /help commands.

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    
    if live == []:
        await message.reply("No Live Matches".upper())
    
    else:
        await message.reply(selected_live)
        

            
# These handle incoming messages from users.      
@dp.message_handler()
#handler function named echo is registered to handle any other messages from the user. Inside this function, 
#you have logic to process the selected live match and continuously fetch live commentary data.
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
                            await bot.send_message(-644768316,NCM)#-644768316 is the chat ID of the target channel.
                            #await: This keyword is used to indicate that the code is waiting for the result of the send_message method.
                            #In an asynchronous context (as indicated by the use of async and await) this is necessary for non-blocking execution.


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
#Executor handling the execution of the bot.
#The start_polling method is used to start the polling loop.( bot regularly checks for new updates or events from the Telegram server.)
#The bot repeatedly sends requests to the Telegram server asking if there are any new updates.
#This is typically done by calling an API method that checks for updates since the last known update ID.
#When the bot receives new updates, it processes them. Updates can include messages from users.

#The polling loop allows the bot to be responsive to user interactions in near-real-time. 
