from src.config.database import config
from datetime import datetime

class MessageService:

    def get_messages(self, sender_id, recipient_id):
        db = config()
        cur = db.cursor()
        cur.execute("SELECT * FROM messages WHERE (sender_id=%s AND recipient_id=%s) OR (sender_id=%s AND recipient_id=%s) ORDER BY created_at ASC", (sender_id, recipient_id, recipient_id, sender_id))
        rows = cur.fetchall()
        messages = []
        for row in rows:
            message_date = row[4].strftime('%Y-%m-%d %H:%M:%S')
            message = {
                "id": row[0],
                "sender_id": row[1],
                "recipient_id": row[2],
                "content": row[3],
                "created_at": message_date
            }
            messages.append(message)
        cur.close()
        return messages

    def create_message(self, sender_id, recipient_id, content):
        date_sent = datetime.now()

        db = config()
        cur = db.cursor()
        cur.execute("INSERT INTO messages (sender_id, recipient_id, content, created_at) VALUES (%s, %s, %s, %s)", (sender_id, recipient_id, content, date_sent))
        db.commit()

        message_id = cur.lastrowid

        cur.execute("SELECT * FROM messages WHERE id=%s", (message_id,))
        row = cur.fetchone()
        message_date = row[4].strftime('%Y-%m-%d %H:%M:%S')
        message = {
            "id": row[0],
            "sender_id": row[1],
            "recipient_id": row[2],
            "content": row[3],
            "created_at": message_date
        }
        cur.close()
        return message

    def update_message(self, id, data):
        text = data['text']

        db = config()
        cur = db.cursor()
        cur.execute("UPDATE messages SET text=%s WHERE id=%s", (text, id))
        db.commit()

        cur.execute("SELECT * FROM messages WHERE id=%s", (id,))
        row = cur.fetchone()
        message_date = row[2].strftime('%Y-%m-%d %H:%M:%S')
        message = {
            "id": row[0],
            "user_id": row[1],
            "text": row[3],
            "date_sent": message_date
        }
        cur.close()
        return message

    def delete_message(self, id):
        db = config()
        cur = db.cursor()
        cur.execute("DELETE FROM messages WHERE id=%s", (id,))
        db.commit()
        cur.close()
