INSERT INTO vacc VALUES (1,'rozyczka', 'nw', 0, 0);
INSERT INTO vacc VALUES (2,'gruzlica', 'nw', 0, 0);
INSERT INTO check_ups VALUES (1,'mammografia', 0, 0);
INSERT INTO check_ups VALUES (2,'cytologia',0, 0);
INSERT INTO check_ups VALUES (3,'prostata',0, 0);
INSERT INTO check_ups VALUES (4,'lipidogram',0, 0);


/*  resetowanie statusu w bazie
UPDATE vacc SET current_status = 0 WHERE id = 1;
UPDATE vacc SET current_status = 0 WHERE id = 2;
UPDATE check_ups SET current_status = 0 WHERE id = 1;
UPDATE check_ups SET current_status = 0 WHERE id = 2;
UPDATE check_ups SET current_status = 0 WHERE id = 3;
UPDATE check_ups SET current_status = 0 WHERE id = 4;

*/
