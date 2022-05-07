use projekt;

create table accounts
(
    id       int auto_increment,
    fullname char(50) not null,
    username char(20) not null,
    password char(20) not null,
    email    char(20) not null,
    constraint accounts_pk
        primary key (id)
);

create table user
(
    id int auto_increment,
    wiek float null,
    waga float null,
    wzrost float null,
    plec bool null,
    papierosy bool null,
    alkohol bool null,
    aktywnosc bool null,
    constraint vaccines_pk
      primary key(id),
    constraint vaccines_accounts_id_fk
      foreign key (id) references accounts (id)
);

create table check_ups
(
    id    int auto_increment,
    nazwa char(20) not null,
    constraint check_ups_pk
        primary key (id),
    constraint check_ups_accounts_id_fk
        foreign key (id) references accounts (id)
);

create table prevention
(
    id       int auto_increment,
    nazwa    char(20) not null,
    link_gov char(20) not null,
    constraint prevention_pk
        primary key (id),
    constraint prevention_accounts_id_fk
        foreign key (id) references accounts (id)
);

create table vacc
(
    id       int auto_increment,
    nazwa    char(20) not null,
    typ char(20) not null,
    constraint vacc_pk
        primary key (id),
    constraint vacc_accounts_id_fk
        foreign key (id) references accounts (id)
);