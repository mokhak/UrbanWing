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

### Endpoint Description

All endpoints in the application are secured using a JWT token which is unique to each 
user. Below is a description of all the endpoints and their function.

- auth-service/authenticate: This endpoint will take in the username and password
from the request and using encryption validatte the credentials. If validated, the 
end point will return the user information.
- auth-service/createuser: This end point will take in all the information entered
in the sign up form and create a new entry in the users database with the new
user's information.
- auth-service/getuserinfo: This endpoint will take in the JWT token of the current
user and return user information.
- auth-service/getallusers: This is an Admin endpoint which will return the data for
all users that are registered in the application. 
- camera-service/upload-image: This is an Admin endpoint which will take in the user
from the list of all users that is specified, and post a random bird picture on
their dashboard. Once the image is posted, it will call the Model Service API to 
run the ML model on that particular image. 
- camera-service/get-latest-visitor: This endpoint will return the information of 
the latest image that is posted in the particular user's account.
- model-service/classify-image: This endpoint will take the image ID, and post a 
random bird classification in the database entry of that image ID. 

### How to use the application

- To use the application, open the [Application URL](https://mokhak-urbanwing.streamlit.app).
- Now click on 'Join the nest' to create a new account. Once the new account is
created, you will be logged in automatically. 
- You will see that you do not have any visitors initially. Logout of the account.
- Now login with the system admin credentials: username-sysadmin, password-sysadmin.
- Get all the users, find your account and post a picture to your account. You can 
also see the latest usage statistics in the console below. 
- Finally, log out of the admin console and log back into your account. Now, you 
should see your bird being displayed on your dashboard.
