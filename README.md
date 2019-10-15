# user_dashboard

I’ve created numerous projects throughout my coding development. One of my bigger projects, which I completed independently is a user dashboard very similar to Facebook’s Timeline feature. This project was completed in Python utilizing Django as a framework. 

The first portion of the project consisted of creating a login and registration.

The Registration: 

The user inputs their information, I verify that the information is correct, insert it into the database and return back with a success message. If the information is not valid, redirect to the registration page and show the following requirements:

Validations and Fields to Include:

1.	First Name - letters only, at least 2 characters and that it was submitted
2.	Last Name - letters only, at least 2 characters and that it was submitted
3.	Email - Valid Email format, and that it was submitted
4.	Password - at least 8 characters, and that it was submitted
5.	Password Confirmation - matches the password

The Login: 

When the user initially registers, we would log them in automatically, but the process of "logging in" is simply just verifying that the email and password the user is providing matches up with one of the records that I have in my database table for users. I created a database with MySQL so I can insert records, retrieve records from a database and set a session/flash for any error or success messages that we get along the way. 

I created a session variable that holds the user's id, which is all I need to access all the information associated with that user.

In Summary:

1.	I created a basic login and registration form
2.	Redirect the user to a success page on successful login and register
3.	Display error messages if either login or registration validations fail
4.	Use md5 to hash passwords before inserting them into the database

Once a user is successfully registered and logged in, they can now interact with other users in the database through messages. The Django framework uses routes, views, redirects, and rendering. I created an app called “userdash” and relayed information between the controller/view (found in views.py) to handle session and POST data. In the views.py you can see methods that render/redirects:

1.	Login/Registration 
2.	Updating user information (name, e-mail, password)
3.	Adding/removing/editing a message to the dashboard
4.	Adding/removing/editing users 

