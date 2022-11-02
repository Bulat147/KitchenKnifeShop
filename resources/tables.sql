create table company(
    id bigserial primary key,
    name varchar(30),
    country varchar(25)
);

create table knife(
    id bigserial primary key,
    type varchar(25),
    price integer,
    company_id bigint,

    CONSTRAINT knife_company_fk FOREIGN KEY company_id REFERENCES company(id)
);

create table user(
    login varchar(20) primary key,
    type varchar(10),
    password chkpass,
    address varchar(50)
);

