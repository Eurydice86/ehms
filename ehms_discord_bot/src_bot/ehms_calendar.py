
import os
import datetime
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("ehms.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_competitions():
    calendar_id = "c_3fcf293943683058b4b1e9f2e61932d735dc20a0f6059f5fb7d012c6323c0507@group.calendar.google.com"
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now().isoformat() + "Z"
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        message = "No upcoming events"
        return message
    message = ""
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        if "location" in event.keys():
            message += f"{start}: **{event["summary"]}** _({event["location"]})_\n"
        else:
            message += f"{start}: **{event["summary"]}**\n"

    return message, events


def get_events():
    calendar_id = "c_188dc8369c19294909a6d9b5b58acbd1f0a83bfa55e9fcf49648d80c1b681f25@group.calendar.google.com"
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.datetime.now().isoformat() + "Z"
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    if not events:
        message = "No upcoming events"
        return message
    message = ""
    for event in events:
        if not event["start"].get("dateTime"):
            start = event["start"].get("date")
        else:
            start = event["start"].get("dateTime").split("T")[0]
    
        if "location" in event.keys():
            message += f"{start}: **{event["summary"]}** _({event["location"]})_\n"
        else:
            message += f"{start}: **{event["summary"]}**\n"

    return message, events


if __name__ == "__main__":
    m = get_events()[0]
    n = get_competitions()[0]
    print(m)
    print()
    print(n)
