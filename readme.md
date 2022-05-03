[![CI](https://github.com/david1992121/tool-search-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/david1992121/tool-search-engine/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/david1992121/tool-search-engine/branch/main/graph/badge.svg?token=QSWg1CKTVy)](https://codecov.io/gh/david1992121/tool-search-engine)

# Machine Tool Management Service
Web service for searching and inpecting machine tools

## Overview

- Searching of over hundreds of thousands machine tools.
- Saving and checking of inspections

## Main Features

- DRF RestAPI + MSSQL
- SimpleUI for django admin
- Swagger API Documentation

## Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/david1992121/tool-search-engine.git
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver