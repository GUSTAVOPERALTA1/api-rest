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


