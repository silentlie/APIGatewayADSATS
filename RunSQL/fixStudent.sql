DELETE 
FROM staff_roles 
WHERE staff_id = 0;
DELETE
FROM aircraft_crew
WHERE staff_id = 0;
DELETE
FROM staff
WHERE staff_id = 0;
SELECT * FROM staff_roles WHERE staff_id = 0;
SELECT * FROM aircraft_crew WHERE staff_id = 0;
SELECT * FROM staff WHERE staff_id = 0;