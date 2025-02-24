import os
import json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
#from azure.storage.blob import BlobClient

class FunctionCallGenerator:
    
    def __init__(self, model_config):

        self.model_config = model_config

    def __call__(self, intent: str):

        # cred = DefaultAzureCredential()

        # blob_client = BlobClient.from_blob_url(
        #     self.model_config["SWAGGER_PATH"], credential=cred
        # )
        # swagger_blob = blob_client.download_blob().readall()
        # swagger_spec = json.loads(swagger_blob)

        with open(self.model_config["SWAGGER_PATH"], 'r') as swagger_file:
            swagger_spec = json.load(swagger_file)

        system_prompt = f'''
        You generate an array of function calls for the specified API spec, in the expected format.
        You only generate the JSON array, and nothing else.

        API spec:
        {swagger_spec}
        
        Expected JSON array format:
        [{{"function": "function1", "args": {{ "arg1": "value1", "arg2": "value2" }} }}]
        '''

        project = AIProjectClient.from_connection_string(
            conn_str=self.model_config["FOUNDRY_CONNECTION_STRING"], credential=DefaultAzureCredential()
        )

        chat = project.inference.get_chat_completions_client()

        response = chat.complete(
            temperature=self.model_config.get("TEMPERATURE", None),
            top_p=self.model_config.get("TOP_P", None),
            model=self.model_config["MODEL"],
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": intent}
            ]
        )

        return { "actual_calls": json.loads(response.choices[0].message.content) }
