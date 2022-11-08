create table company(
    id bigserial primary key,
    name varchar(30) unique,
    country varchar(25)
);

create table knife(
    id bigserial primary key,
    name varchar(30) unique,
    type varchar(25),
    price integer,
    company_id bigint,
    photo_path varchar(50),

    CONSTRAINT knife_company_fk FOREIGN KEY (company_id) REFERENCES company(id)
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