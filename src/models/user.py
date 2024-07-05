from flask import request, jsonify
from flask_restful import Resource
from src.config.database import config

class Users(Resource):
    def get(self):
        db = config()
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        columnas = [desc[0] for desc in cur.description]
        resultado = [dict(zip(columnas, row)) for row in rows]
        cur.close()
        return jsonify(resultado)

    def post(self):
        data = request.get_json()
        connected = config()
        cursor = connected.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = %s OR email = %s",
            (data['id'], data['email'])
        )
        user = cursor.fetchone()
        if user:
            cursor.close()
            return jsonify({'message': 'El usuario ya existe'})
        else:
            cursor.execute(
                "INSERT INTO users (id, name, email, gcoins, aboutme, regdate, country, photourl) VALUES (%s, %s, %s, %s, %s, now(), %s, %s)",
                tuple(data.values())
            )
        connected.commit()
        cursor.close()
        return jsonify({'message': 'Datos agregados satisfactoriamente'})

class User(Resource):
    def get(self, id=None):
        id = str(id)
        db = config()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        row = cur.fetchone()
        if not row:
            return {'message': 'User not found'}, 404
        columnas = [desc[0] for desc in cur.description]
        resultado = dict(zip(columnas, row))
        cur.close()
        return resultado