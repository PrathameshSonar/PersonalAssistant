from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(dt, summary):
   # creates one hour event for given date and time and summary
   service = get_calendar_service()

   d = datetime.now().date()
   
   start = dt.isoformat()
   end = (dt + timedelta(hours=1)).isoformat()   

   event_result = service.events().insert(calendarId='primary',
       body={
           "summary": summary,
           "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
           "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
       }
   ).execute()


#if __name__ == '__main__':
#   create_event(dt)
