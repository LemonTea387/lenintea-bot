import discord
import boto3
import os
from read_instances import get_instances

TOKEN = os.getenv('DISCORD_TOKEN')
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

    # Start method for the instances
    if message.content.startswith("+start"): 
        # Reset instance_name to new list to have the most updated list
        instance_name = get_instances()
        if ("INSTANCE_ID_"+message.content.split()[1].upper()) not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get("INSTANCE_ID_"+message.content.split()[1].upper())

        state = getInstanceState(INSTANCE_ID)
        # Innitiate server only when instance state is not running, pending or stopping. 
        # (AWS boto3 does not reply 'stopped' state)
        if state != 'running' and state != 'pending' and state != 'stopping':
            if (turnOnInstance(INSTANCE_ID)):
                await message.channel.send("Server is starting")
            else:
                await message.channel.send('Error in starting server')

        else:
            await message.channel.send('Server is ' + state + '\nIf you think this is a bug, contact your incompetent developer.')

    # Displays the state of the instance
    elif message.content.startswith("+state"):
        # Reupdate Instance_name to have the latest data
        instance_name = get_instances()
        if ("INSTANCE_ID_"+message.content.split()[1].upper()) not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get("INSTANCE_ID_"+message.content.split()[1].upper())

        await message.channel.send('AWS Instance Public Ip : ' + getInstanceIp(INSTANCE_ID) + '\nstate : ' + getInstanceState(INSTANCE_ID))
    
    # Stops the server
    elif message.content.startswith("+stop"):
        # Reupdate instance_name to have the latest data
        instance_name = get_instances()
        if ("INSTANCE_ID_"+message.content.split()[1].upper()) not in instance_name:
            await message.channel.send('INVALID SERVER NAME BRUHH')
            return
        else :
            INSTANCE_ID = instance_name.get("INSTANCE_ID_"+message.content.split()[1].upper())
        
        if message.author.guild_permissions.administrator:
            if (stopInstance(INSTANCE_ID)):
                await message.channel.send('Server is stopping~')
            else :
                await message.channel.send('Server did not stop.')
        else :
            await message.channel.send('You are not admin :(, your attacks are FUTILE!')
    
    # Lists all the instances
    elif message.content.startswith("+listservers"):
        # Reupdate instance_name to have the latest data
        instance_name = get_instances()
        names = [name[12:] for name in instance_name]
        names = "\n".join(names)
        await message.channel.send(f'```\nList of Servers available :\n{names}\n```')
            
    # Pays respect
    elif message.content.upper().startswith("+F"):
        for mention in message.mentions:
            await message.channel.send(f'{message.author.mention} has paid their respects to {mention.mention}')

# Functions to start instance
# Returns boolean on outcome
def turnOnInstance(INSTANCE_ID):
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
def stopInstance(INSTANCE_ID):
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
def getInstanceState(INSTANCE_ID):
    try:
        response = instance.describe_instances(InstanceIds=[INSTANCE_ID])
        return response['Reservations'][0]['Instances'][0]['State']['Name']
    except:
        return 'Server is not up :)'


# Returns the public ip of the server
def getInstanceIp(INSTANCE_ID):
    try:
        response = instance.describe_instances(InstanceIds=[INSTANCE_ID])
        return response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    except:
        return 'Server is not up :)'
    
client.run(TOKEN)