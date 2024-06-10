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

    
    def authentication(self):
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
        
        return creds

    @match_regex(r"What are my next 2 upcoming events?")
    async def upcomingEvents(self, message):
        try:
            creds = self.authentication()
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = dt.datetime.utcnow().isoformat() + "Z"  
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
            else:
                response = f"The two upcoming events are:"
                for i, event in enumerate(events, start=1):
                    start_dt = dt.datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date"))).astimezone()
                    end_dt = dt.datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date"))).astimezone()
                    
                    start_time = start_dt.strftime("%H:%M")  
                    end_time = end_dt.strftime("%H:%M") 
                    summary = event["summary"]

                    if start_time == "00:00" and end_time == "00:00":
                        response += f"\n {i} Today is: {summary}"
                    else:
                        response += f"\n {i}. At {start_dt.strftime('%A %d %B %Y')}-{start_time}-{end_time} you have {summary}."

            await message.respond("{}".format(response))  

        except HttpError as error:
            response = (f"An error occurred: {error}")

    
    @match_regex(r"Give me my events on (\d{2}-\d{2}-\d{4})$")
    async def eventDetails(self, message):
        try:
            creds = self.authentication()
            date_str = message.regex.group(1)
            service = build("calendar", "v3", credentials=creds)
            date = dt.datetime.strptime(date_str, "%d-%m-%Y").date()
            start_of_day = dt.datetime.combine(date, dt.time.min).isoformat() + 'Z'
            end_of_day = dt.datetime.combine(date, dt.time.max).isoformat() + 'Z'

            # Call the Calendar API
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_of_day,
                    timeMax=end_of_day,
                    maxResults=100,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                response = "No upcoming events found."
            else:
                response = f"Events on {date.strftime('%A %d %B %Y')}:"
                for i, event in enumerate(events, start=1):
                    start_dt = dt.datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date"))).astimezone()
                    end_dt = dt.datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date"))).astimezone()
                    
                    start_time = start_dt.strftime("%H:%M") 
                    end_time = end_dt.strftime("%H:%M")  
                    summary = event["summary"]

                    if start_time == "00:00" and end_time == "00:00":
                        response += f"\n {i} Today is: {summary}"
                    else:
                        response += f"\n {i}. At {start_time}-{end_time} you have {summary}."

            await message.respond("{}".format(response)) 

        except HttpError as error:
            response = (f"An error occurred: {error}")