#!flask/bin/python
from app import app
#host = '194.58.123.188'
host = 'localhost'
app.run(debug=True, host=host)
