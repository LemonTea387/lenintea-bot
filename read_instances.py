def get_instances():
    import os
    instances = {}
    instances = os.environ
    instances = {key:instances[key] for key in list(instances) if key.startswith("INSTANCE_ID")}
    return instances