DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes(id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
nombre VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL);

INSERT INTO clientes(nombre,email) VALUES("Gustavo","gustavo@email.com");
INSERT INTO clientes(nombre,email) VALUES("Maria","maria@email.com");

.headers ON 
SELECT * FROM clientes;