import streamlit as st
import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import json

def comprehensive_calendar_diagnostics():
    st.header("🕵️ Calendar Access Diagnostics")

    try:

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
        service = build('calendar', 'v3', credentials=credentials)

        #st.subheader("1. Service Account Details")
        #st.write(f"Email: {service_account_info['client_email']}")
        #st.write(f"Client ID: {service_account_info['client_id']}")

        st.subheader("2. Calendar List Diagnostic")
        # List all calendars
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])

        st.write(f"Total Calendars Found: {len(calendars)}")
        
        if not calendars:
            st.warning("⚠️ No calendars found. Potential access issue.")
        else:
            st.write("Available Calendars:")
            for calendar in calendars:
                st.write(f"- ID: {calendar['id']}, Summary: {calendar.get('summary', 'No Title')}")

        st.subheader("3. Primary Calendar Details")
        try:
            primary_calendar = service.calendars().get(calendarId='primary').execute()
            st.write("Primary Calendar Found:")
            st.json(primary_calendar)
        except Exception as primary_error:
            st.error(f"Error accessing primary calendar: {primary_error}")

        st.subheader("4. ACL (Access Control List) Diagnostic")
        try:
            acl = service.acl().list(calendarId='primary').execute()
            st.write("Current Sharing Permissions:")
            for rule in acl.get('items', []):
                st.write(f"- Role: {rule['role']}, Scope: {rule['scope']['type']} - {rule['scope'].get('value', 'N/A')}")
        except Exception as acl_error:
            st.error(f"Error checking ACL: {acl_error}")

    except Exception as e:
        st.error("Comprehensive Diagnostic Failed")
        st.error(f"Error: {e}")
        st.error(traceback.format_exc())

def sample_event_operations():
    st.header("🗓️ Sample Calendar Operations")

    try:
        # Reuse service account setup from previous function
        service_account_info = {
            "type": "service_account",
            "project_id": st.secrets['PROJECT_ID'],
            "private_key_id": st.secrets['PRIVATE_KEY_ID'],
            "private_key": st.secrets['PRIVATE_KEY'].replace('\\n', '\n'),
            "client_email": st.secrets['CLIENT_EMAIL'],
            "client_id": st.secrets['CLIENT_ID'],
        }

        SCOPES = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]

        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, 
            scopes=SCOPES
        )

        service = build('calendar', 'v3', credentials=credentials)

        # Create a test event
        test_event = {
            'summary': 'Diagnostic Test Event',
            'location': 'Test Location',
            'description': 'This is a test event created by diagnostic script',
            'start': {
                'dateTime': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (datetime.datetime.now() + datetime.timedelta(days=1, hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
        }

        if st.button("Create Test Event"):
            try:
                event = service.events().insert(calendarId='primary', body=test_event).execute()
                st.success(f"Test event created: {event.get('htmlLink')}")
            except Exception as event_error:
                st.error(f"Error creating test event: {event_error}")

    except Exception as e:
        st.error(f"Sample event operation failed: {e}")

# Streamlit App Layout
st.title("🔍 Google Calendar Service Account Diagnostics")

tab1, tab2 = st.tabs(["Calendar Diagnostics", "Sample Event Operations"])

with tab1:
    comprehensive_calendar_diagnostics()

with tab2:
    sample_event_operations()