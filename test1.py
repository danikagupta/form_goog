from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import datetime
import streamlit as st

def get_calendar_service():
    # Path to your service account JSON key
    SERVICE_ACCOUNT_FILE = '/workspaces/form_goog/.streamlit/gdrivelangchain-25468882b56f.json'
    
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    # Create credentials using the service account file
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, 
        scopes=SCOPES
    )

    # Build and return the Calendar service
    return build('calendar', 'v3', credentials=credentials)

def get_calendar_events(event_count=10):
    try:
        service=get_calendar_service()
        # Specify the shared calendar ID
        calendar_id = "amitamit@gmail.com"

        # Get events from the shared calendar
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=event_count,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(f"{start}: {event['summary']}")
                st.write(f"SERVICE: {start}: {event['summary']}")
    except Exception as error:
        st.error(f"An error occurred: {error}")

def get_calendar_events_st(event_count=10):
    try:
        # Get the calendar service
        service = get_calendar_service()

        # Call the Calendar API
        now = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"  # 'Z' indicates UTC time
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
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

if st.button("Diagnose Calendar Access - TEST"):
    get_calendar_events()

if st.button("Diagnose Calendar Access - ST"):
    get_calendar_events_st(10)