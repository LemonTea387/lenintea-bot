from discord.ext import commands
import os
import boto3
class AwsManager(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.instances_bank = self.update_instance_bank()
        self.instance = boto3.client('ec2',region_name = os.getenv('REGION'),
                        aws_access_key_id = os.getenv('ACCESS_KEY'),
                        aws_secret_access_key = os.getenv('SECRET_KEY'))
    
    def update_instance_bank(self):
        instances = os.environ
        instances = {key:instances[key] for key in list(instances) if key.startswith("INSTANCE_ID")}
        self.instances_bank = instances
    
    @commands.command()
    async def state(self,ctx,instance_name:str):
        self.update_instance_bank()
        name = 'INSTANCE_ID_'+instance_name.strip().upper()
        if self.__is_valid_instance(name):
            id = self.instances_bank.get(name)
            await ctx.send('AWS Instance Public Ip : ' + self.__get_instance_ip(id) + '\nstate : ' + self.__get_instance_state(id))
        else:
            await ctx.send('Sorry, was it too much to ask for you to follow the server names? What a disappointment.')
    
    @commands.command()
    async def start(self,ctx,instance_name:str):
        self.update_instance_bank()
        name = 'INSTANCE_ID_'+instance_name.strip().upper()
        if self.__is_valid_instance(name):
            id = self.instances_bank.get(name)
            state = self.__get_instance_state(id)
            # Innitiate server only when instance state is not running, pending or stopping. 
            # (AWS boto3 does not reply 'stopped' state)
            if state != 'running' and state != 'pending' and state != 'stopping':
                if (self.__start_instance(id)):
                    await ctx.send(f"Server {instance_name} is starting. Buckle up for some fun.")
                else:
                    await ctx.send(f'Error in starting server {instance_name}. Why? I have no freakin clue, ask AWS.')

            else:
                await ctx.send('Server is ' + state + '\nIf you think this is a bug, contact your incompetent developer.')
        else:
            await ctx.send('Sorry, was it too much to ask for you to follow the server names? What a disappointment.')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self,ctx,instance_name:str):
        self.update_instance_bank()
        name = 'INSTANCE_ID_'+instance_name.strip().upper()
        if self.__is_valid_instance(name):
            id = self.instances_bank.get(name)
            if self.__stop_instance(id):
                await ctx.send('Server is stopping~')
            else:
                await ctx.send('Server did not stop.')
        else:
            await ctx.send('Sorry master, couldn\'t find dem server with the name :(')
            return
        
    @commands.command()
    async def listservers(self,ctx):
        self.update_instance_bank()
        names = [name[12:] for name in self.instances_bank]
        names = '\n'.join(names)
        await ctx.send(f'```\nList of Servers available :\n{names}\n```')

        
    # Helper Commands
    def __is_valid_instance(self, instance_name):
        return instance_name in self.instances_bank
    
    def __get_instance_state(self,instance_id:str):
        try:
            response = self.instance.describe_instances(InstanceIds=[instance_id])
            return response['Reservations'][0]['Instances'][0]['State']['Name']
        except:
            return 'Server is not up :)'

    # Returns the public ip of the server
    def __get_instance_ip(self,instance_id:str):
        try:
            response = instance.describe_instances(InstanceIds=[instance_id])
            return response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        except:
            return 'Server is not up :)'
    
    def __start_instance(self,instance_id:str) -> bool:
        try:
            self.instance.start_instances(
            InstanceIds=[
                instance_id
                    ],
            DryRun = False
            )
            return True
        except:
            return False
    
    def __stop_instance(self,instance_id) -> bool:
        try:
            self.instance.stop_instances(
            InstanceIds=[
                instance_id
                ],
            DryRun = False
            )
            return True
        except:
            return False
    
def setup(bot):
    bot.add_cog(AwsManager(bot))