import pymysql

def conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='ventas')
