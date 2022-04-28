from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt, generate_password_hash
bcrypt = Bcrypt(app)

#why .models.user???
from flask_app.models.user import User

@app.route('/')         #root route
def index():
    return render_template('index.html')



@app.route('/registration_form', methods= ['POST'])
def registration_form():
#validate user
#go later to add class method to if already in db
    if User.validate_registration_form(request.form) == True:
#hash password
        pw_hash = bcrypt.generate_password_hash(request.form['password'])

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
            #no confirm password b/c doesn't go to db
        }
        User.registration_create_user(data)
        flash('Congrats! You have successfully registered!')
        return redirect('/')

        #add by ryan
        session['user.id'] = User.registration_create_user(data)
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        # flash('Congrats! You have successfully registered!')
        return redirect('/success')
    return redirect('/')

    #other option to stay on same template and alert person w/ flash
    #         flash('Congrats! You have successfully registered!')
    #     # return redirect('/success')
    # return redirect('/')

    #if:ddd or if == True:
    # print(User.validate_registration_form(request.form))  
    # print('***************')
    # render_template ?? ('success.html')
    # print(request.form)
    # return ('hi')

# @app.route('/success')
# def success():
#     print ('*********')
#     return render_template ('success.html')




@app.route('/login_results', methods = ['POST'])
def login_results():
    #check if user exists via for loop
    users = User.registration_check_user_by_email(request.form)
    #needs to match one
    if len(users) != 1:
        flash('Incorrect, please check email')
        return redirect('/')

    user = users[0]

    #since user exists, check passwords  
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect, please check password')
        return redirect('/')

    #testing
    # flash('email and password are correct!')
    # return redirect('/')

    session['user.id'] = user.id #add by ryan
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email

    return redirect('/dashboard')
    # return redirect('/success')




@app.route('/logout')
def logout():
    session.clear()
    flash('Now you are logged out!')
    return redirect ('/')





# ^^^^ check if user exists (this is why we use a for loop in this class method function)
# if 0 match, user doesn't exist, if 2 or more, error
# match password?
# data in session and redirects to success page