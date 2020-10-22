import datetime
from cal_setup import get_calendar_service

def list_events():
   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List 0 to 10 events')
   events_result = service.events().list(
       calendarId='primary', timeMin=now,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   if not events:
       print('No upcoming events found.')
   for event in events:
       start = event['start'].get('dateTime')
       print(start)
       
       print(start, event['summary'])
       print(event.get('id'))
       
       if start == 2020-10-19:
          print('badiya')
       else:
          print('are ky')

   

   return events

if __name__ == '__main__':
   list_events()
