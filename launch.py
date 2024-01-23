import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from datetime import datetime, timedelta
import uuid

key_file_location=""
user_email=""
scopes=["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/calendar.events"]
print("hello google calendar")
with open(key_file_location) as f:
    service_data=json.loads(f.read())
credentials = service_account.Credentials.from_service_account_info(
        {
            'client_email': service_data['client_email'],
            'private_key': service_data['private_key'],
            'token_uri': service_data['token_uri'],
        },
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events'],
        subject=user_email
    )
calendar_id = "primary"

service = build('calendar', 'v3', credentials=credentials)

start_time = datetime.now() + timedelta(minutes=1)
end_time = start_time + timedelta(hours=2)

event_v1 = {
    'summary': 'Hireintel In person Interview V7',
    'description': 'This face 2 face interview from HireIntel',
    'location': 'Virtual Meeting',
    'start': {
        'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
        'timeZone': 'Asia/Kolkata',
    },
    'conferenceData': {
        'createRequest': {
            'requestId': str(uuid.uuid4()),
            'conferenceSolutionKey': {'type': 'hangoutsMeet'},
        },
    },
    'attendees': [
        {'displayName': 'HireIntel', 'email': 'x', 'organizer': True},

    ],
    'guestsCanModify':True,
    'guestsCanSeeOtherGuests':True,
}



try:
    created_event = service.events().insert(calendarId=calendar_id, body=event_v1, sendNotifications=True,
                                            conferenceDataVersion=1).execute()
    print(created_event)
    print('Event created:', created_event.get('htmlLink'))
    if 'conferenceData' in created_event:
        conferenceData=created_event['conferenceData']
        meeting_link=conferenceData['entryPoints'][0]['uri']
        print("meeting link",meeting_link)
except HttpError as error:
    print(f'Error creating event: {error}')
except RefreshError:
    print('The credentials have been revoked or expired, please re-run the application.')

