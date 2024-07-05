from flask import request, jsonify
from flask_jwt_extended import create_access_token
from src.config.database import config


class UserService:


    def signup(self):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')


        if not username or not password:
            return jsonify({'message': 'Datos incompletos.'}), 400

        db = config()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO account (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password))
        db.commit()
        cur.close()

        return jsonify({'message': 'User logged successful'}), 201

    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({'message': 'Please complete all the camps'}), 400

        db = config()
        cur = db.cursor()
        cur.execute('SELECT * FROM account WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({'message': 'User not found.'}), 401

        if user[1] == password:
            return jsonify({'message': 'Credentials error.'}), 401

        access_token = create_access_token(identity=user[0],expires_delta=False)

        return jsonify({'access_token': access_token}), 200