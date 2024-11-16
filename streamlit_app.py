import streamlit as st


import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

from googleapiclient.errors import HttpError


xxx="""

CREDENTIALS_FILE='/workspaces/form_goog/.streamlit/gdrivelangchain-6dd2e3948406.json'
#CREDENTIALS_FILE='/workspaces/form_goog/.streamlit/client_secret_458566119308-cevat5h5u8grgrae4rpts73it6tikb0m.apps.googleusercontent.com.json'

FORM_ID="https://docs.google.com/forms/d/e/1FAIpQLSfhimr1pG3-R6S48ZOC_1HXxWK3sGGMaxuD3ONl7lwHe886sw/viewform?usp=sf_link"
FORM_ID="1PVJH_uHlyGSv-pKHMVR86bdsxarreIojP1bz1E9xsnA"

# Load the Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/forms", "https://www.googleapis.com/auth/calendar",
           "https://www.googleapis.com/auth/forms.body.readonly",
        "https://www.googleapis.com/auth/forms.responses.readonly",
        "https://www.googleapis.com/auth/forms.responses" ]
)
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds = Credentials(
    token=st.secrets['GCALENDAR_ACCESS_TOKEN'],
    refresh_token=st.secrets['GCALENDAR_REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=st.secrets['GCALENDAR_CLIENT_ID'],
    client_secret=st.secrets['GCALENDAR_CLIENT_SECRET'],
    scopes=['https://www.googleapis.com/auth/calendar']
)

def get_calendar_events(event_count=10):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=event_count,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


xxx="""
# Create a function to submit the Google Form
def submit_google_form(form_id, answer1, answer2, answer3):
    form_service = build("forms", "v1", credentials=credentials)
    form = form_service.forms().get(formId=form_id).execute()
    print(f"Form={form}")
    question_id1 = "QUESTION_ID_1"
    question_id2 = "QUESTION_ID_2"
    question_id3 = "QUESTION_ID_3"
    response_body = {
        "responses": [
            {"questionId": question_id1, "textAnswers": {"answers": [{"value": answer1}]}},
            {"questionId": question_id2, "textAnswers": {"answers": [{"value": answer2}]}},
            {"questionId": question_id3, "textAnswers": {"answers": [{"value": answer3}]}}
        ]
    }
    
    # Submit the form response
    #form_service.forms().responses().create(formId=form_id, body=response_body).execute()
    print(f"Form submitted successfully!: {response_body}")

    #service = build("forms", "v1", credentials=credentials)
    #form_response = {"responses": [{"value": response} for response in responses]}
    #service.forms().responses().create(formId=form_id, body=form_response).execute()
    st.success("Google Form submitted!")
"""
    
# Create a function to add an event to Google Calendar
def add_to_google_calendar(event_title, start_time, end_time,attendee_email):
    service = build("calendar", "v3", credentials=credentials)
    event = {
        "summary": event_title,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "attendees": [{"email": attendee_email}]
    }
    created_event=service.events().insert(calendarId="primary", body=event).execute()
    st.success("Event created in Google Calendar!")
    print(f"Created Event={created_event}")

def add_one_event():
    time_zone = 'America/New_York'  # Replace with your time zone

    # Event start and end times
    event_start_time = datetime.datetime(2024, 11, 21, 14, 0, 0)  # Year, Month, Day, Hour, Minute, Second
    event_end_time = event_start_time + datetime.timedelta(hours=1)  # Event duration of 1 hour

    # Format event details
    event = {
        'summary': 'Test Appointment - pl ignore',
        'location': '123 Main St, Anytown, USA',
        'description': 'A chance to hear more about our services.',
        'start': {
            'dateTime': event_start_time.isoformat(),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': event_end_time.isoformat(),
            'timeZone': time_zone,
        },
        'attendees': [
            {'email': 'amit.gupta@pyxeda.ai'},  # Replace with the user's email address
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Email reminder 24 hours before
                {'method': 'popup', 'minutes': 10},        # Popup reminder 10 minutes before
            ],
        },
    }

    try:
        service = build("calendar", "v3", credentials=creds)
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'
        ).execute()

        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Streamlit app layout
st.title("Google Form and Calendar Submission")

xxx="""

# Form inputs
st.header("Submit Google Form")
responses = st.text_input("Enter your responses (comma-separated)").split(",")

# Submit button for form
answer1 = st.text_input("Answer for Question 1")
answer2 = st.text_input("Answer for Question 2")
answer3 = st.text_input("Answer for Question 3")

if st.button("Submit Form"):
    submit_google_form(form_id="YOUR_FORM_ID", answer1=answer1, answer2=answer2, answer3=answer3)

st.divider()
"""

if st.button("Get Calendar Events"):
    get_calendar_events(10)

if st.button("Add One Event"):
    add_one_event()


xxx="""
# Calendar inputs
st.header("Create Calendar Event")
event_title = st.text_input("Event Title")
start_time = st.text_input("Start Time (YYYY-MM-DDTHH:MM:SS)")
end_time = st.text_input("End Time (YYYY-MM-DDTHH:MM:SS)")
attendee_email = st.text_input("Attendee Email","amitamit@gmail.com")


# Submit button for calendar
if st.button("Add to Calendar"):
    add_to_google_calendar(event_title, start_time, end_time,attendee_email)
"""

