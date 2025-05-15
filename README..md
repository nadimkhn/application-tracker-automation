

###  Goal

The goal of this project is deliver an interactive dashboard that tracks job application progress for users, using real-time data pulled daily using a cron job from Google Sheets.

### Automation Workflow

The system consists of a full automation pipeline developed in Python, integrating Google Sheets and Looker Studio:

1. Users log job applications into a structured Google Sheet (e.g., columns: Date, Company, Role, etc.)
2. A Python script automates the following:
    - Authenticates via Google Service Account
    - Pulls the latest data from [Google Sheets](https://docs.google.com/spreadsheets/d/1Y8VlU05ekfbwExSMjp0fuCxXJOgKMyvtCUt3c3jFfIc/edit?gid=0#gid=0)
    - Cleans and transforms the data
    - Writes the transformed data to a new (or existing) Google Sheet
3. The pipeline is scheduled to run automatically every day at 1:00 PM using a CRON job. This ensures the dashboard reflects the most up-to-date job application data without requiring manual execution.
4. The cleaned sheet is connected to Looker Studio as a live data source, powering a fully interactive dashboard which can be viewed with this [link](https://lookerstudio.google.com/reporting/4859dc74-f96e-4b54-9009-c158070a4045).

### Chart Guide

1. Applications Today - Total number of applications submitted today
2. Daily Average - Average number of applications per day over date range selected
3. Total Applications - Cumulative total of all submissions in the Sheet
4. Previous Week Trends - Trend over the date range showing how many applications were submitted each day
5. Most Recent Applications - A rolling table of the 10 most recent application entries in the date range selected

### Follow-Up Action Items

1. Job title grouping via clustering
2. Add weekly target metric
3. Progress bars for daily & weekly targets