drop table Stardew;
drop table Consultas;

CREATE TABLE Stardew (
    id SERIAL PRIMARY KEY,
	Nome_Fruto varchar(255),
	Inverno boolean,
	Outono boolean,
	Primavera boolean,
	Verão boolean,
	Preço_Compra integer,
	Local_Compra varchar(255),
	Preço_Venda_Comum integer,
	Preço_Venda_Incomum integer,
	Dias_Para_Amadurecer integer,
	Dias_Até_Colher_Novamente integer
);

CREATE TABLE Consultas (
    id SERIAL PRIMARY KEY,
    quantidade_dias INTEGER,
    quantidade_ouro INTEGER,
    quantidade_solo INTEGER,
    estação VARCHAR(10),
    lucro_máximo NUMERIC,
	data_hora TIMESTAMP
);

INSERT INTO Stardew (Nome_Fruto, Inverno, Outono, Primavera, Verão, Preço_Compra, Local_Compra, Preço_Venda_Comum, Preço_Venda_Incomum, Dias_Para_Amadurecer, Dias_Até_Colher_Novamente) VALUES
('Alho',FALSE,FALSE,TRUE,FALSE,40,'Armazém',60,75,4,NULL),
('Arroz não moído',FALSE,FALSE,TRUE,FALSE,40,'Armazém',30,37,8,NULL),
('Batata',FALSE,FALSE,TRUE,FALSE,50,'Armazém',80,100,6,NULL),
('Chirívia',FALSE,FALSE,TRUE,FALSE,20,'Armazém',35,43,4,NULL),
('Couve',FALSE,FALSE,TRUE,FALSE,70,'Armazém',110,137,6,NULL),
('Couve-flor',FALSE,FALSE,TRUE,FALSE,80,'Armazém',175,218,12,NULL),
('Grão de café',FALSE,FALSE,TRUE,TRUE,2500,'Carrinho',15,18,10,2),
('Jasmim-Azul',FALSE,FALSE,TRUE,FALSE,30,'Armazém',50,62,7,NULL),
('Morango',FALSE,FALSE,TRUE,FALSE,100,'Festival',120,150,8,4),
('Ruibarbo',FALSE,FALSE,TRUE,FALSE,100,'Oásis',220,275,13,NULL),
('Tulipa',FALSE,FALSE,TRUE,FALSE,20,'Armazém',30,37,6,NULL),
('Vagem',FALSE,FALSE,TRUE,FALSE,60,'Armazém',40,50,10,3),
('Carambola',FALSE,FALSE,FALSE,TRUE,400,'Oásis',750,937,13,NULL),
('Flor-Miçanga',FALSE,FALSE,FALSE,TRUE,50,'Armazém',90,112,8,NULL),
('Girassol',FALSE,TRUE,FALSE,TRUE,125,'Mercado',80,100,8,NULL),
('Lúpulo',FALSE,FALSE,FALSE,TRUE,60,'Armazém',25,31,11,1),
('Melão',FALSE,FALSE,FALSE,TRUE,80,'Armazém',250,312,12,NULL),
('Milho',FALSE,TRUE,FALSE,TRUE,150,'Armazém',50,62,14,4),
('Mirtilo',FALSE,FALSE,FALSE,TRUE,80,'Armazém',50,62,13,4),
('Papoula',FALSE,FALSE,FALSE,TRUE,100,'Armazém',140,175,7,NULL),
('Pimenta quente',FALSE,FALSE,FALSE,TRUE,40,'Armazém',40,50,5,3),
('Rabanete',FALSE,FALSE,FALSE,TRUE,40,'Armazém',90,112,6,NULL),
('Repolho roxo',FALSE,FALSE,FALSE,TRUE,100,'Armazém',260,325,9,NULL),
('Tomate',FALSE,FALSE,FALSE,TRUE,50,'Armazém',60,75,11,4),
('Trigo',FALSE,TRUE,FALSE,TRUE,10,'Armazém',25,31,4,NULL),
('Abóbora',FALSE,TRUE,FALSE,FALSE,100,'Armazém',320,400,13,NULL),
('Alcachofra',FALSE,TRUE,FALSE,FALSE,30,'Armazém',160,200,8,NULL),
('Amaranto',FALSE,TRUE,FALSE,FALSE,70,'Armazém',150,187,7,NULL),
('Berinjela',FALSE,TRUE,FALSE,FALSE,20,'Armazém',60,75,5,5),
('Beterraba',FALSE,TRUE,FALSE,FALSE,20,'Oásis',100,125,6,NULL),
('Couve chinesa',FALSE,TRUE,FALSE,FALSE,50,'Armazém',80,100,4,NULL),
('Inhame',FALSE,TRUE,FALSE,FALSE,60,'Armazém',160,200,10,NULL),
('Oxicoco',FALSE,TRUE,FALSE,FALSE,240,'Armazém',75,93,7,5),
('Rosa-de-fada',FALSE,TRUE,FALSE,FALSE,200,'Armazém',290,362,12,NULL),
('Uva',FALSE,TRUE,FALSE,TRUE,60,'Armazém',80,100,10,3);