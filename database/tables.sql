create table company(
    name varchar(30) primary key,
    country varchar(25)
);

create table type(
    name varchar(30) primary key,
    description varchar(100) unique
);

create table knife(
    id bigserial primary key,
    name varchar(30) unique,
    type_name varchar(30) REFERENCES type(name),
    price integer,
    company_name varchar(30),
    photo_path varchar(50),

    CONSTRAINT knife_company_fk FOREIGN KEY (company_name) REFERENCES company(name)
);

create table person(
    login varchar(20) primary key,
    type varchar(10),
    password varchar(25),
    address varchar(50)
);

-- Корзина в cookie

create table purchase(
    id bigserial primary key,
    person_login varchar(20),
    purchase_date date,


    CONSTRAINT purchase_person_fk FOREIGN KEY (person_login) REFERENCES person(login)
);

create table favorites(
    person_login varchar(20) primary key,

    constraint favorites_person_fk foreign key (person_login) references person(login)
);

create table favorites_knifes(
    favorites_key varchar(20) references favorites(person_login),
    knife_id bigint references knife(id),

    constraint fav_knf_pk primary key (favorites_key, knife_id)
);

create table purchase_knifes(
    purchase_id bigint references purchase(id),
    knife_id bigint references knife(id),

    constraint prc_knf_pk primary key (purchase_id, knife_id)
);

create table basket(
    basket_id bigserial primary key,
    person_login varchar(20) references person(login)
)

create table basket_knifes(
    knife_id bigint references knife(id),
    basket_id bigint references basket(basket_id),

    constraint bsk_knf_pk primary key (knife_id, basket_id)
)

ALTER TABLE purchase ALTER COLUMN purchase_date set DEFAULT CURRENT_DATE;

ALTER TABLE person ALTER COLUMN address set NOT NULL;
ALTER TABLE person ALTER COLUMN type set NOT NULL;
ALTER TABLE person ALTER COLUMN password set NOT NULL;