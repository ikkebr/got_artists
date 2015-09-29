===============================
Got_Artists
===============================

Implement a simple search service (complete with suitable test coverage) using a suitable Python web framework (micro frameworks welcome). The purpose is to find artists that match an age range (minimum to maximum) where results are ordered and returned by best fit. The best fit algorithm is open to your choice, but should favour artists with ages in the middle of the range over those at the edge of the range. The output from the search function should be a JSON encoded structure with a list of matching artist UUIDs and ages. The dataset is in the attached 'artists.json' file.


Requirements
----

MongoDB

Python

Flask


Setup & Installation
----

Clone the repository into a virtualenv and execute the following to get it up and running.

 **$ mongoimport.exe -v -d got_artists -c artists --jsonArray artists.json**
 
 **$ pip install -r requirements.txt **
 
 **$ python got_artists.py
 
 

What has been implemented?
----

Simple search service, using Flask and MongoDB. I implemented a simple form so testing can be done easily.
