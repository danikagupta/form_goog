from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import datetime

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/workspaces/form_goog/.streamlit/gdrivelangchain-25468882b56f.json'

# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Authenticate using service account credentials
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Calendar API service
service = build("calendar", "v3", credentials=credentials)

# Specify the shared calendar ID
calendar_id = "amitamit@gmail.com"

# Get events from the shared calendar
now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
print("Getting the upcoming 10 events")
events_result = service.events().list(
    calendarId=calendar_id,
    timeMin=now,
    maxResults=10,
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