
import os
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.auth.transport.requests
import requests

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_auth_url(user):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": ["https://yourdomain.com/api/calendar/google-callback/"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = "https://yourdomain.com/api/calendar/google-callback/"
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    return auth_url

def handle_google_callback(user, code):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": ["https://yourdomain.com/api/calendar/google-callback/"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=GOOGLE_SCOPES
    )
    flow.redirect_uri = "https://yourdomain.com/api/calendar/google-callback/"
    flow.fetch_token(code=code)
    # Store credentials (flow.credentials) securely per user
    # Example: user.profile.google_token = flow.credentials.to_json()
    # user.profile.save()

def push_events_to_google(user, events):
    # Load credentials from user profile
    credentials = getattr(user, 'google_credentials', None)
    if credentials:
        service = build('calendar', 'v3', credentials=credentials)
        for event in events:
            service.events().insert(calendarId='primary', body=event).execute()
    # Sync with external LMS (Moodle)
    try:
        moodle_url = 'https://lms.uzuriuniversity.ac.ke/webservice/rest/server.php'
        token = getattr(user, 'moodle_token', None)
        if token:
            for event in events:
                payload = {
                    'wstoken': token,
                    'wsfunction': 'core_calendar_create_calendar_events',
                    'moodlewsrestformat': 'json',
                    'events[0][name]': event.get('summary'),
                    'events[0][timestart]': event.get('start', {}).get('dateTime'),
                }
                requests.post(moodle_url, data=payload)
    except Exception:
        pass

def pull_events_from_google(user):
    # Load credentials from user profile
    credentials = getattr(user, 'google_credentials', None)
    events = []
    if credentials:
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
    # Sync events from LMS (Moodle)
    try:
        moodle_url = 'https://lms.uzuriuniversity.ac.ke/webservice/rest/server.php'
        token = getattr(user, 'moodle_token', None)
        if token:
            payload = {
                'wstoken': token,
                'wsfunction': 'core_calendar_get_calendar_events',
                'moodlewsrestformat': 'json',
            }
            resp = requests.post(moodle_url, data=payload)
            lms_events = resp.json().get('events', [])
            events.extend(lms_events)
    except Exception:
        pass
    return events

# Similar scaffolding for Outlook (Microsoft Graph) can be added here
