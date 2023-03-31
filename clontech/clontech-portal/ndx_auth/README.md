# Ndx Auth

This app is customised to:

* Provide an additional user type (QC User)
* Modify the forms to create & edit users

## Overview

#### App

The mobile app always connects with the same user: **mobile-app@novarumdx.com** which may not log into the portal. 

A post_migrate signal creates this user if it does not exist with a password set in envdir (or settings for test runs).

#### Portal

The portal is only accessed by staff at Takara, and "QC Users". Takara staff are called "normal users" even though they are administrators in novarum parlance.

New users are created using the same form and selecting the user type from a dropdown.

The QC users are third party Quality Control accounts, and differ as follows:

* Should only see results uploaded for QC purposes (as identified by result's uploader email being that of another QC user)
* They do not see email field in the results list
* Certain parts of the portal are off bounds (e.g. feedback, manage users)
* The edit user form which they can access from the profile page is restricted to ensure they cannot give themselves rights they shouldn't have (e.g. change their user type, receive feedback notifications).

## User Types

Clontech uses the following UserTypes:

| Name       | Comment                                                      |
| ---------- | ------------------------------------------------------------ |
| Superuser  | Only for Novarum access.                                     |
| Admin      | In Clontech administrators are called "Normal users"         |
| QC User    | Quality control. Similar to normal users but only see results for other QC users, and cannot access certain other features like user administration. |
| Mobile App | A single user of this type should be created, and this how the mobile app authenticates. This user type cannot log into the portal normally. |

## Settings

The following settings are relevant:

| Name                            | Purpose                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| NDX_AUTH_USER_CREATE_FORM       | Override the default form.                                   |
| NDX_AUTH_USER_UPDATE_FORM       | Override the default form.                                   |
| NDX_MOBILE_USER_EMAIL           | The email for the mobile user.                               |
| NDX_MOBILE_USER_PASSWORD        | The password for mobile-app user. Obtained from environment. Only required when creating mobile user first time. |
| NDX_USER_TYPES_ADMIN_GROUP_NAME | Because we call administrators "Normal users" in this portal. |
| NDX_VALID_USER_TYPES            | List of valid user types for dropdown in forms. Deliberately exclude MobileApp. |

## Signals

A post_migrate signal in **ndx_auth/apps.py** creates the mobile user account if it doesn't already exist.

You will need to set as the environment variable MOBILE_USER_PASSWORD to match the password set in the app. On the server you should set this in envdir. 

Locally you can prefix the management command:

```
MOBILE_USER_PASSWORD=xyz ./manage.py migrate
```