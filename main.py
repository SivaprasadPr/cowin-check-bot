from typing import final
import discord
import requests
from datetime import date
from time import time, sleep



token = '' #Provide your discord bot token here
# url for the cowin api
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
# the interval in which the result should be refreshed
DELAY = 180

client = discord.Client()



@client.event
async def on_ready():
    print(f'{client.user} has successfully connected!')
    



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print (message.mentions)
        mention = f'{message.mentions}'
        if((mention.find(f'{client.user.name}'))>=0):
             print(f'{message.author}: {message.content}')
             # this block will activate if a user mention the bot with a message containing the word 'cowin'
             if("cowin" in message.content):
                text1 = f'Triggered\nDelay set: {DELAY} seconds'
                print(text1)
                await message.channel.send(text1)
                k = 0
                prev = None
                while True:
                        k += 1
                        print("Try: ", k)
                        if(k > 20): # Terminate after 1 hour
                            await message.channel.send(f'Timeout')
                            print("Timeout")
                            break 
                        sleep(DELAY-time() % DELAY)
                        # defining a params dict for the parameters to be sent to the API
                        
                        # the distict_id given here is a random one, you have to find your district id from the cowin protal
                        PARAMS = {'district_id':304, 'date': date.today().strftime('%d-%m-%Y')}

                        
                        # sending get request and saving the response as response object
                        r = requests.get(url = URL, params = PARAMS)

                        # extracting data in json format
                        data = r.json()

                         #checking whether the data has changed or not
                        if(data == prev):        
                            continue
                        else:
                            prev = data

                        # printing the output
                        print("Size :",len(data))
                        
                        # this varible is used to store the message to send to discord
                        text = ""
                        # iterate through every available centers
                        for key1 in data['centers']:          
                            # iterate though every sessions available in each center
                            for i in key1['sessions']:         
                                # you can change the conditons for the bot to respond 
                                # right now it is set to only respond if 'Free' 'Dose 1' vaccines are available
                                # fee types are 'Free' and 'Paid'
                                # for dose 2 you can use key 'available_capacity_dose2'
                                
                                if(i['available_capacity_dose1']>0 and key1['fee_type'] == 'Free'):
                                    text = text + f'Name: {key1["name"]}\nSlots\nDose 1 : {i["available_capacity_dose1"]}\nDose 2 : {i["available_capacity_dose2"]}\nType: {key1["fee_type"]}\nVaccine: {i["vaccine"]}\n━━━━━━━━━━━━━━━━━━━━━━━━\n'                           
                        if (text != ""):
                            # print the bot's response before sending 
                            print(f'Message: {text}')
                            # send the response to discord
                            await message.channel.send("```"+text+"```")
        else:
            await message.channel.send(f'Hello {message.author.mention}')
client.run(token)

