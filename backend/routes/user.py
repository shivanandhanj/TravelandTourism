from flask import request, jsonify
from main import app, db, bcrypt, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.mailer import send_email

JWT_SECRET = 'SHY23FDA45G2G1K89KH5sec4H8KUTF85ret'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        username = data['username']
        password = data['password']
        phone_number = data['phoneNumber']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists, choose another'}), 400

        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, username=username, password=hash, phone_number=phone_number, admin=False)
        db.session.add(new_user)
        db.session.commit()

        send_email(
            email,
            'Welcome to Raattai',
            'Welcome to Raattai and happy purchasing. Please confirm your registration by login to http://3.6.184.48:3000/login',
            '<p>Welcome to Raattai and happy purchasing. Please confirm your registration by login to <a href="http://3.6.184.48:3000/login">http://3.6.184.48:3000/login</a></p>'
        )

        return jsonify({'success': 'You will receive an email notification.'})
    except Exception as e:
        print('Error registering user:', e)
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        token = generate_jwt_token(user.id)
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

def generate_jwt_token(user_id):
    s = Serializer(JWT_SECRET, expires_in=3600)
    return s.dumps({'user_id': user_id}).decode('utf-8')
