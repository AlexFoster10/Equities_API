# Equities Api Project
This project allows users to interact with an equitites database via fastapi endpoints. It utilises pydantic modelling to ensure all entries meet a set criteria.

## How It's Made:

**Tech used:** Python, Fastapi, Sqlite, sqlalchemy

The project is made of a collection of Fastapi endpoints that allow a user to interact with 2 tables (instruments and prices) with a  variety of CRUD operations. Initially the project used .json files in place of a database, which allowed me to create a template for each endpoint. I then converted the storage system to a sqlite + sqlalchemy system, which greatly improved fastapi endpoint interaction. Each "object" has 4 models: actual object, the database template version, the fastapi response version and the fastapi updates requirement version. Each route uses combinations of these models to correctly store/update objects in the DB.

## Optimizations
I plan to optimise the database search as it currently uses a combination of the new sqlalchemy functions and legacy json db code. It copies all results from the instruments table to a list then searches that, but I'm aware I can just query the database directly and return on results, skipping out the legacy code entirely. 

## Lessons Learned:
This project really improved my understanding of Fastapi as a whole, it's given me a solid grasp on request validation, database persistence and API error handling. It's also made me really appreciate sqlalchemy as I initially attempted the project without it, harcoding the entire thing with sqlite cursor, which was terrible.  
