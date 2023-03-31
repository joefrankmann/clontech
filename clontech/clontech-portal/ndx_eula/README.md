# NDX_EULA

This is a custom app from clontech before sourcification and is different to ndx_eula in shadow apps.

### Overview

This portal only uses EULAs for users accessing the app, not the portal. Users must approve the EULA before they can use the app.

EULAs are dated, and the current EULA is determined as the latest one that is not in the future. This allows portal users to create future dated EULAs which will automatically activate when the EULA's date is reached.

### Models

The **Eula** has *valid_from* and *is_active*. It has a one to many relation with **EulaFile** which has fields *locale* (e.g. EN, pt_Bz) and the *eula_file* (an upload).