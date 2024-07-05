import mysql.connector

def config():
    dsource = mysql.connector.connect(
        user='gruwin',
        password='marinmarin123',
        host='gruwin.mysql.pythonanywhere-services.com',
        database='gruwin$default'
    )
    return dsource

