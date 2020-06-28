import requests
import json
import os

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb+") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def downloadAllFiles(baseFolder):
    with open('ResourceLinks.json') as json_file:
        jsonData = json.load(json_file)
    downloadFiles(jsonData,baseFolder)

def downloadFiles(jsonData,baseFolder):
    for key in jsonData:
        destination = baseFolder + "/" + key
        includedObject = jsonData[key]
        if "." in key:
            if not os.path.isdir(baseFolder):
                os.mkdir(baseFolder)
            #Uncomment This and tab line 48 if you only want to download missing files
            #if not os.path.exists(destination):
            download_file_from_google_drive(id=includedObject,destination=destination)
        else:
            downloadFiles(includedObject,destination)






if __name__ == "__main__":
    import sys
    # DESTINATION FILE ON YOUR DISK
    destination = 'Resources'
    downloadAllFiles(destination)