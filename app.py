from src.services.userservice import UserService
from flask import Flask, jsonify, request
from flask_restful import Api
from src.models.user import Users, User
from src.models.post import Posts
from src.models.message import MessageService
from src.models.image_post import ImagePost
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'GRUWIN-ADMIN-ACCOUNT'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

api = Api(app)

uservice = UserService()

msg_service = MessageService()

@app.route('/')
def welcome():
    return jsonify({'Flask restful': 'conected'})


@app.route('/signup', methods=['POST'])
def signup():
    return uservice.signup()


@app.route('/login', methods=['POST'])
def login():
    return uservice.login()


@app.route('/users', methods=['GET'])
@jwt_required()
def getUsers():
    users = Users().get()
    return users


@app.route('/users', methods=['POST'])
def addUsers():
    users = Users()
    return users.post()


@app.route('/user/<string:id>')
@jwt_required()
def getUserById(id):
    user = User().get(id)
    return jsonify(user)


@app.route('/post', methods=['GET'])
@jwt_required()
def getPost():
    posts = Posts().get()
    return posts


@app.route('/post', methods=['POST'])
def createPost():
    post = Posts()
    return post.post()


@app.route('/imagepost/<int:postid>', methods=['GET'])
@jwt_required()
def getImagePost(postid):
    Image = ImagePost()
    return Image.get(postid)


@app.route('/imagepost', methods=['POST'])
def createImagePost():
    image_post = ImagePost()
    return image_post.post()


@app.route('/messages/<string:sender_id>/<string:recipient_id>', methods=['GET'])
@jwt_required()
def getMessages(sender_id, recipient_id):
    messages = msg_service.get_messages(sender_id, recipient_id)
    return jsonify(messages)


@app.route('/messages', methods=['POST'])
@jwt_required()
def createMessage():
    data = request.get_json()
    message = msg_service.create_message(data['sender_id'], data['recipient_id'], data['content'])
    return jsonify(message)


@app.route('/messages/<string:id>', methods=['PUT'])
@jwt_required()
def updateMessage(id):
    data = request.get_json()
    message = msg_service.update_message(id, data)
    return jsonify(message)


@app.route('/messages/<string:id>', methods=['DELETE'])
@jwt_required()
def deleteMessage(id):
    msg_service.delete_message(id)
    return '', 204


@app.route('/protected')
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'message': f'¡Bienvenido, usuario con id {current_user_id}!'}), 200

@app.route('/email', methods=['POST'])
@jwt_required()
def sendEmail():
    try:
        # Obtener los datos del cuerpo del mensaje
        data = request.get_json()

        if data:
            name_client = data.get('name_client')
            email_client = data.get('email_client')
            phone_client = data.get('phone_client')
            email_address = data.get('email_address')
            message_subject = data.get('message_subject')
            message_send = data.get('message_send')

            sender_email = "marinalexander691@gmail.com"
            password = "ibdzsrjmsfkjhdbj"
            receiver_email = email_client

            message = MIMEMultipart("alternative")
            message["Subject"] = message_subject
            message["From"] = "Intermediario <{}>".format(sender_email)
            message["To"] = receiver_email

            # Crear el cuerpo del correo electrónico con los datos
            text = """<html>
                        <body>
                        <span style="font-size:15px;">Ey! Te estamos enviando este correo para informarte que tienes un nuevo mensaje:</span>
                        <br>
                        <br>
                        <b style="font-size:15px;">Cliente:</b><br><span style="font-size:15px;">{}</span><br><br>
                        <b style="font-size:15px;">Telefono:</b><br><span style="font-size:15px;">{}</span><br><br>
                        <b style="font-size:15px;">Correo del cliente:</b><br><span style="font-size:15px;">{}</span><br><br>
                        <b style="font-size:15px;">Mensaje del cliente:</b><br><span style="font-size:15px;">{}</span><br><br>
                        </body>
                        </html>""".format(name_client, phone_client, email_address, message_send)

            message.attach(MIMEText(text, "html"))

            # Iniciar sesión en el servidor SMTP y enviar el correo electrónico
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            return jsonify({"message": "Email sent successfully"})
        else:
            return jsonify({"message": "No data received"}), 400

    except Exception as e:
        return jsonify({"message": "An error occurred: {}".format(str(e))}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'La URL solicitada no se encontró en el servidor.'}), 404


if __name__ == '__main__':
    app.run()
