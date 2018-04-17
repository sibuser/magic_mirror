import datetime
import logging
from datetime import datetime
from threading import Thread

from apiclient.discovery import build
from dateutil import parser
from httplib2 import Http
from oauth2client import file, client, tools

from modules.base import BaseModule
from settings import BIRTHDAY_UPDATE_DELAY, CALENDAR_ID


class Birthday(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.update)
        self.data = []
        self.new_data = []
        self.event_padding = 0.03
        self.position_top = 0.3

        # Setup the Calendar API
        scopes = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', scopes)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))

    def update(self):

        while not self.shutdown:
            self.event_padding = 0.03
            self.position_top = 0.3
            events = self.fetch_upcoming_event()

            self.show_header()
            self.move_down()
            for event in events:
                self.show_date(event)
                self.show_summary(event)
                self.move_down()

            self.data.clear()
            self.data = self.new_data[:]
            self.new_data.clear()

            logging.debug("Completed updating %s..." % self.__class__.__name__)
            self.sleep(BIRTHDAY_UPDATE_DELAY)

    def move_down(self):
        self.position_top += self.event_padding

    def show_header(self):
        surface = self.font('regular', 0.025).render('Upcoming Birthdays', True, self.color)
        position = surface.get_rect(left=self.width / 100, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def show_date(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        surface = self.font('regular', 0.025).render(parser.parse(start).strftime("%d %B"), True,
                                                     self.color)
        position = surface.get_rect(left=self.width / 100, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def show_summary(self, event):
        surface = self.font('regular', 0.025).render(event['summary'], True,
                                                     self.color)
        position = surface.get_rect(left=self.width / 10, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def fetch_upcoming_event(self):
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=CALENDAR_ID,
                                                   timeMin=now,
                                                   maxResults=10,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            logging.info('No upcoming events found.')
            return []
        return events
