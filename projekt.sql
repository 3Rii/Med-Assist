CREATE TABLE accounts (
    id       NUMBER NOT NULL,
    fullname VARCHAR2(25) NOT NULL,
    username VARCHAR2(25) NOT NULL,
    password VARCHAR2(25) NOT NULL,
    email    VARCHAR2(25)
);

ALTER TABLE accounts ADD CONSTRAINT accounts_pk PRIMARY KEY ( id );

ALTER TABLE accounts ADD CONSTRAINT accounts_username_un UNIQUE ( username );

CREATE TABLE basics (
    id          NUMBER NOT NULL,
    wiek        NUMBER(2) NOT NULL,
    waga        NUMBER(3) NOT NULL,
    wzrost      NUMBER(3) NOT NULL,
    plec        CHAR(1) NOT NULL,
    papierosy   CHAR(1) NOT NULL,
    alkohol     CHAR(1) NOT NULL,
    aktywnosc   VARCHAR2(25) NOT NULL,
    accounts_id NUMBER NOT NULL
);

CREATE UNIQUE INDEX basics__idx ON
    basics (
        accounts_id
    ASC );

ALTER TABLE basics ADD CONSTRAINT basics_pk PRIMARY KEY ( id );

CREATE TABLE checkups (
    id        NUMBER NOT NULL,
    nazwa     VARCHAR2(25) NOT NULL,
    status    VARCHAR2(25) NOT NULL,
    basics_id NUMBER NOT NULL
);

ALTER TABLE checkups ADD CONSTRAINT checkups_pk PRIMARY KEY ( id );

CREATE TABLE entity_6 
    
    -- No Columns 
;

CREATE TABLE prevention (
    id        NUMBER NOT NULL,
    nazwa     VARCHAR2(25) NOT NULL,
    link      VARCHAR2(25) NOT NULL,
    status    VARCHAR2(25) NOT NULL,
    basics_id NUMBER NOT NULL
);

ALTER TABLE prevention ADD CONSTRAINT prevention_pk PRIMARY KEY ( id );

CREATE TABLE vaccines (
    id        NUMBER NOT NULL,
    nazwa     VARCHAR2(25) NOT NULL,
    typ       VARCHAR2(25) NOT NULL,
    status    VARCHAR2(25) NOT NULL,
    basics_id NUMBER NOT NULL
);

ALTER TABLE vaccines ADD CONSTRAINT vaccines_pk PRIMARY KEY ( id );

ALTER TABLE basics
    ADD CONSTRAINT basics_accounts_fk FOREIGN KEY ( accounts_id )
        REFERENCES accounts ( id );

ALTER TABLE checkups
    ADD CONSTRAINT checkups_basics_fk FOREIGN KEY ( basics_id )
        REFERENCES basics ( id );

ALTER TABLE prevention
    ADD CONSTRAINT prevention_basics_fk FOREIGN KEY ( basics_id )
        REFERENCES basics ( id );

ALTER TABLE vaccines
    ADD CONSTRAINT vaccines_basics_fk FOREIGN KEY ( basics_id )
        REFERENCES basics ( id );