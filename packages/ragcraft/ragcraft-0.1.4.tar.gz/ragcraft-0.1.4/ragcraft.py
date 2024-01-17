import requests
import os 

class Ragcraft:
    base_url = str(os.getenv('RAGCRAFT_ENDPOINT')) if 'RAGCRAFT_ENDPOINT' in os.environ else "https://ragevals-lively-snowflake-5923-divine-bird-6466.fly.dev"
    api_key = str(os.getenv('RAGCRAFT_API_KEY'))
    dataset_name = None

    @staticmethod
    def _strip_quotes(value):
        """
        Helper method to strip quotes from a string.
        """
        if isinstance(value, str):
            return value.strip('"').strip("'")
        return value
    
    @staticmethod
    def init():
        Ragcraft.base_url = Ragcraft._strip_quotes(os.getenv('RAGCRAFT_ENDPOINT')) if 'RAGCRAFT_ENDPOINT' in os.environ else "https://ragevals-lively-snowflake-5923-divine-bird-6466.fly.dev"
        Ragcraft.api_key = Ragcraft._strip_quotes(os.getenv('RAGCRAFT_API_KEY'))

    @staticmethod
    def prepare_payload(additional_payload):
        """
        Prepares the payload with necessary API keys.
        """
        payload = {
            "token": Ragcraft._strip_quotes(Ragcraft.api_key),
            "openai_api_key": Ragcraft._strip_quotes(os.getenv('OPENAI_API_KEY'))
        }
        payload.update(additional_payload)
        return payload
    
    @staticmethod
    def generate(payload, files=[]):
        
        complete_payload = Ragcraft.prepare_payload(payload)

        files_to_send = [('files', (open(file_path, 'rb'))) for file_path in files]

        response = requests.post(f"{Ragcraft.base_url}/api/generate", files=files_to_send, data=complete_payload)

        for _, file_obj in files_to_send:
            file_obj.close()
        
        response = response.json()
        return {
            "message": "Generator in progress, Use the list_datasets() API to check the status of the generator",
            "gen_id": response["gen_id"],
            "dataset_id": response["dataset_id"]
        }

    @staticmethod
    def list_datasets(payload):
        complete_payload = Ragcraft.prepare_payload(payload)
        response = requests.get(f"{Ragcraft.base_url}/api/dataset/list", params=complete_payload)
        return response.json()
 
    @staticmethod
    def fetch(payload):
        complete_payload = Ragcraft.prepare_payload(payload)
        response = requests.get(f"{Ragcraft.base_url}/api/qa-data", params=complete_payload)
        return response.json()

    @staticmethod
    def evaluate(query_params):
        response = requests.get(f"{Ragcraft.base_url}/api/evaluate", params=query_params)
        return response.json()

