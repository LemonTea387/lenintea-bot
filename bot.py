import discord
import boto3
import os

TOKEN = os.getenv('DISCORD_TOKEN')
INSTANCE_ID = 0
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
    global INSTANCE_ID
    # Return program flow when author is bot. Stops looping
    if message.author == client.user: 
        return

    if message.content.startswith("+start"): 
        if(message.content.split()[1] == "lemonteabagpack"):
            INSTANCE_ID = os.getenv('INSTANCE_ID_LEMON')
        elif(message.content.split()[1] == "UltimateAlchemy"):
            INSTANCE_ID = os.getenv("INSTANCE_ID_ULTIMATEALCHEMY")
        elif(message.content.split()[1] == "Vanilla"):
            INSTANCE_ID = os.getenv("INSTANCE_ID_VANILLA1163")
        else:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return


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
    elif message.content.startswith("+state"):
        if(message.content.split()[1] == "lemonteabagpack"):
            INSTANCE_ID = os.getenv('INSTANCE_ID_LEMON')
        elif(message.content.split()[1] == "UltimateAlchemy"):
            INSTANCE_ID = os.getenv("INSTANCE_ID_ULTIMATEALCHEMY")
        elif(message.content.split()[1] == "Vanilla"):
            INSTANCE_ID = os.getenv("INSTANCE_ID_VANILLA1163")
        else:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return


        await message.channel.send('AWS Instance state : ' + getInstanceState() +f'\n {getInstanceIp()}')


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
        response = instance.describe_instances(InstanceIds=[INSTANCE_ID])
        return response['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return 'Server is not up :)'


# Returns the public ip of the server
def getInstanceIp():
    try:
        response = instance.describe_instances(InstanceIds=[INSTANCE_ID])
        return response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
client.run(TOKEN)