import streamlit as st


import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

CREDENTIALS_FILE='/workspaces/form_goog/.streamlit/gdrivelangchain-6dd2e3948406.json'

# Load the Google Cloud credentials
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/forms", "https://www.googleapis.com/auth/calendar"]
)

# Create a function to submit the Google Form
def submit_google_form(form_id, responses):
    service = build("forms", "v1", credentials=credentials)
    form_response = {"responses": [{"value": response} for response in responses]}
    service.forms().responses().create(formId=form_id, body=form_response).execute()
    st.success("Google Form submitted!")

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

# Streamlit app layout
st.title("Google Form and Calendar Submission")

# Form inputs
st.header("Submit Google Form")
responses = st.text_input("Enter your responses (comma-separated)").split(",")

# Submit button for form
if st.button("Submit Form"):
    submit_google_form(form_id="YOUR_FORM_ID", responses=responses)

st.divider()

# Calendar inputs
st.header("Create Calendar Event")
event_title = st.text_input("Event Title")
start_time = st.text_input("Start Time (YYYY-MM-DDTHH:MM:SS)")
end_time = st.text_input("End Time (YYYY-MM-DDTHH:MM:SS)")
attendee_email = st.text_input("Attendee Email","amitamit@gmail.com")


# Submit button for calendar
if st.button("Add to Calendar"):
    add_to_google_calendar(event_title, start_time, end_time,attendee_email)


