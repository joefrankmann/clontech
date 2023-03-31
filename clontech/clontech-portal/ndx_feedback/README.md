# Ndx Feedback

Collects user feedback from the apps.

## Standard

#### Models

Just a single simple Feedback model with data about the user and device, the feedback rating, comments and whether they want to allow follow up contact.

#### API

There is an API endpoint to create feedback entries, and another to download them as CSV for display inside the app.

#### Views

There is a view for viewing the feedback in the portal. Only portal admins (i.e. normal users) and above should be able to access this. QC users should not.

#### Permissions

Only **view_feedback**, which is used in views.

#### Settings

DEFAULT_FROM_EMAIL and SITE_NAME are used in the sending of emails.

## Special

#### Email Notifications

There is post_save signal in **signals.py** which sends emails to all users who are set to receive notifications for feedback emails (a boolean field on the user model). 

The sending of the email is handled by a celery task in **tasks.py**

