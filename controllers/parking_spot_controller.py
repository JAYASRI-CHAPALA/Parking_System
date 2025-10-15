from flask import render_template , redirect, url_for ,flash ,request
from forms import ReserveParkingSpotForm ,ReleaseSpotForm
from datetime import datetime
from models.models import db, ReserveParkingSpot ,ParkingSpot ,ParkingLot
from flask_login import current_user
from flask_login import login_required
import math

@login_required
def reserveSpot( lot_id, spot_id):
    form = ReserveParkingSpotForm()
    form.spot_id.data = spot_id
    spot = ParkingSpot.query.filter_by(id=spot_id).first()
    form.parkingcost.data = ParkingLot.query.filter_by(id = lot_id).first().price

    if form.validate_on_submit():
        spot_id = form.spot_id.data
        parking_cost = form.parkingcost.data
        vehicle_number = form.vehicle_number.data
        id = gen_reserve_id(spot_id)
        bookspot = ReserveParkingSpot(id = id ,spot_id=spot_id, user_id= int(current_user.get_id()), parkingcost=parking_cost, vehicle_number=vehicle_number)
        if bookspot:
            db.session.add(bookspot)
            parking_spot = ParkingSpot.query.filter_by(id=spot_id).first()
            if parking_spot:
                parking_spot.status = 'O'
            else:
                flash("Error: Parking spot not found.", 'danger')
                return render_template('reserve_spot.html', form=form)
            db.session.commit()
            flash("Parking spot reserved successfully.",'info')
            return redirect(url_for('home'))  
        else:
            flash("Error: Could not reserve the parking spot.",'warning')
    return render_template('reserve-spot.html',form = form)

def gen_reserve_id(spot_id):
    user_id = current_user.get_id()
    time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"RES-{user_id}-{spot_id[8:]}-{time}"



@login_required
def releaseSpot(res_id):
    reservation = ReserveParkingSpot.query.filter_by(id=res_id).first()
    # print(type(reservation.user_id),type(current_user.get_id()))
    if reservation.user_id == int(current_user.get_id()):
        form = ReleaseSpotForm()
        totalcost = calculate_parking_cost(reservation.parking_timestamp,datetime.utcnow() , reservation.parkingcost)
        form.total_cost.data = totalcost
        form.leaving_time.data = datetime.utcnow().strftime('%I:%M %p, %d %B %Y')
        form.parking_time.data = reservation.parking_timestamp.strftime('%I:%M %p, %d %B %Y')
        form.spot_id.data = reservation.spot_id
        print(form.validate_on_submit())
        if form.validate_on_submit():
            reservation.leaving_timestamp = datetime.utcnow()
            reservation.payment_status = "Success"
            reservation.amount_paid = totalcost
            reservation.spot.status = 'A'
            db.session.commit()
            flash('Payment Success and Slot Released','success')
            return redirect(url_for('userdashboard'))
        return render_template('release-spot.html' , reservation = reservation , totalcost = totalcost , form = form)

    else:
        flash('Unexpected Error','danger')
        return redirect(url_for('userdashboard'))


# @login_required
# def releaseSpot(res_id):
#     """
#     releases spot and pays the bill amount by calculating 
#     """
#     reservation = ReserveParkingSpot.query.filter_by(id=res_id).first()
#     slot = ParkingSpot.query.filter_by(id=slot_id).first()

#     if reservation and slot:
#         reservation.leaving_timestamp = datetime.utcnow()
#         reservation.payment_status = "Success"
#         reservation.amount_paid = calculate_parking_cost(reservation.parking_timestamp,datetime.utcnow() , reservation.parkingcost)
#         slot.status = 'A'
#         db.session.commit()   
#     return redirect(url_for('userdashboard'))

def calculate_parking_cost(parkingtime , leavingtime , cost):
    if not parkingtime or not leavingtime :
        return 0.0
    duration = leavingtime - parkingtime
    total_hours = duration.total_seconds()/3600
    rounded_hours = math.ceil(total_hours)
    return rounded_hours * cost
    
    