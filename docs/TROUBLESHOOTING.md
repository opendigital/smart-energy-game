# Troubleshooting the Otree App on Heroku

## Heroku "Static Files" Error

OTREE REQUIRES STATIC FILES TO BE COLLECTED IN THE SAME DIRECTORY WHEN
RUNNING IN PRODUCTION. IF THIS IS NOT DONE FIRST SETTING `OTREE_PRODUCTION`
WILL CAUSE A FATAL ERROR ON THE HEROKU SERVERS SINCE THEY ARE 'READ-ONLY'
THE OTREE APP CANNOT WRITE FILES TO DISK THAT ARE NOT ENTERED THROUGH GIT

```sh
otree collectstatic
```

## Set the App Auth Level

```
export OTREE_AUTH_LEVEL=STUDY
```

## DATABASE MIGRATION ERRORS

THIS ONE COMES UP PRETTY OFTEN IF YOU ARE MAKING ANY CHANGES TO THE GAME
MODELS. BEFORE DEPLOYING TO THE PRODUCTION SERVER MAKE SURE YOU DOWNLOAD
ANY OF THE DATA EXPORT FILES THAT YOU ARE INTERESTED IN, IT IS VERY LIKELY
THAT THE SERVER WILL REQUIRE A MANUAL DB RESET AFTER BUILDING THE NEW APP
VERSION.

**IF YOU ARE READY TO RESET THE DATABASE RUN THE FOLLOWING COMMAND**

```sh
heroku run 'cd app && otree resetdb'
```

NOTE: IF YOU HAVE ALREADY DEPLOYED A NEW VERSION AND SEE THE ERROR SCREEN
ON THE MAIN PAGE, YOU CAN GO BACK TO THE HEROKU DASHBOARD AND 'ROLLBACK'
TO THE PREVIOUS VERSION VERY QUICKLY. ONCE YOU'VE DONE THIS, REMEMBER TO
EXPORT THE LATEST DATA. AFTER THAT YOU CAN ROLL FORWARD AGAIN, AND RUN
DATABASE RESET COMMAND.

TO CHECK THE SERVER LOGS ON THE HEROKU YOU CAN USE THE HEROKU-CLI UTILITY  
FROM THE ANYWHERE INSIDE THE PROJECT FOLDER.

## Heroku Logs


## WORKING PATHS

THE MAIN APP IS INSTALLED IN A SUBDIRECTORY OF THE MAIN FOLDER TO KEEP BUILD FILES NOTES AND DEVELOPMENT SCRIPTS OUT OF THE PATHS WHERE THEY MIGHT ACCIDENTALLY BE SERVED OR EXECUTED REMOTELY, ALSO THIS PROVIDES A CLEANER PROJECT STRUCTURE.

THIS DOES CAUSE SOME OF THE MANAGEMENT COMMANDS TO EXECUTE IN THE WRONG DIRECTORY. IF A HEROKU COMMAND FAILS TO RUN OR RETURNS NO RESULT, TRY CHANGING DIR TO THE APP FOLDER AND CHAINING THE COMMANDS.

NOTE: PAY ATTENTION TO QUOTATIONS, THE EXECUTABLE STATEMENT MUST BE SENT TO THE HEROKU SERVICE AS A SINGLE STRING, IF YOU UNESCAPE PARTS THEN IT WILL NOT RUN AS EXPECTED

### EXAMPLE:

__FAILS "-al" is unknown__

```sh
# --------------
# FAILS
# --------------

$> heroku run 'ls -al'
   Running ls on ⬢ l... !
   ▸   Couldn\'t find that app.

# --------------
# WRONG FOLDER
# --------------

$> heroku run 'ls -al'
  drwx------  9 u28374 dyno   4096 Mar 24 12:02 app
  drwx------  2 u28374 dyno   4096 Mar 24 12:02 .bin
  drwx------  2 u28374 dyno   4096 Mar 24 12:02 dist
  -rw-------  1 u28374 dyno    186 Mar 24 12:02 .gitignore
  drwx------  4 u28374 dyno   4096 Mar 24 12:04 .heroku
  -rw-------  1 u28374 dyno   1573 Mar 24 12:02 LICENSE
  -rw-------  1 u28374 dyno   1115 Mar 24 12:02 package.json
  -rw-------  1 u28374 dyno 158948 Mar 24 12:02 package-lock.json
  -rw-------  1 u28374 dyno     81 Mar 24 12:02 Procfile
  drwx------  2 u28374 dyno   4096 Mar 24 12:04 .profile.d
  -rw-------  1 u28374 dyno  15661 Mar 24 12:02 .pylintrc
  -rw-------  1 u28374 dyno   1440 Mar 24 12:02 README.md
  -rw-------  1 u28374 dyno     20 Mar 24 12:02 requirements_base.txt
  -rw-------  1 u28374 dyno     51 Mar 24 12:02 requirements_dev.txt
  -rw-------  1 u28374 dyno    133 Mar 24 12:02 requirements.txt
  -rw-------  1 u28374 dyno     12 Mar 24 12:03 runtime.txt
  drwx------  2 u28374 dyno   4096 Mar 24 12:02 src
```

```sh
# --------------
#   CORRECT
# --------------
$> heroku run 'cd app && ls -al'

  drwx------ 4 u16731 dyno 4096 Mar 24 12:02 game
  -rw------- 1 u16731 dyno  261 Mar 24 12:02 manage.py
  -rw------- 1 u16731 dyno   61 Mar 24 12:02 Procfile
  drwx------ 4 u16731 dyno 4096 Mar 24 12:02 quiz
  -rw------- 1 u16731 dyno   20 Mar 24 12:02 requirements_base.txt
  -rw------- 1 u16731 dyno  133 Mar 24 12:02 requirements.txt
  drwx------ 2 u16731 dyno 4096 Mar 24 12:02 _rooms
  -rw------- 1 u16731 dyno 2447 Mar 24 12:02 settings.py
  drwx------ 4 u16731 dyno 4096 Mar 24 12:02 _static
  drwx------ 4 u16731 dyno 4096 Mar 24 12:02 survey
  drwx------ 5 u16731 dyno 4096 Mar 24 12:02 _templates
  drwx------ 7 u16731 dyno 4096 Mar 24 12:02 __temp_static_root
```
