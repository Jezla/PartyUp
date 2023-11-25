# PartyUp

## Note
When using the PayPal checkout, you can use partyupuser@gmail.com as the email and partyuppasswor as the password.

## Tests
5 main functionalities of the system were tested: 1) login, 2) register, 3) create_checklist, 4) invite guests, 5) hire vendors. These can be found under PartyUp/PartyUpApp/tests. To run the tests, simply change directory to where manage.py exists (in the outermost PartyUp directory) and run `python manage.py test`.

## Security Modifications
To make the system more secure:  
- Instead of using Django's default secret key which is insecure according to the documentation, a new and more secure key was generated which should be replaced with the old key in the .env file. Here is the new key: `SECRET_KEY=2yf5g@f02gn4hp7@**_1c3(_8d_=gpq8#g)z@20#)7%=(9e2sf`.  
- User sessions are now timed, meaning that they get automatically logged out after 1 hour if still logged in.
- Print statements to the terminal that were created for debugging purposes are deleted.
- DB password has been set to something stronger now to protect it from unauthorised access.

## Description
This is a party planning website. The main aim of this project is to make event organisation easier both for customers and businesses in the event planning industry. As a member, after registration, you can create events, invite other users, create party playlists, and hire vendors for your events. For now, our services are limited to DJs, decoratores, venues, and MCs. As a vendor, after registration and providing your details, you can set the price for your services and directly find your customers.

## Setup
IMPORTANT: please note that the main branch on our github repository which contains the finalised version of the website is called main (and not master), so make sure you pull from the correct branch.  

The following packages are required for the PartyHub Application:  
- Django Version 4.1.1
- django-widget-tweaks Version 1.4.12
- django-phonenumbers Version 1.0.1
- django-phonenumber-field Version .0.0
- django-address Version 0.2.8
- python-decouple Version 3.6
- requests Version 2.28.1
- django-autocomplete-light Version 3.9.0

We recommend you use pip as the python package manager and a virtual environment with a requirements.txt file. First activate the virutal env by calling:

`source [path-to-environment]/myvenv/bin/activate`  

Then recursively install the packages in requirements.txt, located in the root directory (Group-16-PartyUp), by executing:

`pip install -r requirements.txt`  

For more information, see https://learnpython.com/blog/python-requirements-file/

Next, please create a .env file inside the outermost PartyUp directory and copy the following inside it:  
`SECRET_KEY=django-insecure-e=^enb)jks+g&b)mi8^r$ayl32xw53abm8(_4f58ja8yv!hcm8`   
`DEBUG=True`    
`SPOTIFY_CLIENT_SECRET=fb573dd6f7ae46e7ac9603b5354ff058`   
`SPOTIFY_CLIENT_ID=da61dc35245f4de2808e0351d29f39ba`    
`REDIRECT_URI=http://127.0.0.1:8000/spotify/redirect`    
`SPOTIFY_BASE_URL=https://api.spotify.com/v1`        
Since our team members did not want to expose their personal Google API keys, you also need to create and add your own Google API Key to the end of this file, as we are using the Google Maps API. Please use the following format:  
`GOOGLE_API_KEY=[YOUR KEY]`  
Now that your .env has been created, you can proceed to the next stage.
## How to create and connect to the database?
We are using postgreSQL as our database management tool. You can refer to settings.py in the project for full details on our database.  
First, make sure that pgsql is running on your local machine (you can use `brew services start postgresql@14` on a mac). Next, you need to set up the database and the user associated with it. You can do so by opening up the pgsql shell after running `psql -U username` and then typing the SQL command `CREATE USER partyupuser;` to create the postgres user. Finally, type in the command `CREATE DATABASE partyup OWNER partyupuser;` to create the database with partyupuser as its owner. If all steps are run successfully, you should now be able to see the database by running the command `\l`. Finally, we recommend downloading and using pgAdmin4 for easier interaction with our database. To do so, you need to register a new server on pgAdmin by right cliking on the server in the left-hand panel and choosing register > server. You can name the server anything you like, but our team has used the name local_partyup_server. Next, in the connection panel, provide `localhost` as the hostname/address and 5432 as port number. The username is just called partyupuser. Once prompted to enter the password to the database, type in mypassword, as specified in settings.py
## How to run the server?
To start the server, run the following commands:
first, from the root directory, go to the outermost PartyUp directory (ie where you created the .env file)   
`cd PartyUp`  
Then, start the server using      
`python manage.py runserver`  

If successful, you can open the website on your browser at http://127.0.0.1:8000/partyup.  
Navigate to  http://127.0.0.1:8000/admin to access the admin page. Alternatively, you will be automatically redirected to the admin page when you enter admin credentials on the website's login page.   
http://127.0.0.1:8000/partyup is the root for all the endpoints in the API. 
## How to (re)run the migrations?
After editing the database, make sure you run the following commands to create migrations.  

`python manage.py makemigrations PartyUpApp` - This will store changes to models as migrations.

`python manage.py migrate` - This will update the local database with model changes.

## Contributors
Dina Kazemi Beidokhti  
Ricardo Akkari  
Chris Ters  
Dean Diamant  
Will Qiu
 


## Aknowledgements
The document by PWC at https://www.pwc.com.au/about-us/social-impact/Privacy-Policy-Template.docx.pdf was used to write up our website's privacy policy.


