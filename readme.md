# UrbanWing
## Bringing Nature Closer, One Featured Friend at a time.

My application was a pseudo version of a bird detection application that would pair
to your motion detection camera, have machine learning to detect the bird species, and
finally a dashboard for the user to view their visitor. 

I used various services to mimic such features. Below is a description of all the 
microservices that exist in the application.

- Auth Service: This service is responsible for user authentication, user sign up, and
also returns user data to other services as well as the admin console. 
- Camera Service: This service is responsible for posting a picture to mimic the motion
detection camera on a particular User's dashboard. The camera service will also get the 
latest entry from the database as well as call the machine learning service to run. 
- Model Service: This service mimics a machine learning model. The service is provided
with the image and it randomly generates a classification of the bird that is in the 
image and posts it to the database. 