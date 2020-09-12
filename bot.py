import discord
import boto3
import os

TOKEN = os.getenv('DISCORD_TOKEN')
INSTANCE_ID = os.getenv('INSTANCE_ID')
client = discord.Client() #connect to discord client
instance = boto3.client('ec2',region_name = os.getenv('REGION'),
                        aws_access_key_id = os.getenv('ACCESS_KEY'),
                        aws_secret_access_key = os.getenv('SECRET_KEY'))

# On event of bot going up and running
@client.event
async def on_ready():
    print(f'{client.user.name} has come online and connected to Discord')


@client.event
async def on_message(message): 
    # Return program flow when author is bot. Stops looping
    if message.author == client.user: 
        return

    if message.content == '+start': 
        state = getInstanceState()
        # Innitiate server only when instance state is not running, pending or stopping. 
        # (AWS boto3 does not reply 'stopped' state)
        if state != 'running' and state != 'pending' and state != 'stopping':
            if (turnOnInstance()):
                await message.channel.send("Server is starting")
            else:
                await message.channel.send('Error in starting server')

        else:
            await message.channel.send('Server is ' + state + '\nIf you think this is a bug, contact your incompetent developer.')

    # Displays the state of the instance
    elif message.content == '+state':
        await message.channel.send('AWS Instance state : ' + getInstanceState())


# Functions to start instance
# Returns boolean on outcome
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

# Returns state of server as String
def getInstanceState():
    try:
        response = instance.describe_instance_status(InstanceIds=[INSTANCE_ID])
        return response['InstanceStatuses'][0]['InstanceState']['Name']
    except:
        return 'Server is not up :)'
    
client.run(TOKEN)