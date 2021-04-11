<h1><b>The backend</b></h1>

<h3><b>Motivation</b></h3>

The backend is just a very simple wrapper for mongodb so that our front
end can query mongodb.  

The reason we need the backend is because we can't query
mongodb directly from the frontend due to JS running in the browser not being able to
to use any other protocols over TCP other than HTTP, Websockets, and a couple of others. Basically, MongoDb does
not use any of the supported protocols that browsers allow you to use.

<h3><b>Running the backend</b></h3>
install the dependencies: "pip3 install -r requirements.txt"  
run the server: python3 mongowrapper.py


<h3><b>querying the backend</b></h3>
Check out the API documentation by going to http://127.0.0.1:8000/docs once
you've got the backend up and running


