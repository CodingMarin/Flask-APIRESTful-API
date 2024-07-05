from flask import request, jsonify, Response
from flask_restful import Resource
from src.config.database import config
from werkzeug.utils import secure_filename
import os

class ImagePost(Resource):
    def get(self, postid):
        db = config()
        cur = db.cursor()
        cur.execute("SELECT image FROM image_post WHERE postid = %s", (postid,))
        result = cur.fetchone()

        if result is None:
            return {'message': 'La imagen solicitada no existe.'}, 404

        image_data = result[0]
        cur.close()

        # Obtener la extensión del archivo a partir del nombre de archivo
        filename = f'image_{postid}'
        extension = os.path.splitext(filename)[-1]

        # Establecer el tipo MIME en la respuesta
        mimetype = f'image/{extension[1:]}'

        return Response(image_data, mimetype=mimetype)


    def post(self):
        data = request.form
        postid = data['postid']
        image = request.files['image']

        # Verificar que se haya enviado una imagen
        if image.filename == '':
            return jsonify({'message': 'No se ha seleccionado ninguna imagen.'}), 400

        # Verificar que la extensión de la imagen sea permitida
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not allowed_file(image.filename, allowed_extensions):
            return jsonify({'message': 'El archivo de imagen no es válido.'}), 400

        # Guardar la imagen en el servidor
        filename = secure_filename(image.filename)
        image.save(filename)

       # Leer la imagen y guardarla en la base de datos
        with open(filename, 'rb') as f:
            image_data = f.read()

        db = config()
        cur = db.cursor()
        cur.execute("INSERT INTO image_post (postid, image) VALUES (%s, %s)", (postid, image_data))
        db.commit()
        cur.close()

        return jsonify({'message': 'La imagen ha sido agregada correctamente.'})


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
