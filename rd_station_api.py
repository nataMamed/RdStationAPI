import requests


class RdStationAPI:
    def __init__(self, client_id, client_secret, refresh_token):
        self.host = "https://api.rd.services"
        self.token = self.make_access_token(client_id, client_secret, refresh_token)


    
    def make_access_token(self, client_id, client_secret, refresh_token):
        json = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
        }


        header = {
        'Content-Type': 'application/json'
        }
        resp = requests.post(url=f'{self.host}/auth/token',headers= header, json=json).json()

        return resp['access_token']

    def get(self, url):
        headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}"
                }
        return requests.get(url, headers=headers)


    def fetch_analytics_workflow_emails(self, start_date, end_date):
        result = self.get(f'{self.host}/platform/analytics/workflow_emails?start_date={start_date}&end_date={end_date}')
        print(f"Status code: {result.status_code}")
        return result.json()['workflow_email_statistics']


    def fetch_analytics_emails(self, start_date, end_date):
        result = self.get(f'{self.host}/platform/analytics/emails?start_date={start_date}&end_date={end_date}')
        print(f"Status code: {result.status_code}")
        return result.json()['emails']


    def fetch_segmentations(self):
        # get segmentations
        page_counter = 1
        all_segmentations = []
        while True:
            url =  f"{self.host}/platform/segmentations?page={page_counter}&page_size=125"
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}"
                }

            segmentations = requests.get(url, headers=headers).json()['segmentations']


            all_segmentations.extend(segmentations)
            page_counter += 1
            
            if len(segmentations) < 125:
                break

        return all_segmentations


    def fetch_leads_from_segmentation(self, segmentation_id):
        
        contacts = []   

        page = 1


        headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {self.token}"
        }
        while True:
            url = f"{self.host}/platform/segmentations/{segmentation_id}/contacts?page={page}&page_size=125"
            print("Request -> id: ", id, f"| page:{page}")
            temp_contacts_json = requests.get(url, headers=headers).json()
            if  'contacts' in temp_contacts_json.keys():
                temp_contacts = temp_contacts_json['contacts']
                
                if len(temp_contacts) > 0:
                    print(len(temp_contacts))
                    contacts.extend(temp_contacts)
                    page += 1
                    
                if len(temp_contacts) < 125:
                    break
            else:
                break


        return contacts