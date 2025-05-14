import os
import json

class SetEnv:
    def __init__(self):
        os.environ['DC_API_KEY'] = 'your-api-key-here'



_config_instance = SetEnv()