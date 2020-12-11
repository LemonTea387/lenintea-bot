import discord
import boto3
import os

TOKEN = os.getenv('DISCORD_TOKEN')
INSTANCE_ID = 0
client = discord.Client() #connect to discord client
instance = boto3.client('ec2',region_name = os.getenv('REGION'),
                        aws_access_key_id = os.getenv('ACCESS_KEY'),
                        aws_secret_access_key = os.getenv('SECRET_KEY'))

# Dict to fetch the correct instance id
instance_name = {
    "lemonteabagpack":os.getenv("INSTANCE_ID_LEMON"),
    "ultimatealchemy":os.getenv("INSTANCE_ID_ULTIMATEALCHEMY"),
    "vanilla":os.getenv("INSTANCE_ID_VANILLA"),
    "enigmatica2light":os.getenv("INSTANCE_ID_ENIGMATICA2LIGHT")
}

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

    # Start method for the instances
    if message.content.startswith("+start"): 
        if message.content.split()[1].lower() not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get(message.content.split()[1].lower())


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
        if message.content.split()[1].lower() not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get(message.content.split()[1].lower())

        await message.channel.send('AWS Instance Public Ip : ' + getInstanceIp() + '\nstate : ' + getInstanceState())
    
    # Stops the server
    elif message.content.startswith("+stop"):
        if message.content.split()[1].lower() not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get(message.content.split()[1].lower())
        
        if message.author.guild_permissions.administrator:
            if (stopInstance()):
                await message.channel.send('Server is stopping~')
            else :
                await message.channel.send('Server did not stop.')
        else :
            await message.channel.send('You are not admin :(, your attacks are FUTILE!')
            
    # Pays respect
    elif message.content.upper().startswith("+F"):
        for mention in message.mentions:
            await message.channel.send(f'{message.author.mention} has paid their respects to {mention.mention}')

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

# Function to stop instance
# Returns boolean on outcome
def stopInstance():
    try:
        instance.stop_instances(
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
    except:
        return 'Server is not up :)'
    
client.run(TOKEN)