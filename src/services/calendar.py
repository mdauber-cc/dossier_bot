import datetime as dt, json, base64, google.oauth2.service_account
from googleapiclient.discovery import build
from src.services.db import get_conn
from src.config import settings

def log_todays_events():
    creds = google.oauth2.service_account.Credentials.from_service_account_info(
        json.loads(base64.b64decode(settings.google_sa_json)),
        scopes=["https://www.googleapis.com/auth/calendar.readonly"])
    svc = build('calendar', 'v3', credentials=creds)
    now = dt.datetime.utcnow().isoformat()+'Z'
    end = (dt.datetime.utcnow()+dt.timedelta(days=1)).isoformat()+'Z'
    evs = svc.events().list(calendarId='primary', timeMin=now, timeMax=end,
                            singleEvents=True).execute().get('items', [])
    with get_conn() as conn:
        for e in evs:
            attendees = [a['email'] for a in e.get('attendees', [])
                         if a.get('responseStatus') != 'declined']
            conn.execute("""
                insert into events(id, start_ts, attendees)
                values ($1, $2, $3)
                on conflict (id) do update set attendees = excluded.attendees
            """, e['id'], e['start']['dateTime'], json.dumps(attendees))
    return len(evs)