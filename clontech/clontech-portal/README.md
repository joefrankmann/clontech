# Clontech portal

## 1 General

### 1.1 About the portal

Clontech tests the purity of lentivirus samples, which are used to break up DNA for gene sequencing. 

Clontech is also referred to as Takara or TBUSA. 

### 1.2 Useful Links

| Description | Link                                                         |
| ----------- | ------------------------------------------------------------ |
| Confluence  | https://documents.novarumcloud.com/display/NDX357DRAFT       |
| Bitbucket   | https://code.novarumcloud.com/projects/NDX357/repos/clontech-portal |
| JIRA        | https://tasks.novarumcloud.com/projects/NDX357/summary       |
| Live        | https://gostixportal.takarabio.com/                          |
| Prelive     | https://clontech-prelive.novarumcloud.com/                   |
| Staging*    | https://clontech2-staging.novarumcloud.com                   |
| Shadow      | https://clontech.shadow.novarumcloud.com/                    |

\* Note it is **clontech2** on staging!

### 1.3 Apps

This portal contains three non-standard apps:

1. **ndx_batch** which relates to batches of the test kit
2. **ndx_eula** (different from ndx_eula in portal apps)
3. **ndx_feedback** which pertains to user feedback from the mobile app 

### 1.4 User Types

See **ndx_auth/README.md**

## 2 Technical notes

### 2.1 Installation

1. Clone from the **develop** branch (master is not sourcified, so migrations will break between master and develop).
2. Create a virtual environment with python 3.

    mkvirtualenv -p $(which python3) clontech_portal

3. Install dependencies and portal:

    pip install --upgrade -r requirements.txt
    ./setup.py develop .[tests]

4. Create local override settings (run  `./manage.py` to see a print out of where it expects to find them).
5. Run unit tests with `./test.sh`.

### 2.2 Sourcification

This portal was sourcified at version 2.0.0. This change breaks the migrations meaning you cannot use a database that was created with migrations from before 2.0.0 with code from 2.0.0 or above.

A pre sourcification database cannot be converted, instead you must:

1. Rename the old database
2. Create a new database
3. Apply django's migration scripts to create the tables
4. Run the **data_migration** command to copy the data over. 

#### 2.2.1 Running the data_migration command

With the virtualenv active run:

```
envdir envdir ./manage.py data_migration localhost port user passwd clontech_legacy /path/to/migration/reports --dry-run
```

The arguments refer to details of the old database to read data **from**, the target database is taken from django settings like any other management command. 

The **/path/to/migration/reports** is a directory where the migration reports will be dumped. These are json files mapping the IDs of records in old vs new database should you ever need them.







