## Django CSV Reconciliation API
This Django-based project provides an API to reconcile two CSV files (source and target) by identifying missing records and discrepancies. The API accepts two CSV files, normalizes the data, and generates a reconciliation report in various formats (CSV, HTML, JSON).

# Features
Upload two CSV files for reconciliation
Normalize data (case sensitivity, date formats, trimming spaces)
Identify records missing in the source or target file
Compare matching records for discrepancies across specific fields
Generate reports in CSV, HTML, or JSON format

# Requirements
Docker
Docker Compose
Python
Django
Pandas


# HOW TO RUN THE PROJECT
To run this project, open your terminal (preferably Linux) and run
`docker compose up`
Navigate to `http://localhost:8080/reconcile/` to access the API


API CONTRACT
TYPE: `FORM DATA`
METHOD: `POST`
PARAM: `format` ["json", "csv", "html"]
`source` (source csv), `target` (target csv)