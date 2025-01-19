import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlY2RjN2FhZS00MTI4LTQyZTAtODE1Yi0xMzZhNDczZmZiMGQiLCJlbWFpbCI6InNoYXZvbi50aGFkYW5pQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI2ZjRjYjQxY2Y0MTY2MzgzOGZkNiIsInNjb3BlZEtleVNlY3JldCI6ImRhMDZhYThjMmMyNTg4NDZhY2NmNjk0NzMwZWJlNzIwNjM5ZGNjNjk0MDNmYjE1YjM3MWFjMWRiYTNmZmMzMjkiLCJleHAiOjE3Njg3NDIzMzl9.WXPFvzT5j0W7MtSvQy7kw8NcgB4fuafB81VdKJ3wmyY"
PINATA_GATEWAY = "https://gateway.pinata.cloud"  # Pinata Gateway

class Decentralized_db:
    def upload_file_to_pinata(self, file, filename):
        """
        Upload a file to Pinata using the JWT Token.
        """
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"  # Pinata API endpoint

        headers = {
            "Authorization": f"Bearer {PINATA_JWT}",
        }

        
        files = {'file': (filename, file, 'application/octet-stream')}

        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            print("File uploaded successfully!")
            print("Response:", response.json())
            cid = response.json().get("IpfsHash", None)
            return cid
        else:
            print("Error uploading file:", response.text)
            return None
    def retrieve_file_from_cid(self, cid):
            """
            Retrieve a file from IPFS using the CID.
            """
            url = f"https://gateway.pinata.cloud/ipfs/{cid}"  # IPFS gateway URL
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print("File retrieved successfully!")
                    return response.content  # The file content
                else:
                    print(f"Error retrieving file. Status code: {response.status_code}, Message: {response.text}")
                    return None
            except Exception as e:
                print(f"An error occurred while retrieving the file: {e}")
                return None