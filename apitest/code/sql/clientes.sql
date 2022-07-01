DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes(id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
nombre VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL);

INSERT INTO clientes(nombre,email) VALUES("Gustavo","gustavo@email.com");
INSERT INTO clientes(nombre,email) VALUES("Maria","maria@email.com");
INSERT INTO clientes(nombre,email) VALUES("Fatima","fatima@email.com");
INSERT INTO clientes(nombre,email) VALUES("Luz","luz@email.com");
INSERT INTO clientes(nombre,email) VALUES("Fanny","fanny@email.com");
INSERT INTO clientes(nombre,email) VALUES("Rosa","rosa@email.com");
INSERT INTO clientes(nombre,email) VALUES("Ale","ale@email.com");
INSERT INTO clientes(nombre,email) VALUES("Ana","ana@email.com");
INSERT INTO clientes(nombre,email) VALUES("Lupita","lupita@email.com");
INSERT INTO clientes(nombre,email) VALUES("Carmen","carmen@email.com");
.headers ON 
SELECT * FROM clientes;

<<<<<<< HEAD
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);
CREATE UNIQUE INDEX index_usuario ON usuarios(username);
INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);
SELECT * FROM usuarios;
=======

>>>>>>> 2ac3389 (Funcionando VS)
