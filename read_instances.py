import os
instances = {}
with open('instances.txt','r') as f:
    for line in f:
        key, configVar = line.split(':')
        instances[key] = os.getenv(configVar.strip())