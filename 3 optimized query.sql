
-- -- optimization 
-- -- 1.a
-- SELECT A.arrest_id, A.arrest_date
-- FROM Arrests A
-- JOIN Arrest_Offenses AO ON A.arrest_id = AO.arrest_id
-- JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
-- WHERE OT.category_desc = 'FELONY ASSAULT';

-- -- 1.b
-- SELECT A.arrest_id, A.arrest_date
-- FROM Arrests A
-- WHERE EXISTS (
--     SELECT 1
--     FROM Arrest_Offenses AO
--     JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
--     WHERE AO.arrest_id = A.arrest_id
--       AND OT.category_desc = 'FELONY ASSAULT'
-- );

-- -- 2.a
-- SELECT DISTINCT AD.arrest_precinct
-- FROM Arrests A
-- JOIN Arrest_Offenses AO ON A.arrest_id = AO.arrest_id
-- JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
-- JOIN Arrest_Details AD ON A.arrest_id = AD.arrest_id
-- WHERE OT.category_desc = 'DANGEROUS DRUGS';

-- -- 2.b
-- SELECT AD.arrest_precinct
-- FROM Arrests A
-- JOIN Arrest_Offenses AO ON A.arrest_id = AO.arrest_id
-- JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
-- JOIN Arrest_Details AD ON A.arrest_id = AD.arrest_id
-- WHERE OT.category_desc = 'DANGEROUS DRUGS'
-- GROUP BY AD.arrest_precinct;

-- -- 3.a
-- SELECT A.arrest_id, A.arrest_date, OT.offense_desc
-- FROM Arrests A
-- JOIN Arrest_Offenses AO ON A.arrest_id = AO.arrest_id
-- JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
-- WHERE A.arrest_date BETWEEN '2023-01-01' AND '2023-12-31'
--   AND OT.category_desc = 'ROBBERY';

-- -- 3.b
-- WITH Filtered_Arrests AS (
--     SELECT arrest_id, arrest_date
--     FROM Arrests
--     WHERE arrest_date BETWEEN '2023-01-01' AND '2023-12-31'
-- )
-- SELECT FA.arrest_id, FA.arrest_date, OT.offense_desc
-- FROM Filtered_Arrests FA
-- JOIN Arrest_Offenses AO ON FA.arrest_id = AO.arrest_id
-- JOIN Offense_Types OT ON AO.offense_code = OT.offense_code
-- WHERE OT.category_desc = 'ROBBERY';
