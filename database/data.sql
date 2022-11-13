INSERT INTO knife(name, type_name, company_name, price)
VALUES  ('JOJO', 'chief', 'FoxKnife', 3000);

INSERT INTO type
VALUES ('chief', 'Шеф-нож');

INSERT INTO company
VALUES ('FoxKnife', 'Россия');

INSERT INTO company
VALUES ('Jashoui', 'Франция');

INSERT INTO type
VALUES ('bread', 'Нож для хлеба');

INSERT INTO basket(person_login)
values ('bulatHulk');

INSERT INTO basket_knifes
VALUES (1, 1);

INSERT INTO purchase(person_login, purchase_date)
VALUES ('bulatHulk', 2022-11-12);

INSERT INTO purchase_knifes
VALUES (1, 2);

INSERT INTO purchase_knifes
VALUES (1, 1);
