# Create products table

create table product
(
    id              char(50) not null,
    article         char(50) not null,
    name            text     not null,
    externalCode    char(50) not null,
    minimumStock    int      null,
    lastSyncDate    datetime null,
    supplyFilterUrl text     null,
    demandFilterUrl text     null,
    constraint product_pk
        unique (id),
    constraint product_pk_2
        unique (article),
    constraint product_pk_3
        unique (externalCode)
);

create table event
(
    id        char(50) null,
    eventType char(50) null,
    product   char(50) null,
    stock     int      null,
    quantity  int      null,
    moment    datetime null,
    name      char(50) null,
    constraint event_pk
        unique (id),
    constraint event_product_id_fk
        foreign key (product) references product (id)
);

create index event_eventType_index
    on event (eventType);

create index event_name_index
    on event (name);

