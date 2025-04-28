-- -- 1
-- SELECT Arrest_ID, Arrest_Date, 
-- Law_Code, Offense_Level 
-- FROM Arrests;

-- -- 2
-- SELECT ad.Arrest_Borough, 
-- a.Offense_Level, COUNT(*) 
-- AS Arrest_Count 
-- FROM Arrests a 
-- JOIN Arrest_Details ad 
-- ON a.Arrest_ID = ad.Arrest_ID 
-- GROUP BY ad.Arrest_Borough, 
-- a.Offense_Level;

--  -- --3
-- SELECT p.Arrest_ID, p.Age, 
-- p.Sex, p.Race 
-- FROM Perpetrators p 
-- WHERE p.Age > (SELECT AVG(Age) 
-- FROM Perpetrators);

-- -- 4
-- SELECT a.Arrest_ID, a.Arrest_Date, 
-- ot.Offense_Desc, p.Age, 
-- ad.Arrest_Borough 
-- FROM Arrests a 
-- JOIN Arrest_Offenses ao 
-- ON a.Arrest_ID = ao.Arrest_ID 
-- JOIN Offense_Types ot 
-- ON ao.Offense_Code = ot.Offense_Code 
-- JOIN Perpetrators p 
-- ON a.Arrest_ID = p.Arrest_ID 
-- JOIN Arrest_Details ad 
-- ON a.Arrest_ID = ad.Arrest_ID;

-- -- 5 
-- INSERT INTO Arrests (Arrest_ID, 
-- Arrest_Date, Law_Code, 
-- Offense_Level) 
-- VALUES ('A123456', '2023-06-01', 
-- 'PL 120.00', 'F');

-- -- 6
-- INSERT INTO Perpetrators (Arrest_ID, 
-- Age, Sex, Race) 
-- VALUES ('A123456', 30, 'M', 
-- 'WHITE');

-- --7
-- UPDATE Arrest_Details 
-- SET Arrest_Borough = 'M' 
-- WHERE Arrest_ID = 'A123456';

--8 
-- UPDATE Offense_Types 
-- SET Offense_Desc = 
-- 'ASSAULT 3RD DEGREE' 
-- WHERE Offense_Code = 101;

--9 
-- DELETE FROM Arrest_Offenses 
-- WHERE Arrest_ID = 'A123456' 
-- AND Offense_Code = 101;
