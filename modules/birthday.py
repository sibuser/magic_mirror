from datetime import datetime, timedelta
from threading import Thread

from apiclient.discovery import build
from dateutil import parser
from httplib2 import Http
from oauth2client import file, client, tools

from modules.base import BaseModule
from modules.logs import setup_logger
from settings import BIRTHDAY_UPDATE_DELAY, CALENDAR_ID

logging = setup_logger(__name__)


class Birthday(BaseModule):
    def __init__(self):
        super().__init__()
        self.thread = Thread(name=self.__class__.__name__, target=self.update)
        self.data = []
        self.new_data = []
        self.event_padding = None
        self.position_top = None

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
            self.event_padding = 0.012
            self.position_top = 0.8
            events = self.fetch_upcoming_event()
            if events:
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
        logging.info('Stopped %s...' % self.__class__.__name__)

    def move_down(self):
        self.position_top += self.event_padding

    def show_header(self):
        surface = self.font('regular', 0.008).render('Birthdays:', True, self.color)
        position = surface.get_rect(left=self.width * 0.045, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def show_date(self, event):
        start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
        today = datetime.today().day
        if start.day - today == 0 and start.month == datetime.today().month:
            msg = 'Today'
        elif start.day - today == 1 and start.month == datetime.today().month:
            msg = 'Tomorrow'
        else:
            msg = start.strftime("%d %b")
        surface = self.font('regular', 0.01).render(msg, True, self.color)
        position = surface.get_rect(left=self.width * 0.045, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def show_summary(self, event):
        surface = self.font('regular', 0.01).render(event['summary'], True, self.color)
        position = surface.get_rect(left=self.width * 0.13, top=self.height * self.position_top)
        self.new_data.append((surface, position))

    def fetch_upcoming_event(self):
        # Call the Calendar API
        try:
            now = datetime.utcnow().replace(hour=1, minute=0).isoformat() + 'Z'
            later = (datetime.today() + timedelta(days=30)).isoformat() + 'Z'
            events_result = self.service.events().list(calendarId=CALENDAR_ID,
                                                       timeMin=now,
                                                       timeMax=later,
                                                       singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                logging.info('No upcoming events found.')
                return []
            return events
        except Exception as e:
            logging.error(e)
            return []
