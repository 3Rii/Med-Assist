use projekt;

create table accounts
(
    id       int auto_increment
        primary key,
    fullname char(50) not null,
    username char(20) not null,
    password char(20) not null,
    email    char(40) not null
)
    auto_increment = 8;

create table check_ups
(
    id             int auto_increment
        primary key,
    id_user        int                    null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    nazwa          char(20)   default '0' null,
    constraint check_ups_accounts_id_fk
        foreign key (id_user) references accounts (id)
);

create table prevention
(
    id             int auto_increment
        primary key,
    id_user        int                    null,
    link_gov       char(20)   default '0' not null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    nazwa          char(20)   default '0' not null,
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
)
    auto_increment = 10;

create table vacc
(
    id             int auto_increment
        primary key,
    id_user        int                    null,
    typ            char(20)   default '0' not null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    nazwa          char(20)   default '0' not null,
    constraint vacc_accounts_id_fk
        foreign key (id_user) references accounts (id)
);
