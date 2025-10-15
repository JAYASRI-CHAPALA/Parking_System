from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, DecimalField , EmailField ,TextAreaField ,HiddenField , SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email , NumberRange ,optional 

class SigninForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=40)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=6, message='Enter a valid 6-digit pincode')])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=50)])   
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign In')

class UserEditForm(FlaskForm):
    fullname = StringField('Fullname', validators=[Length(min=4, max=20)])
    email = EmailField('Email', validators=[Email(), Length(max=40)])
    phone = StringField('Phone', validators=[Length(min=10, max=15)])
    pincode = StringField('Pincode', validators=[Length(min=6, max=6, message='Enter a valid 6-digit pincode')])
    address = StringField('Address', validators=[ Length(max=50)])
    submit = SubmitField('Update')

class PasswordUpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired(), Length(min=6, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Password')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password ', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Login to Dashboard')
    
class ParkingLotForm(FlaskForm):
    prime_location_name = StringField('Prime Location Name :', validators=[DataRequired(), Length(max=150)])
    address = StringField('Address :', validators=[DataRequired(), Length(max=50)])
    city = StringField('City :', validators=[DataRequired(), Length(max=15)])
    state = StringField('State :', validators=[DataRequired(), Length(max=15)])
    pincode = IntegerField('Pincode :', validators=[DataRequired(),NumberRange(min=100000, max=999999, message='Enter a valid 6-digit pincode')])
    price = DecimalField('Price :', validators=[DataRequired()])
    maximum_number_of_spots = IntegerField('Maximum Number of Spots :', validators=[DataRequired(), NumberRange(min=5 , message="Must be at least 1")  ])
    submit = SubmitField('Add Parking Lot')

class EditParkingLotForm(FlaskForm):
    prime_location_name = StringField('Prime Location Name :', validators=[optional(), Length(max=150)])
    address = StringField('Address :', validators=[optional(), Length(max=100)])
    city = StringField('City :', validators=[optional(), Length(max=35)])
    state = StringField('State :', validators=[optional(), Length(max=15)])
    pincode = IntegerField('Pincode :', validators=[optional(),NumberRange(min=100000, max=999999, message='Enter a valid 6-digit pincode')])
    price = DecimalField('Price :', validators=[optional()])
    maximum_number_of_spots = IntegerField('Maximum Number of Spots :', validators=[optional(), NumberRange(min=5 , message="Must be at least 1")  ])
    submit = SubmitField('Update Parking Lot')
    
class SearchParkingLotForm(FlaskForm):
    location = StringField("Search ParkingLocation :", validators=[DataRequired()])
    submit = SubmitField('Search')
    
class ReserveParkingSpotForm(FlaskForm):
    parkingcost = DecimalField('Parking Cost:', validators=[DataRequired()])
    vehicle_number = StringField('Vehicle Number:', validators=[DataRequired(), Length(max=20)])
    spot_id = StringField('Parking Spot:', validators=[DataRequired()])
    
    submit = SubmitField('Reserve Parking Spot')


class IncreaseParkingSpotsForm(FlaskForm):
    lot_id = StringField("Lot Id :")
    no_of_slots_to_increase = IntegerField('Increase Spots :' , validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Update') 

class DecreaseParkingSpotsForm(FlaskForm):
    lot_id = StringField("Lot Id :")
    no_of_spots_to_decrease = IntegerField('Decrease Spots :' , validators=[DataRequired(),NumberRange(min=1)])
    submit = SubmitField('Update') 

class ReleaseSpotForm(FlaskForm):
    spot_id = StringField('SPOT ID :')
    parking_time = StringField('Parking Time :')
    leaving_time = StringField('Leaving Time')
    total_cost = DecimalField('Total Cost :')
    submit = SubmitField('Release')
    
class AdminSearchForm(FlaskForm):
    type = SelectField('Search by',choices=[('user', 'user'), ('parkinglot', 'parkinglot'),('parkingspot','parkingspot')], validators=[DataRequired()] )
    value = StringField('Search Here....', validators=[DataRequired()])
    search = SubmitField('Search')
    
class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5):', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment:', validators=[Length(max=500)])
    submit = SubmitField('Submit Rating')