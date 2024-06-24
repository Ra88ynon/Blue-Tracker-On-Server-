import requests
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()
URL=os.getenv("URL")
APIKey=os.getenv("APIKey")
def get_Vessels():
    LocalURL = URL+"ships"
    Auth=f"ApiKey {APIKey}"
    header={
        "content-type":"application/json",
        "authorization":Auth
    }
    response = requests.get(LocalURL, headers=header)
    if response.status_code==200 :
        return response.json()
    else:
        return response
def get_Report(IMONum):
    LocalURL = URL +"ships/"+IMONum+ "/reportsummaries"
    Auth=f"ApiKey {APIKey}"
    header={
        "content-type":"application/json",
        "authorization":Auth
    }
    response = requests.get(LocalURL, headers=header)
    if response.status_code==200 :
        return response.json()
    else:
        return response

def get_Events(IMONum):
    LocalURL = URL + "ships/" + IMONum + "/events"
    Auth=f"ApiKey {APIKey}"
    header = {
        "content-type": "application/json",
        "authorization": Auth
    }
    response = requests.get(LocalURL, headers=header)
    if response.status_code==200 :
        return response.json()
    else:
        return response

def get_Voyage(IMONum):
        LocalURL = URL + "ships/" + IMONum + "/voyages"
        Auth=f"ApiKey {APIKey}"
        header = {
            "content-type": "application/json",
            "authorization": Auth
        }
        response = requests.get(LocalURL, headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            return response
def Get_VoyageSummary(VoyageID):
        print(VoyageID)
        LocalURL = URL + "voyages/" + VoyageID + "/summary"
        Auth=f"ApiKey {APIKey}"
        header = {
            "content-type": "application/json",
            "authorization": Auth
        }
        response = requests.get(LocalURL, headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            return response



def Get_LegSummary(EventId):
    LocalURL = URL + "legs/" + EventId + "/legSummary"
    Auth=f"ApiKey {APIKey}"
    header = {
        "content-type": "application/json",
        "authorization": Auth
    }
    response = requests.get(LocalURL, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        return [response, response.text]




