from flask import request, jsonify
from flask_restful import Resource
from src.config.database import config

class Posts(Resource):
    def get(self):
        db = config()
        cur = db.cursor()
        cur.execute("SELECT * FROM post")
        rows = cur.fetchall()
        posts = []
        for row in rows:
            post = {
                "id": row[0],
                "userid": row[1],
                "public": row[2],
                "context": row[3],
                "category": row[4],
                "reward": row[5],
                "title": row[7],
                "datepost": row[6].strftime('%Y-%m-%d %H:%M:%S'),
            }
            posts.append(post)
        cur.close()
        return jsonify(posts)

    def post(self):
        data = request.get_json()
        userid = data['userid']
        public = data['public']
        context = data['context']
        category = data['category']
        reward = data['reward']
        title = data['title']

        db = config()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO post (userid, public, context, category, reward, title, datepost) VALUES (%s, %s, %s, %s, %s, %s,now())",
            (userid, public, context, category, reward, title)
        )
        db.commit()
        cur.close()
        return jsonify({'message': 'Datos agregados satisfactoriamente'})
