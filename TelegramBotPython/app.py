import pymysql
from telegram.ext import Updater, CommandHandler
from credentials import credentials

connection = pymysql.connect(
    host='localhost',
    user=credentials['user_database'],
    password=credentials['password_database'],
    db='agencia_de_viajes'
)

cursor = connection.cursor()


def start(update, context):
    first_name = update.message['chat']['first_name']
    update.message.reply_text('''Hola, {}. Los comandos disponibles son:

    /list -> Lista todos los vuelos disponibles.
    /searchd <destino> -> Lista todos los vuelos disponibles al destino especificado.
    /searcho <origen> -> Lista todos los vuelos disponibles desde el origen especificado.
    /buyticket <id de vuelo> <cédula> <nombre> <apellido>-> Reserva vuelos solo de ida.
    /buyrtticket <id de vuelo> <cédula> <nombre> <apellido> -> Reserva vuelos de ida y vuelta.
    
    Si te olvidas de los comandos, usa /help para consultarlos.'''.format(first_name))
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /start")


def list(update, context):
    sql = 'SELECT * FROM vuelo'
    all = ''
    cursor.execute(sql)
    vuelos = cursor.fetchall()
    for vuelo in vuelos:
        all += f'ID: {vuelo[0]}, \nOrigen: {vuelo[1]},\nDestino: {vuelo[2]},\nNúmero de asientos: {vuelo[3]},\nFecha de ida: {vuelo[4]},\nFecha de llegada: {vuelo[5]}\n\n'
    update.message.reply_text(all)
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /list")


def searchd(update, context):
    arguments = update.message['text'].split(" ")
    if len(arguments) == 1:
        update.message.reply_text(
            f'El comando no puede ir solo! tiene que tener un argumento.')
    else:
        str = " ".join(arguments[1:])
        sql = f'select * from vuelo join aeropuerto on vuelo.destino = aeropuerto.IATA where destino = %s or pais = %s or ciudad = %s or nombre = %s'
        all = ''
        cursor.execute(sql, (str, str, str, str))
        vuelos_disponibles = cursor.fetchall()
        for vuelo in vuelos_disponibles:
            all += f'ID: {vuelo[0]}, \nOrigen: {vuelo[1]},\nDestino: {vuelo[2]},\nNúmero de asientos: {vuelo[3]},\nFecha de ida: {vuelo[4]},\nFecha de llegada: {vuelo[5]}\n\n'
        if vuelos_disponibles != None:
            update.message.reply_text(
                f"Los vuelos disponibles al destino {str} son:\n\n"+all)
        else:
            update.message.reply_text(
                f'No hay vuelos disponibles desde el origen indicado.')
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /searchd")


def searcho(update, context):
    arguments = update.message['text'].split(" ")
    if len(arguments) == 1:
        update.message.reply_text(
            f'El comando no puede ir solo! tiene que tener un argumento.')
    else:
        str = " ".join(arguments[1:])
        sql = f'select * from vuelo join aeropuerto on vuelo.origen = aeropuerto.IATA where origen = %s or pais = %s or ciudad = %s or nombre = %s'
        all = ''
        cursor.execute(sql, (str, str, str, str))
        vuelos_disponibles = cursor.fetchall()
        for vuelo in vuelos_disponibles:
            all += f'ID: {vuelo[0]}, \nOrigen: {vuelo[1]},\nDestino: {vuelo[2]},\nNúmero de asientos: {vuelo[3]},\nFecha de ida: {vuelo[4]},\nFecha de llegada: {vuelo[5]}\n\n'
        if vuelos_disponibles != None:
            update.message.reply_text(
                f"Los vuelos disponibles desde {str} son:\n\n"+all)
        else:
            update.message.reply_text(
                f'No hay vuelos disponibles desde el origen indicado.')
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /searcho")


def buyticket(update, context):
    arguments = update.message['text'].split(" ")
    if len(arguments) < 5 or len(arguments) > 5:
        update.message.reply_text(
            f'El comando debe tener 4 argumentos.')
    else:
        sql = f'select * from usuario where cedula = {arguments[2]}'
        cursor.execute(sql)
        usuario = cursor.fetchone()
        if usuario == None:
            sql = f'insert into usuario (cedula, nombres, apellidos) values (%s, %s, %s)'
            cursor.execute(sql, (arguments[2], arguments[3], arguments[4]))
            connection.commit()
        sql = f'select * from vuelo where id = %s'
        cursor.execute(sql, arguments[1])
        vuelo = cursor.fetchone()
        if vuelo[5] == None:
            sql = f'insert into reservacion (usuario, vuelo) values (%s, %s)'
            cursor.execute(sql, (arguments[2], arguments[1]))
            connection.commit()
            update.message.reply_text(
                f"El vuelo {arguments[1]} para el usuario {arguments[4]} ha sido reservado.")
        else:
            update.message.reply_text(
                f'Solo puede reservar vuelos que solo tenga fecha de ida.')
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /buyticket")


def buyrtticket(update, context):
    arguments = update.message['text'].split(" ")
    if len(arguments) < 5 or len(arguments) > 5:
        update.message.reply_text(
            f'El comando debe tener 4 argumentos.')
    else:
        sql = f'select * from usuario where cedula = {arguments[2]}'
        cursor.execute(sql)
        usuario = cursor.fetchone()
        if usuario == None:
            sql = f'insert into usuario (cedula, nombres, apellidos) values (%s, %s, %s)'
            cursor.execute(sql, (arguments[2], arguments[3], arguments[4]))
            connection.commit()
        sql = f'select * from vuelo where id = %s'
        cursor.execute(sql, arguments[1])
        vuelo = cursor.fetchone()
        if vuelo[5] != None:
            sql = f'insert into reservacion (usuario, vuelo) values (%s, %s)'
            cursor.execute(sql, (arguments[2], arguments[1]))
            connection.commit()
            update.message.reply_text(
                f"El vuelo {arguments[1]} para el usuario {arguments[4]} ha sido reservado.")
        else:
            update.message.reply_text(
                f'Solo puede reservar vuelos que tengan fecha de ida y de retorno.')
    print(update.message['chat']['first_name']+" " +
          update.message['chat']['last_name']+" ha ejecutado /buyrtticket")


# Método de prueba
def listvuelos(update, context):
    sql = 'SELECT * FROM vuelo'
    cursor.execute(sql)
    vuelos = cursor.fetchall()
    for vuelo in vuelos:
        string_vuelo = [str(int) for int in vuelo]
        update.message.reply_text(str(" | ".join(string_vuelo)))

# Método de prueba
def register(update, context):
    arguments = update.message['text'].split(" ")
    if len(arguments) != 1:
        try:
            sql = 'INSERT INTO usuario VALUES (%s, %s, %s)'
            cursor.execute(sql, (arguments[1], arguments[2], arguments[3]))
            connection.commit()
        except Exception as e:
            update.message.reply_text(e)
    else:
        update.message.reply_text(
            "El comando no puede ir solo! tiene que tener un argumento.")


def main():
    updater = Updater(credentials['token'], use_context=True)
    # Comandos
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", start))
    updater.dispatcher.add_handler(CommandHandler("list", list))
    updater.dispatcher.add_handler(CommandHandler("searchd", searchd))
    updater.dispatcher.add_handler(CommandHandler("searcho", searcho))
    updater.dispatcher.add_handler(CommandHandler("buyticket", buyticket))
    updater.dispatcher.add_handler(CommandHandler("buyrtticket", buyrtticket))
    updater.dispatcher.add_handler(
        CommandHandler("listvuelos", listvuelos))  # Comando de prueba
    updater.dispatcher.add_handler(
        CommandHandler("register", register))  # Prueba
    # Start
    updater.start_polling()
    print('Funcionando...')
    # Esperando
    updater.idle()


# Otros métodos
if __name__ == '__main__':
    main()
