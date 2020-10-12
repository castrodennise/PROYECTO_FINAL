# imports
import pymysql
import random
import datetime

# lista de paises
aeropuertos = [["GYE", "Ecuador", "Guayaquil", "LAN Ecuador", "Aeropuerto Internacional Jose Joaquin de Olmedo"],
               ["UIO", "Ecuador", "Quito", "Avianca Ecuador",
                   "Aeropuerto Internacional Mariscal Sucre"],
               ["ICN", 'Corea del Sur', "Ciudad Metropolitana de Incheon",
                   "Korean Air", "Aeropuerto Internacional de Incheon"],
               ["ABC", 'España', "Castilla-La Mancha",
                   "Air Europa Lineas Aereas", "Aeropuerto de Albacete"],
               ["AGP", 'España', "Andalucía", "Vueling Airlines",
                   "Aeropuerto de Málaga-Costa del Sol"],
               ["HMO", 'Mexico', "Sonora", "Aeroméxico",
                   "Aeropuerto Internacional General Ignacio Pesqueira García"],
               ["GDL", 'Mexico', "Jalisco", "Calafia Airlines",
                   "Aeropuerto Internacional de Guadalajara"],
               ["ARI", "Chile", "Arica y Parinacota", "LATAM Chile",
                   "Aeropuerto Internacional Chacalluta"],
               ["CCP", "Chile", "Biobío", "Sky Airline", "Aeropuerto Carriel Sur"],
               ["BOG", "Colombia", "Bogotá", "Avianca Aerotaxi",
                   "Aeropuerto Internacional El Dorado"],
               ["MDE", "Colombia", "Antioquia-Medellin", "Cosmos S.A",
                   "Aeropuerto Internacional José María Cordova"],
               ["CCC", "Cuba", "Ciego de Ávila", "Cubana",
                   "Aeropuerto Internacional de Jardines del Rey"],
               ["HAV", "Cuba", "La Habana", "Cubana",
                   "	Aeropuerto Internacional José Martí"],
               ["DAY", "Estados Unidos", "Ohio", "Southwest Airlines",
                   "Aeropuerto Internacional James M. Cox-Dayton"],
               ["EGE", "Estados Unidos", "Colorado", "Delta Airlines",
                   "	Aeropuerto Regional del Condado de Eagle"],
               ["CCS", "Venezuela", "Dependencias Federales-Caracas", "AeroAndinas",
                   "Aeropuerto Internacional de Maiquetía Simón Bolívar"],
               ["VCP", "Brasil", "São Paulo", "Azul Brazilian Airlines",
                   "Aeropuerto de Viracopos"],
               ["VDC", "Brasil", "Bahía", "Passaredo Transportes Aéreos",
                   "Aeropuerto de Vitoria da Conquista"],
               ["TRS", "Italia", "Friuli-Venecia Julia - Trieste",
                   "Air Italy", "Aeropuerto de Trieste - Friuli Venezia Giulia"],
               ["NAP", "Italia", "Campania - Napoles", "Ernest Airlines",
                   "Aeropuerto de Nápoles-Capodichino"],
               ["MPN", "Reino Unido", "Islas Malvinas",
                   "British Airways", "Base Aérea de Monte Agradable"]
               ]

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='agencia_de_viajes'
)

cursor = connection.cursor()


def upload_airports():
    for value in aeropuertos:
        sql = "INSERT INTO aeropuerto (IATA, nombre, pais, ciudad) VALUES (%s, %s, %s, %s)"
        cursor.execute(
            sql, (value[0].strip(), value[4].strip(), value[1].strip(), value[2].strip()))
    connection.commit()


def upload_vuelos():
    inicio = datetime.date(2020, 10, 10)
    final = datetime.date(2020, 12, 31)
    for value in range(random.randint(25, 30)):
        random_date_ida = inicio + (final - inicio) * random.random()
        random_date_llegada = inicio + (final - inicio) * random.random()
        sql = """INSERT INTO vuelo (origen, destino, numero_de_asientos, fecha_de_ida, fecha_de_llegada) 
                        VALUES (%s, %s, %s, %s, %s)"""
        if random_date_llegada > random_date_ida:
            cursor.execute(sql, (aeropuertos[random.randint(0, len(aeropuertos)-1)][0],
                             aeropuertos[random.randint(0, len(aeropuertos)-1)][0], 
                             random.randint(1, 5), random_date_ida, random_date_llegada))
        elif random.randint(0,10) % 2 == 0:
            sql = """INSERT INTO vuelo (origen, destino, numero_de_asientos, fecha_de_ida) 
                        VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (aeropuertos[random.randint(0, len(aeropuertos)-1)][0],
                             aeropuertos[random.randint(0, len(aeropuertos)-1)][0], 
                             random.randint(1, 5), random_date_ida))
        else:
            cursor.execute(sql, (aeropuertos[random.randint(0, len(aeropuertos)-1)][0],
                             aeropuertos[random.randint(0, len(aeropuertos)-1)][0], 
                             random.randint(1, 5), random_date_llegada, random_date_ida))
    connection.commit()


upload_airports()
upload_vuelos()
