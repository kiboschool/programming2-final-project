from urllib import request
import json
import os

from helpers import datetime_to_eventbrite_format

class EventBriteAPIHelper:
    '''Methods that send/receive data to the eventbrite.com api'''
    def __init__(self):
        self.token = get_api_key()
        print(self.token)

    def get_organization_id(self):
        # (gets the "organization id" of our eventbrite.com account)
        url = f'https://www.eventbriteapi.com/v3/users/me/organizations/?token={self.token}'

        request_object = request.Request(url, method="GET")
        request_object.add_header('Content-Type', 'application/json')

        opened_request = request.urlopen(request_object, data=None)
        result = opened_request.read().decode('utf-8')
        parsed = json.loads(result)
        
        print(f"{parsed['organizations'][0]['id']=}")
        return parsed['organizations'][0]['id']

    # def get_event_information(self, event_id):
    #     token = helpers.get_api_key()
    #     url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?token={token}'
    #     request_object = request.Request(url, method="GET")
    #     request_object.add_header('Content-Type', 'application/json')
    #     opened_request = request.urlopen(request_object, data=None)
    #     result = opened_request.read().decode('utf-8')
    #     parsed = json.loads(result)
    #     return parsed
        
    def create_event(self, title, description, start_time, end_time):
        organization_id = self.get_organization_id()
        
        # the reason we place the data in a dictionary that looks like this is that
        # the eventbrite api documents the structure here,
        # https://www.eventbrite.com/platform/api#/reference/event/create/create-an-event
        data = {
            "event": {
                "currency": "USD",
                "name": {
                    "html": title
                },
                "description": {
                    "html": description
                },
                "start": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(start_time)
                },
                "end": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(end_time)
                },
            }
        }

        data = json.dumps(data)
        data = data.encode()
        
        url = f'https://www.eventbriteapi.com/v3/organizations/{organization_id}/events/?token={self.token}'
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        opened_request = request.urlopen(req, data=data)
        content = opened_request.read().decode('utf-8')
        parsed = json.loads(content)
        return parsed.get('id')

    def update_event(self, event_id, title, description, start_time, end_time):

        # the reason we place the data in a dictionary that looks like this is that
        # the eventbrite api documents the structure here,
        # https://www.eventbrite.com/platform/api#/reference/event/create/create-an-event
        data = {
            "event": {
                "currency": "USD",
                "name": {
                    "html": title
                },
                "description": {
                    "html": description
                },
                "start": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(start_time)
                },
                "end": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(end_time)
                },
            }
        }

        data = json.dumps(data)
        data = data.encode()
        
        url = f'https://www.eventbriteapi.com/v3/events/{event_id}/?token={self.token}'
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        opened_request = request.urlopen(req, data=data)

    ########### HELPERS ###############

def get_api_key():
    '''Read the api key from the apikey.txt file'''
    if not os.path.exists('apikey.txt'):
        raise Exception("Please create a file named apikey.txt and paste the Private Token there")
    
    with open('apikey.txt') as f:
        return f.read().strip()

if __name__ == '__main__':
    client = EventBriteAPIHelper()
    result = client.create_event("Test Event", "something", "2024-05-12T02:00:00Z", "2024-05-12T04:00:00Z" )

    print(result)