# Opsdroid skill Google Calendar
A skill for Opsdroid that connects to your Google Calendar to display 
1. Your upcoming events
2. Your events for a specific day

Use this as a foundation for creating more Google Calendar skills, such as adding new events, and more!

## Requirements
- Have a Google account with Google Calendar enabled.
- Create your Google Cloud project. Follow the steps you will see [here](https://developers.google.com/workspace/guides/create-project)
- [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com) on your Google Cloud project.
- Configure the OAuth consent screen:
    1. In the Google Cloud console, go to Menu menu > APIs & Services > [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).
    2. For User type select Internal, then click Create.
    3. Complete the app registration form, then click Save and Continue.
    4. For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside of your Google Workspace organization, you must change the User type to External, and then, add the authorization scopes that your app requires.
    5. Review your app registration summary. To make changes, click Edit. If the app registration looks OK, click Back to Dashboard.
- Authorize credentials for a desktop application
    1. In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.
    2. Click Create Credentials > OAuth client ID.
    3. Click Application type > Desktop app.
    4. In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
    5. Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
    6. Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
    7. Save the downloaded JSON file as credentials.json, and move the file to your working directory.
- Install the Google client library
~~~
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
~~~
## Configuration
```yaml
googlecalendar:
    path: # your local path to __init__.py
    creds_path: # your path to credentials.json
```
## Usage

### 1.  `What are my next 2 upcoming events?`

> user: What are the upcoming 2 events?

> Opsdroid: Your two upcoming events are:
>
> 1. At Tuesday 11 June 2024-13:30-14:30 you have Yoga Session. 
>
> 2. At Wednesday 12 June 2024-16:00-17:00 you have Meeting with partners.

### 2. `Give me my events on 10-07-2024`

> Opsdroid: Events on Wednesday 10 July 2024:
>
> 1. At 16:00-17:00 you have Doctor Appointment.
>
> 2. At 22:00-23:00 you have Meeting at work.


