import requests, os

class Pinata():
    def __init__(self, api_key, secret_key, access_token):
        self.headers = {
                'pinata_api_key': api_key, 
                'pinata_secret_api_key': secret_key,
                'Authorization': f'Bearer {access_token}'
            }
        self.base_url = "https://api.pinata.cloud/"

    def pin_file(self, file):
        if isinstance(file, str):
            if os.path.exists(file) == False:
                return {'status': 'error', 'message':'File does not exist'}
            files = {
                'file': open(file, 'rb')
            }
        else:
            file_name = os.path.basename(file.filename)
            files = {
                'file': open('/tmp/' + file_name, 'wb').write(file.read()),
            }
        response = requests.post(f'{self.base_url}pinning/pinFileToIPFS', headers=self.headers, files=files).json()
        if 'error' in response:
            return {'status': 'error', 'message': response['error']['details']}
        return {'status': 'success', 'data': response}

    def unpin_file(self, ipfs_hash):
        response = requests.delete(f'{self.base_url}pinning/unpin/{ipfs_hash}', headers=self.headers)
        if response.status_code != 200:
            return {'status': "error", 'message': response.json()["error"]["details"]}
        return {'status': "success", 'message': "Unpinning file successful"}

    def get_pins(self):
        response = requests.get(f'{self.base_url}psa/pins', headers=self.headers).json()
        if "error" in response:
            return {'status': 'error', 'message':response['error']['details']}
        return {'status': 'success', 'data': response}
