from flask import Flask
import secrets
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_login import login_required
from flask_migrate import Migrate

from models.models import db , Users

# config the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db.init_app(app)
migrate = Migrate(app,db)

from controllers import home_controller
from controllers import auth_controller , admin_dashboard_controller , user_dashboard_controller 
from controllers import parking_lot_controller , parking_spot_controller

# admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = generate_password_hash('admin123')
ADMIN_EMAIL = 'admin@parkingapp.com'
ADMIN_PHONE = '1234567890'
ADMIN_PINCODE = '123456'


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models.models import Users
    return Users.query.filter_by(id=int(user_id)).first()

# all Routes 

# Home Route 
@app.route('/' , methods = ['GET','POST'])
def home():
    return home_controller.home()

# Parking Spot Routes 
@app.route('/reserve-spot/<lot_id>/<spot_id>', methods=['GET', 'POST'])
def reservespot(lot_id, spot_id):
    return parking_spot_controller.reserveSpot(lot_id,spot_id)

@app.route('/release-spot/<res_id>' , methods = ['POST', 'GET'])
def releasespot(res_id):
    return parking_spot_controller.releaseSpot(res_id)


# Parking Lot Routes
@app.route('/add-parking-lot', methods = ['GET','POST'])
@login_required
def addparkinglot():
    return parking_lot_controller.addParkingLot()

@app.route('/edit-parking-lot/<lot_id>', methods = ['GET','POST'])
def editparkinglot(lot_id):
    return parking_lot_controller.editParkingLot(lot_id)

@app.route('/increase-parking-lot/<lot_id>' , methods = ['GET','POST'])
def increaselot(lot_id):
    return parking_lot_controller.increaseLot(lot_id)

@app.route('/decrease-parking-lot/<lot_id>' , methods = ['GET','POST'])
def decreaselot(lot_id):
    return parking_lot_controller.decreaseLot(lot_id)

@app.route('/delete-parking-lot/<lot_id>')
def deleteparkinglot(lot_id):
    return parking_lot_controller.deleteParkingLot(lot_id)

@app.route('/search-parking-lot' , methods=['GET','POST'])
def searchlot():
    return parking_lot_controller.searchParkingLot()

@app.route('/make-active/<lot_id>')
def makeactive(lot_id):
    return parking_lot_controller.makeActive(lot_id)

@app.route('/rating-lot/<res_id>/<rating>', methods=['GET', 'POST'])
def rating(res_id , rating):
   return parking_lot_controller.lotRating(res_id , rating)

# User Routes 
@app.route('/user-dashboard')
def userdashboard():
    return user_dashboard_controller.userDashboard()

@app.route('/user/edit-user/<user_id>', methods= ['GET', 'POST'])
def edituser(user_id):
    return user_dashboard_controller.editUser(user_id)

@app.route('/user/update-password/<user_id>', methods = ['GET','POST'])
def passwordupdate(user_id):
    return user_dashboard_controller.passwordUpdate(user_id)



# Admin Routes
@app.route('/admin-dashboard', methods=['GET','POST'])
def admindashboard():
    return admin_dashboard_controller.adminDashboard()

@app.route('/admin-search/<type>/<value>', methods=['GET','POST'])
def adminsearch(type , value):
    return admin_dashboard_controller.adminSearch(type , value)
    

# authentication routes 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return auth_controller.signup()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth_controller.login()

@app.route('/logout')
@login_required
def logout():
    return auth_controller.logout()

    
# Initialize the database
with app.app_context():
    db.create_all() 
    admin_user = Users.query.filter_by(email = ADMIN_EMAIL).first()
    if not admin_user:
        admin_user = Users(fullname = ADMIN_USERNAME, email = ADMIN_EMAIL, phone = ADMIN_PHONE, pincode = ADMIN_PINCODE , role='admin', password = ADMIN_PASSWORD)
        db.session.add(admin_user)
        db.session.commit()
    
if __name__ == '__main__':
    app.run(debug=True)