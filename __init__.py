from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
import os.path
import datetime as dt 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar(Skill):

    def __init__(self, opsdroid, config):
        super().__init__(opsdroid, config)
        self.creds_path = config.get("creds_path")

    @match_regex(r"What are the upcoming 2 events?")
    async def upcomingEvents(self, message):
        creds = None
        SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json")

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    
        try:
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = dt.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=2,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                response = "No upcoming events found."

            # Respond with the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                response = (start, event["summary"])
                await message.respond("{}".format(response)) 

        except HttpError as error:
            response = (f"An error occurred: {error}")
