# Google Calendar REST API Integration in Django using OAuth2 Authentication

This project demonstrates how to integrate Google Calendar with a Django application using OAuth2 authentication and Django Rest Framework. It provides a set of Django Rest Framework views that handle the OAuth2 flow and retrieve calendar events from the user's Google Calendar.

The project is configured to run on ReplIt and is hosted [here](https://replit.com/@VyomVerma/Auth0GoogleCalendarIntegration). Only few email addresses are allowed as test users as the app is kept in development.

## Configuration

The following Django Rest Framework views are implemented for the Google Calendar integration:

- `GoogleCalendarInitView`: Initiates the OAuth2 flow by redirecting the user to Google's authorization page.

- `GoogleCalendarRedirectView`: Handles the OAuth2 callback from Google and retrieves the access token to access the user's Google Calendar.

### GoogleCalendarInitView ([link](https://auth0googlecalendarintegration.vyomverma.repl.co/rest/v1/calendar/init/))

The `GoogleCalendarInitView` view is responsible for starting the OAuth2 flow. When a user visits the `/rest/v1/calendar/init/` endpoint, they will be redirected to Google's authorization page. The user will be prompted to grant access to their Google Calendar. After granting access, the user will be redirected to the callback URL.

### GoogleCalendarRedirectView ([link](https://auth0googlecalendarintegration.vyomverma.repl.co/rest/v1/calendar/redirect/))

The `GoogleCalendarRedirectView` view handles the OAuth2 callback from Google. After the user is redirected from the authorization page to the callback URL (`/rest/v1/calendar/redirect/`), this view will be triggered. It retrieves the authorization code from the URL parameters and exchanges it for an access token. The access token is then used to retrieve the list of events from the user's Google Calendar.

The retrieved events are returned as JSON.