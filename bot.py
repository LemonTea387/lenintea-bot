import discord
import boto3
import os

TOKEN = os.getenv('DISCORD_TOKEN')
INSTANCE_ID = os.getenv('INSTANCE_ID')
client = discord.Client() #connect to discord client
instance = boto3.client('ec2',region_name = os.getenv('REGION'),
                        aws_access_key_id = os.getenv('ACCESS_KEY'),
                        aws_secret_access_key = os.getenv('SECRET_KEY'))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!') #tell console its connected to discord


@client.event   #for event a.k.a things going on in discord
async def on_message(message): #message stuff
    if message.author == client.user: #prevent bot for repeating it self
        return
    if message.content == '+start': 
        state = getInstanceState()
        if state != 'running' and state != 'pending' and state != 'stopping':
            turnOnInstance()
            await message.channel.send("Server is starting")
        else:
            await message.channel.send('Server is ' + state + '\nIf you think this is a bug, contact your incompetent developer.')
    elif message.content == '+state':
            await message.channel.send('AWS Instance state : ' + getInstanceState())

#functions to start instance
def turnOnInstance():
    try:
        instance.start_instances(
        InstanceIds=[
            INSTANCE_ID
                ],
        DryRun = False
        )
        return True
    except:
        return False

def getInstanceState():
    try:
        response = instance.describe_instance_status(InstanceIds=[INSTANCE_ID])
        return response['InstanceStatuses'][0]['InstanceState']['Name']
    except:
        return 'Server is not up :)'
    
client.run(TOKEN)