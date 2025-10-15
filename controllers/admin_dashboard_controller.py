from datetime import datetime
from flask import render_template, redirect, url_for ,request ,flash
from models.models import db, ParkingLot, ParkingSpot, Users, ReserveParkingSpot , Rating
from flask_login import login_required
from sqlalchemy import func
from forms import IncreaseParkingSpotsForm , DecreaseParkingSpotsForm ,AdminSearchForm


@login_required
def adminDashboard():
    incform = IncreaseParkingSpotsForm()
    decform = DecreaseParkingSpotsForm()
    searchform = AdminSearchForm()

    if incform.validate_on_submit():
        increaselot(incform.lot_id.data,incform.no_of_slots_to_increase.data )

    if decform.validate_on_submit():
        decreaselot(decform.lot_id.data,decform.no_of_spots_to_decrease.data)
        
    if searchform.validate_on_submit():
        return redirect(url_for('adminsearch', type = searchform.type.data , value = searchform.value.data))
        
    # Fetching user related data
    users = Users.query.all()
    total_users = Users.query.count()

    # fetching Parking lot related data
    total_parking_lots = ParkingLot.query.filter_by().count()
    parking_lots = ParkingLot.query.filter_by(is_active=True).all()
    active_parking_lots = ParkingLot.query.filter_by(is_active=True).count()
    deleted_parking_lots = ParkingLot.query.filter_by(is_active=False).all()

    # fetching parking spot related data
    parking_spots = ParkingSpot.query.filter_by(is_active=True).all()
    available_spots = ParkingSpot.query.filter_by(is_active = True , status = 'A' ).count()
    occupied_spots = ParkingSpot.query.filter_by(is_active = True , status = 'O' ).count()

    # reservation details
    all_reservations = ReserveParkingSpot.query.all()
    reservations = ReserveParkingSpot.query.filter(ReserveParkingSpot.leaving_timestamp.isnot(None),ReserveParkingSpot.parking_timestamp.isnot(None)).all()
    total_reservations = ReserveParkingSpot.query.count()
    active_reservations = ReserveParkingSpot.query.filter_by(payment_status='Pending').count()
    completed_reservations = ReserveParkingSpot.query.filter_by(payment_status='Success').count()

    # Financial Details
    total_revenue =round(db.session.query(func.sum(ReserveParkingSpot.amount_paid)).filter_by(payment_status='Success').scalar() or 0,2)
    avg_revenue = round(db.session.query(func.avg(ReserveParkingSpot.amount_paid)).filter_by(payment_status='Success').scalar() or 0,2)
    highest_paid = round(db.session.query(func.max(ReserveParkingSpot.amount_paid)).filter_by(payment_status='Success').scalar() or 0,2)

    # Parking Details

    durations = [(r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600 for r in reservations]
    total_parking_time = round(sum(durations), 2)
    avg_parking_duration = round(sum(durations)/len(durations), 2) if durations else 0
    longest_parking_duration = round(max(durations), 2) if durations else 0

    total_ratings = Rating.query.count()
    average_rating = db.session.query(func.avg(Rating.rating)).scalar()


    today =  datetime.now().strftime('%B %d, %Y')
    
    return render_template('admin-dashboard.html',
        users=users,
        total_users = total_users,

        parkingLots=parking_lots,
        total_parking_lots = total_parking_lots,
        deleted_parking_lots=deleted_parking_lots,
        active_parking_lots = active_parking_lots,

        parkingSpots=parking_spots,
        available_spots = available_spots,
        occupied_spots = occupied_spots,
        
        all_reservations = all_reservations,
        reservations=reservations,
        total_reservations = total_reservations,
        active_reservations = active_reservations,
        completed_reservations = completed_reservations,

        total_revenue = total_revenue,
        avg_revenue = avg_revenue,
        highest_paid = highest_paid,

        total_parking_time = total_parking_time,
        avg_parking_duration = avg_parking_duration,
        longest_parking_duration = longest_parking_duration,

        today = today,
        incform = incform,
        decform = decform,
        searchform = searchform,
        total_ratings = total_ratings,
        average_rating = average_rating
    )


@login_required
def decreaselot(lot_id , spots):
        delete_spots_count = spots
        lot = ParkingLot.query.filter_by(id=lot_id).first()

        if not lot:
            flash("Parking lot not found.", "error")
            return redirect(url_for('dashboard'))

        # Find available spots that can be removed
        available_spots = ParkingSpot.query.filter_by(
            lot_id=lot.id, status='A', is_active=True
        ).order_by(ParkingSpot.id.desc()).limit(delete_spots_count).all()

        if len(available_spots) < delete_spots_count:
            flash("Not enough available spots to remove.", "warning")
            return redirect(url_for('admindashboard'))

        # Soft-delete those spots
        for spot in available_spots:
            spot.is_active = False

        lot.maximum_number_of_spots -= spots
        db.session.commit()

        flash(f"{delete_spots_count} spot(s) removed successfully.", "success")
        return redirect(url_for('admindashboard'))



def increaselot(lot_id , spots):
        increase_spots_count = spots

        lot = ParkingLot.query.filter_by(id=lot_id).first()
        print(lot)

        if not lot:
            return redirect(url_for('admindashboard'))

        # Reactivate old inactive spots first
        inactive_spots = ParkingSpot.query.filter_by(
            lot_id=lot.id, is_active=False
        ).order_by(ParkingSpot.id).limit(increase_spots_count).all()
        print('inactive spots',inactive_spots)
        for spot in inactive_spots:
            spot.is_active = True
            increase_spots_count -= 1

        # Only create new spots if more are needed
        if increase_spots_count > 0:
            existing_count = ParkingSpot.query.filter_by(lot_id=lot.id).count()
            for i in range(existing_count + 1, existing_count + increase_spots_count + 1):
                spot_id = f"{lot.id}-SPOT-{str(i).zfill(2)}"
                new_spot = ParkingSpot(id=spot_id, lot_id=lot.id, status='A')
                db.session.add(new_spot)

        lot.maximum_number_of_spots += spots
        db.session.commit()
        flash('successfully added','success')
        return redirect(url_for('admindashboard'))
    
@login_required
def adminSearch(type, value):
    # print(type , value )

    if type == 'user':
            user = Users.query.filter_by(id = value).first()
            if user:
                return render_template('admin-search.html', user = user)   
            else :
                flash('User Not Found','danger')
                # return redirect(url_for('admindashboard'))
    if type == 'parkinglot':
            parkinglot = ParkingLot.query.filter_by(id = value).first()
            if parkinglot:
                return render_template('admin-search.html',  parkinglot = parkinglot)   
            else :
                flash('Parking Lot Not Found','danger')
                # return redirect(url_for('admindashboard'))
    if type == 'parkingspot':
            parkingspot = ParkingSpot.query.filter_by(id = value).first()
            if parkingspot:
                return render_template('admin-search.html',  parkingspot = parkingspot)   
            else :
                flash('Parking Spot Not Found','danger')
    return redirect(url_for('admindashboard'))
