drop database agencia_de_viajes;

create database agencia_de_viajes;

use agencia_de_viajes;

create table usuario(
    cedula varchar(20) primary key,
    nombres varchar(200),
    apellidos varchar(200)
);

create table aeropuerto(
    IATA varchar(3) primary key,
    nombre varchar(100),
    pais varchar(100),
    ciudad varchar(100)
);

create table vuelo(
    id int primary key auto_increment,
    origen varchar(3),
    destino varchar(3),
    numero_de_asientos int(3),
    fecha_de_ida date,
    fecha_de_llegada date,
    foreign key (origen) references aeropuerto(IATA),
    foreign key (destino) references aeropuerto(IATA)
);

create table reservacion(
    id int primary key auto_increment,
    usuario varchar(20),
    vuelo int,
    foreign key (usuario) references usuario(cedula),
    foreign key (vuelo) references vuelo(id)
);