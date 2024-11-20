
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import traceback

def get_calendar_service():
    try:
        # Load service account from Streamlit secrets
        SERVICE_ACCOUNT_FILE = '/workspaces/form_goog/.streamlit/gdrivelangchain-25468882b56f.json'
        # Scopes with explicit calendar access
        SCOPES = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=SCOPES
        )

        # Build Calendar service
        return build('calendar', 'v3', credentials=credentials)
    except Exception as e:
        st.error(f"Error creating service: {e}")
        st.error(traceback.format_exc())
        return None

def get_calendar_events(event_count=10):
    try:
        # Get the calendar service
        service = get_calendar_service()
        if not service:
            st.error("Could not create calendar service")
            return

        # List available calendars to verify access
        calendar_list = service.calendarList().list().execute()
        st.write("Available Calendars:")
        for calendar_entry in calendar_list['items']:
            st.write(f"Calendar ID: {calendar_entry['id']}, Summary: {calendar_entry['summary']}")

        # Try to access primary calendar
        now = datetime.datetime.utcnow().isoformat() + "Z"
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

        # Display events
        if not events:
            st.write("No upcoming events found.")
            return

        st.write("Upcoming Events:")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            st.write(f"{start}: {event.get('summary', 'No title')}")

    except Exception as error:
        st.error(f"An error occurred: {error}")
        st.error(traceback.format_exc())

# Streamlit UI
st.title("Google Calendar Troubleshooter")

if st.button("Diagnose Calendar Access"):
    get_calendar_events(10)

def advanced_diagnostics():
    try:
        service = get_calendar_service()
        
        # Print service account details
        #st.write("Service Account Email:", st.secrets['CLIENT_EMAIL'])
        
        # Check available calendars
        calendar_list = service.calendarList().list().execute()
        st.write("Total Calendars:", len(calendar_list.get('items', [])))
        
        # Try to get primary calendar details
        primary_calendar = service.calendars().get(calendarId='primary').execute()
        st.write("Primary Calendar Details:")
        st.write(f"ID: {primary_calendar['id']}")
        st.write(f"Summary: {primary_calendar['summary']}")
        
    except Exception as e:
        st.error(f"Diagnostic error: {e}")
        st.error(traceback.format_exc())

# Add to Streamlit UI
if st.button("Advanced Diagnostics"):
    advanced_diagnostics()

