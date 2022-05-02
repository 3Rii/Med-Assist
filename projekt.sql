CREATE TABLE accounts 
    (
     id NUMERIC (28) NOT NULL , 
     fullname VARCHAR (25) NOT NULL , 
     username VARCHAR (25) NOT NULL , 
     password VARCHAR (25) NOT NULL , 
     email VARCHAR (25) 
    )
;

ALTER TABLE accounts ADD CONSTRAINT accounts_pk PRIMARY KEY CLUSTERED (id)
    ;
    ALTER TABLE accounts ADD CONSTRAINT accounts_username_un UNIQUE NONCLUSTERED (username)
    ;

CREATE TABLE basics 
    (
     id NUMERIC (28) NOT NULL , 
     wiek NUMERIC (2) NOT NULL , 
     waga NUMERIC (3) NOT NULL , 
     wzrost NUMERIC (3) NOT NULL , 
     plec CHAR (1) NOT NULL , 
     papierosy CHAR (1) NOT NULL , 
     alkohol CHAR (1) NOT NULL , 
     aktywnosc VARCHAR (25) NOT NULL , 
     accounts_id NUMERIC (28) NOT NULL 
    )
; 


    


CREATE UNIQUE INDEX 
    basics__idx ON basics 
    ( 
     accounts_id 
    ) 
;

ALTER TABLE basics ADD CONSTRAINT basics_pk PRIMARY KEY CLUSTERED (id)
    ;

CREATE TABLE checkups 
    (
     id NUMERIC (28) NOT NULL , 
     nazwa VARCHAR (25) NOT NULL , 
     status VARCHAR (25) NOT NULL , 
     basics_id NUMERIC (28) NOT NULL 
    )
;

ALTER TABLE checkups ADD CONSTRAINT checkups_pk PRIMARY KEY CLUSTERED (id)
    ;

CREATE TABLE prevention 
    (
     id NUMERIC (28) NOT NULL , 
     nazwa VARCHAR (25) NOT NULL , 
     link VARCHAR (25) NOT NULL , 
     status VARCHAR (25) NOT NULL , 
     basics_id NUMERIC (28) NOT NULL 
    )
;

ALTER TABLE prevention ADD CONSTRAINT prevention_pk PRIMARY KEY CLUSTERED (id)
    ;

CREATE TABLE vaccines 
    (
     id NUMERIC (28) NOT NULL , 
     nazwa VARCHAR (25) NOT NULL , 
     typ VARCHAR (25) NOT NULL , 
     status VARCHAR (25) NOT NULL , 
     basics_id NUMERIC (28) NOT NULL 
    )
;

ALTER TABLE vaccines ADD CONSTRAINT vaccines_pk PRIMARY KEY CLUSTERED (id)
    ;

ALTER TABLE basics 
    ADD CONSTRAINT basics_accounts_fk FOREIGN KEY 
    ( 
     accounts_id
    ) 
    REFERENCES accounts 
    ( 
     id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
;

ALTER TABLE checkups 
    ADD CONSTRAINT checkups_basics_fk FOREIGN KEY 
    ( 
     basics_id
    ) 
    REFERENCES basics 
    ( 
     id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
;

ALTER TABLE prevention 
    ADD CONSTRAINT prevention_basics_fk FOREIGN KEY 
    ( 
     basics_id
    ) 
    REFERENCES basics 
    ( 
     id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
;

ALTER TABLE vaccines 
    ADD CONSTRAINT vaccines_basics_fk FOREIGN KEY 
    ( 
     basics_id
    ) 
    REFERENCES basics 
    ( 
     id 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
;
