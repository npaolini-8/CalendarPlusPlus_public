# CalendarPlusPlus
CalendarPlusPlus is a format agnostic calendar web application written in Flask. It provides a basic calendar that anyone can use.
It provides quality of life additions to a typical calendar such as an import or export system to make transition easy
and comparing schedules to allow for group event scheduling.

It currently is in a very basic stage in development.

## Features
- Day, Week, Month calendars
- User Accounts
- Mutual friend system
- Import/Exporting calendars in different formats
- Event tracking
- Free time comparison

## Running the app for development
#### Cloning and getting requirements
```
git clone https://github.com/JehuA/CalendarPlusPlus.git 
pip (or pip3) install -r requirements.txt
```


#### Flask Setup
Follow the initial Flask setup, otherwise simply running app.py should allow you to run this locally
```
https://flask.palletsprojects.com/en/2.0.x/tutorial/factory/#run-the-application
```

### Supported Files
- ICS (Widely used by most popular calendar apps)
- iCal (Deprecated calendar file format, only imports for legacy)
- CSV (Custom CSV layout, recommended exporting an existing calendar first for an example)


### Contributors
- Jehu Ananoria
- Swanora Campbell
- Nick Paolini
- Jonathan Witkowski
- Taylor Gould
