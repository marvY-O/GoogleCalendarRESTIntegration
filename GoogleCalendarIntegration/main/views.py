from django.http import HttpResponse
from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

#Client configuration
CLIENT_CONFIG = {
  'web': {
    'client_id': settings.GOOGLE_CLIENT_ID,
    'project_id': settings.GOOGLE_PROJECT_ID,
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://www.googleapis.com/oauth2/v3/token',
    'auth_provider_x509_cert_url':
    'https://www.googleapis.com/oauth2/v1/certs',
    'client_secret': settings.GOOGLE_CLIENT_SECRET,
    'redirect_uris': settings.GOOGLE_REDIRECT_URIS,
  }
}

#Scopes of the service
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


@api_view(['GET'])
def GoogleCalendarInitView(request):
  """
    Initiates the OAuth2 flow for Google Calendar integration.

    This view redirects the user to Google's authorization page to grant
    permission for accessing their Google Calendar. After successful
    authorization, the user will be redirected to the callback URL.

    Returns:
        A redirect response to Google's authorization page.

    Raises:
        None
  """

  #Configuring Client
  flow = Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=SCOPES)
  flow.redirect_uri = 'https://auth0googlecalendarintegration.vyomverma.repl.co/rest/v1/calendar/redirect/'

  authorization_url, state = flow.authorization_url(
    access_type='offline', include_granted_scopes='true')
  request.session['oauth_state'] = state

  return redirect(authorization_url)


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
  """
    Handles the OAuth2 callback for Google Calendar integration.

    This view is responsible for exchanging the authorization code received
    from Google's authorization page for an access token. It then uses the
    access token to retrieve the list of events from the user's Google Calendar.

    Returns:
        An JSON response containing the list  of calendar events.

    Raises:
        None
    """
  state = request.session.pop('oauth_state', '')
  if state != request.GET.get('state', ''):
    pass

  flow = Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=SCOPES)
  flow.redirect_uri = 'https://auth0googlecalendarintegration.vyomverma.repl.co/rest/v1/calendar/redirect/'

  flow.fetch_token(authorization_response=request.build_absolute_uri())
  credentials = flow.credentials

  #Refresh the token if it has expired
  if credentials.expired:
    credentials.refresh(Request())

  #Call the callendar service
  service = build(serviceName='calendar',
                  version='v3',
                  credentials=credentials,
                  static_discovery=False)

  #Fetch all events
  events = service.events().list(calendarId='primary').execute()

  #JSON Reponse with items in the events
  return Response({"events": events['items']})

