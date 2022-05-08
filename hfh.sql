use projekt;

create table projekt.accounts
(
    id       int auto_increment
        primary key,
    fullname char(50) not null,
    username char(20) not null,
    password char(20) not null,
    email    char(40) not null
)
    auto_increment = 6;

create table projekt.check_ups
(
    id             int                    not null,
    nazwa          char(20)   default '0' null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    primary key (id),
    constraint check_ups_id_uindex
        unique (id)
);
create table projekt.Date
(
    id    int          not null,
    name  varchar(100) null,
    email varchar(100) null,
    phone varchar(100) null,
    primary key (id)
);

create table projekt.prevention
(
    id             int                    not null,
    nazwa          char(20)   default '0' not null,
    link_gov       char(20)   default '0' not null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    primary key (id),
    constraint prevention_id_uindex
        unique (id)
);

create table projekt.user
(
    id        int        default 2 not null,
    wiek      float      default 0 null,
    waga      float      default 0 null,
    wzrost    float      default 0 null,
    plec      tinyint(1) default 0 null,
    papierosy tinyint(1) default 0 null,
    alkohol   tinyint(1) default 0 null,
    aktywnosc tinyint(1) default 0 null,
    primary key (id),
    constraint user_u_id_uindex
        unique (id)
);

create table projekt.vacc
(
    id             int                    not null,
    nazwa          char(20)   default '0' not null,
    typ            char(20)   default '0' not null,
    current_status tinyint(1) default 0   null,
    todo_status    tinyint(1) default 0   null,
    primary key (id),
    constraint vacc_id_uindex
        unique (id)
);

