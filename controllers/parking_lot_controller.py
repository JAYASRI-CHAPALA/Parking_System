from flask import render_template , redirect, request,url_for ,flash
from forms import ParkingLotForm
from models.models import db , ParkingLot , ParkingSpot , Rating , ReserveParkingSpot
from datetime import datetime
from forms import IncreaseParkingSpotsForm , DecreaseParkingSpotsForm
from forms import SearchParkingLotForm
from flask_login import login_required , current_user
from forms import EditParkingLotForm , RatingForm


# add parking lot 
@login_required
def addParkingLot():
    '''
    add parking lot adds new parking lot into db on form submission which contains fields like prime_location_name, address,city,pincode,price,maximum_number_of_spots
    '''
    form = ParkingLotForm()
    if form.validate_on_submit():
        prime_location_name = form.prime_location_name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        pincode = str(form.pincode.data)
        price = float(form.price.data)
        maximum_number_of_spots = form.maximum_number_of_spots.data
        id = gen_parking_id(pincode)
        
        parkingLot = ParkingLot(id = id , prime_location_name = prime_location_name, address = address, city = city, state = state, pincode= pincode, price = price, maximum_number_of_spots = maximum_number_of_spots)
        
        if parkingLot :
            db.session.add(parkingLot)
            db.session.flush()
            for i in range(1, maximum_number_of_spots + 1):
                spot_id = f"{parkingLot.id}-SPOT-{str(i).zfill(2)}"
                parking_spot = ParkingSpot(id=spot_id, lot_id=parkingLot.id, status='A')
                db.session.add(parking_spot)
            db.session.commit()
            flash("successfully added Parking Lot" , 'success')
            return redirect(url_for('home'))
        else:
            flash("Error in adding parking lot" , 'danger')
            return render_template('add-parking-lot.html', form=form)

    parking_lots = ParkingLot.query.all()
    return render_template('add-parking-lot.html',form = form , parkingLots = parking_lots, parking_spots = ParkingSpot.query.all())


def gen_parking_id(pincode):
    count = ParkingLot.query.filter_by(pincode=pincode).count()
    year = datetime.now().year
    serial = str(count +1).zfill(3)  
    return f"PL-{year}-{pincode}-{serial}"


@login_required
def deleteParkingLot(lot_id):
    '''
    deletes the parking lot if there is no active spots in that parking lot
    params :
    lot id = str datatype
    '''
    lot = ParkingLot.query.filter_by(id=lot_id).first()

    if not lot:
        flash("Parking lot not found.", "warning")
        return redirect(url_for('admindashboard'))
    
    occupied_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').first()
    if occupied_spot:
        flash("Cannot delete parking lot. Some spots are still occupied.", "warning")
        return redirect(url_for('admindashboard'))
    
    lot.is_active = False
    db.session.commit()
    flash("Parking lot deleted successfully.", "success")
    return redirect(url_for('admindashboard'))

# edit parking lot 
def editParkingLot(lot_id):
    '''
    edits parking lot by taking the details of parking lot
    '''
    parking_lot = ParkingLot.query.filter_by(id= lot_id).first()  
    form = EditParkingLotForm(obj = parking_lot)

    if form.validate_on_submit():
        if form.address.data:
            parking_lot.address = form.address.data

        if form.price.data is not None:
            parking_lot.price = float(form.price.data)
            # parking_lot.maximum_number_of_spots = int(form.maximum_number_of_spots.data)
        try:
            db.session.commit()
            flash("updated Successfully" , 'success')
            return redirect(url_for('admindashboard'))
        except Exception as e :
            db.session.rollback()
            flash(str(e), "warning")
            return redirect(url_for('admindashboard'))
        
    return render_template('edit-parking-lot.html',form = form)


@login_required
def searchParkingLot():
    form = SearchParkingLotForm()
    parking_lots = []
    available_count = 0
    count_by_lot_id = {}

    if form.validate_on_submit():
        location = form.location.data.strip()
        parking_lots = ParkingLot.query.filter_by(pincode=location, is_active = True).all()

        if parking_lots:
            lot_ids = [lot.id for lot in parking_lots]
            print(lot_ids)

            # Get count of available spots per lot
            for lot_id in lot_ids:
                count = ParkingSpot.query.filter_by(lot_id=lot_id, is_active=True).count()
                available_slots = ParkingSpot.query.filter_by(lot_id=lot_id, is_active=True,status='A').all()
                spot_ids = [spot.id for spot in available_slots]
                count_by_lot_id[lot_id] = [count,spot_ids]
            print(count_by_lot_id)
        else:
            flash("No parking lots found for this pincode.", "danger")

    return render_template(
        'search-parking-lot.html',
        form=form,
        parkingLots=parking_lots,
        available_count=available_count,
        count_by_lot_id=count_by_lot_id
    )

@login_required
def makeActive(lot_id):
    lot = ParkingLot.query.filter_by(id = lot_id ).first()
    if lot and lot.is_active  == False :
        lot.is_active = True
        db.session.commit()
        flash('Parking lot activated successfully!', 'success')
        return redirect(url_for('admindashboard'))
    else :
        flash('Parking lot is Already Active', 'warning')
        return redirect(url_for('admindashboard'))

@login_required
def lotRating(res_id, rating):
    print(res_id, rating)
    reservation = ReserveParkingSpot.query.filter_by(id=res_id).first()
    lot_id = reservation.spot.parking_lot.id
    print(lot_id)
    try:
        rating = int(rating)
        new_rating = Rating(user_id=current_user.get_id(), lot_id=lot_id, rating=rating)
        # print(new_rating)
        reservation.is_rated = True
        db.session.add(new_rating)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('userdashboard'))
    except ValueError:
        flash('Invalid rating value.', 'danger')
        return redirect(url_for('userdashboard'))
