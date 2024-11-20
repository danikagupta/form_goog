import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

def get_calendar_service():
    # Path to your service account JSON key
    SERVICE_ACCOUNT_FILE = '/workspaces/form_goog/.streamlit/gdrivelangchain-25468882b56f.json'
    
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    # Create credentials using the service account file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=SCOPES
    )

    # Build and return the Calendar service
    return build('calendar', 'v3', credentials=credentials)

def get_calendar_events(event_count=10):
    try:
        # Get the calendar service
        service = get_calendar_service()

        # Call the Calendar API
        now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"  # 'Z' indicates UTC time
        st.write(f"IN get-calendar-events, now: {now}")
        events_result = (
            service.events()
            .list(
                calendarId="amitamit@gmail.com",
                timeMin=now,
                maxResults=event_count,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # Display events in Streamlit
        if not events:
            st.write("No upcoming events found.")
            return

        # Create a list to store event details
        event_details = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_details.append(f"{start}: {event.get('summary', 'No title')}")
        
        # Display events in Streamlit
        st.write("Upcoming Events:")
        for event in event_details:
            st.write(event)

    except Exception as error:
        st.error(f"An error occurred: {error}")

def add_event_to_calendar(event_title, start_time, end_time, attendee_email):
    try:
        # Get the calendar service
        service = get_calendar_service()

        # Create event details
        event = {
            "summary": event_title,
            "start": {
                "dateTime": start_time,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "UTC"
            },
            "attendees": [{"email": attendee_email}]
        }

        # Insert the event
        created_event = service.events().insert(calendarId="amitamit@gmail.com", body=event).execute()
        st.success(f"Event created: {created_event.get('htmlLink')}")

    except Exception as error:
        st.error(f"An error occurred: {error}")

# Streamlit UI
st.title("Google Calendar Service Account Integration")

# Get Events Button
if st.button("Fetch Calendar Events"):
    get_calendar_events(10)

# Add Event Form
st.header("Add New Event")
event_title = st.text_input("Event Title")
start_time = st.text_input("Start Time (YYYY-MM-DDTHH:MM:SSZ)", help="Format: 2024-11-21T14:00:00Z")
end_time = st.text_input("End Time (YYYY-MM-DDTHH:MM:SSZ)", help="Format: 2024-11-21T15:00:00Z")
attendee_email = st.text_input("Attendee Email")

if st.button("Create Event"):
    if event_title and start_time and end_time and attendee_email:
        add_event_to_calendar(event_title, start_time, end_time, attendee_email)
    else:
        st.warning("Please fill in all fields")
