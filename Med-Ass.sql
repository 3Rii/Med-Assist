create database projekt;
use projekt;

create table accounts
(
    id       int auto_increment
        primary key,
    fullname varchar(100) not null,
    username char(100)    not null,
    password char(100)    not null,
    email    char(100)    not null
);

create table check_ups
(
    id             int auto_increment
        primary key,
    id_user        int                      null,
    current_status tinyint(1)   default 0   null,
    todo_status    tinyint(1)   default 0   null,
    nazwa          varchar(100) default '0' null,
    constraint check_ups_accounts_id_fk
        foreign key (id_user) references accounts (id)
);

create table prevention
(
    id             int auto_increment
        primary key,
    id_user        int                      null,
    link_gov       varchar(100) default '0' not null,
    current_status tinyint(1)   default 0   null,
    todo_status    tinyint(1)   default 0   null,
    nazwa          varchar(100) default '0' not null,
    constraint prevention_accounts_id_fk
        foreign key (id_user) references accounts (id)
);

create table user
(
    id         int auto_increment
        primary key,
    account_id int                  not null,
    wiek       float      default 0 null,
    waga       float      default 0 null,
    wzrost     float      default 0 null,
    plec       tinyint(1) default 0 null,
    papierosy  tinyint(1) default 0 null,
    alkohol    tinyint(1) default 0 null,
    aktywnosc  tinyint(1) default 0 null,
    constraint user_u_id_uindex
        unique (id),
    constraint user_ibfk_1
        foreign key (account_id) references accounts (id),
    constraint user_accounts_id_fk
        foreign key (account_id) references accounts (id)
);

create table vacc
(
    id             int auto_increment
        primary key,
    id_user        int                      null,
    typ            varchar(100) default '0' not null,
    current_status tinyint(1)   default 0   null,
    todo_status    tinyint(1)   default 0   null,
    nazwa          char(100)    default '0' not null,
    constraint vacc_accounts_id_fk
        foreign key (id_user) references accounts (id)
);
