from flask import Flask , render_template , flash
from forms import ParkingLotForm, SearchParkingLotForm
from models.models import ParkingLot , db , ParkingSpot 

# home
def home():
    '''
    home returns the index page !
    '''
    return render_template('index.html')


