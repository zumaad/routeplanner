for a hosted version of the api, checkout:
http://ec2-54-160-116-97.compute-1.amazonaws.com:8000/docs

<h1><b>/backend</b></h1>

Contains the code for the backend service which returns a list of 
locations a user will want to visit.
<h3><b>Motivation</b></h3>

The reason we need the backend is because we can't query
mongodb directly from the frontend due to JS running in the browser not being able to
to use any other protocols over TCP other than HTTP, Websockets, and a couple of others. Basically, MongoDb does
not use any of the supported protocols that browsers allow you to use.

<h3><b>Running the backend locally</b></h3>
Make sure you have a mongo server up and running (on the default port) as the backend needs to connect
to a mongo instance.   

Assuming you have mongo installed, run:  
<b>start the mongo server:</b> "mongod -dbpath="routeplanner/data"

<b>install the dependencies for the backend:</b> "pip3 install -r requirements.txt"  
<b>run the backend:</b> python3 api.py

<h3><b>querying the backend</b></h3>
Check out the API documentation by going to http://127.0.0.1:8000/docs once
you've got the backend up and running

<h1><b>/database</b></h1>
contains our mongo client that is used by the backend service (backend/api.py) to 
query mongodb.

<h1><b>/data</b></h1>
contains the mongo data so that you can just clone the repo
and run "mongod -dbpath="routeplanner/data" to get a local mongo 
instance running with all the necessary data

<h1><b>/overpass</b></h1>
contains our overpass client. This was used to originally
populate mongo db with the data from overpass turbo.

<h1><b>/frontend</b></h1>
contains the html and js that the user will interact with.