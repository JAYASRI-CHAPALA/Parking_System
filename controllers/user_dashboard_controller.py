from flask import render_template , url_for, redirect , flash ,request
from models.models import ReserveParkingSpot , db , Users
from flask_login import current_user , login_required
from sqlalchemy import and_ , func
from forms import UserEditForm , PasswordUpdateForm
from werkzeug.security import check_password_hash,generate_password_hash

@login_required
def userDashboard():
    user_reservations = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id()).all()
    total_reservations = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id()).count()

    current_bookings = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id(),payment_status ='Pending').all()
    active_bookings = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id(),payment_status ='Pending').count()

    booking_history = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id(),payment_status ='Success').all()
    completed_bookings = ReserveParkingSpot.query.filter_by(user_id = current_user.get_id(),payment_status ='Success').count()

    total_amout_paid = round(db.session.query(func.sum(ReserveParkingSpot.amount_paid)).filter_by(user_id = current_user.get_id(),payment_status='Success').scalar() or 0,2)
    avg_amount_paid = round(db.session.query(func.avg(ReserveParkingSpot.amount_paid)).filter_by(user_id = current_user.get_id(),payment_status='Success').scalar() or 0,2)
    max_amout_paid = round(db.session.query(func.max(ReserveParkingSpot.amount_paid)).filter_by(user_id = current_user.get_id(),payment_status='Success').scalar() or 0,2)

    durations = [(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600 for r in booking_history]
    total_parking_time = round(sum(durations), 2)
    avg_parking_duration = round(sum(durations)/len(durations), 2) if durations else 0
    longest_parking_duration = round(max(durations), 2) if durations else 0
    
    
    return render_template('user-dashboard.html', 
                           user_reservations = user_reservations ,
                           current_bookings = current_bookings,
                           booking_history = booking_history,
                           total_reservations = total_reservations,
                           active_bookings = active_bookings,
                           completed_bookings = completed_bookings,
                           total_amout_paid = total_amout_paid,
                           avg_amount_paid = avg_amount_paid,
                           max_amout_paid = max_amout_paid,
                           total_parking_time = total_parking_time,
                           avg_parking_duration = avg_parking_duration,
                           longest_parking_duration = longest_parking_duration
                           )

@login_required
def editUser(user_id):
    user = Users.query.filter_by(id = user_id).first()
    # print(type(edit_user.id) , type(current_user.get_id()))
    form = UserEditForm()
    if user.id == int(current_user.get_id()):

        if request.method == 'POST' and form.validate_on_submit():
            # Update user details
            user.fullname = form.fullname.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.pincode = form.pincode.data
            user.address = form.address.data

            db.session.commit()
            flash('Profile Updated Successfully', 'success')
            return redirect(url_for('home'))

        elif request.method == 'GET':
            # Pre-fill form on GET request
            form.fullname.data = user.fullname
            form.email.data = user.email
            form.phone.data = user.phone
            form.pincode.data = user.pincode
            form.address.data = user.address

        return render_template('edit-user.html', form=form)

    else:
        flash('User Authentication Failed')
        return redirect(url_for('home'))
    
@login_required
def passwordUpdate(user_id):
    if user_id == current_user.get_id():
        form = PasswordUpdateForm()
        if form.validate_on_submit():
            oldpassword = form.oldpassword.data
            password = form.password.data
            # confirm_password = form.confirm_password.data
            user = Users.query.filter_by(id = current_user.get_id()).first()
            if  user and check_password_hash(user.password , oldpassword):
                user.password = generate_password_hash(password)
                db.session.commit()
                flash('Password Updated successfully','success')
                return redirect('userdashboard')
            else :
                flash('old Password mismatch','warning')
                return redirect(url_for('passwordupdate', user_id = current_user.get_id()))
        return render_template('password-update.html' , form = form)
    else :
        flash('Unauthorized Access','danger')
        return redirect(url_for('userdashboard'))
        