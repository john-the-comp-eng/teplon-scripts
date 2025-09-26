# Create products table

create table product
(
    id           char(50) not null,
    article      char(50) not null,
    name         text     not null,
    externalCode char(50) not null,
    minimumStock int      null,
    lastSyncDate datetime null,
    filterUrl    text     null,
    constraint product_pk
        unique (id),
    constraint product_pk_2
        unique (article),
    constraint product_pk_3
        unique (externalCode)
);



