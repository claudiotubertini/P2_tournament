-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players ( 	id SERIAL PRIMARY KEY,
						fullname TEXT NOT NULL);


DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches ( id int PRIMARY KEY); 

DROP TABLE IF EXISTS results CASCADE;
CREATE TABLE results (	id_player int references players(id) ON DELETE CASCADE,
						id_match int references matches(id) ON DELETE CASCADE,
						result text,
                        byeresult boolean
						-- CONSTRAINT result_check CHECK ((((result = 'Win'::text) OR (result = 'Draw'::text)) OR (result = 'Lose'::text)) OR (result = 'Bye'::text))
						);
CREATE UNIQUE INDEX tests_bye_results ON results (id_player, result) WHERE result = 'Bye';
--CREATE DOMAIN result VARCHAR(10) CHECK (UPPER(VALUE) IN ('WIN', 'DRAW', 'LOSE', 'BYE'));

CREATE OR REPLACE VIEW view_points AS 
    SELECT id_player, SUM(
        CASE WHEN result='Win' THEN 2
            WHEN result='Draw' THEN 1
            WHEN result='Lose' THEN 0
            WHEN result='Bye' THEN 2
            ELSE 0
        END) AS points, COUNT(id_match) AS matches
    FROM results
    GROUP BY id_player
    ORDER BY points DESC;

CREATE OR REPLACE FUNCTION trigger_function()
  RETURNS trigger AS $$
BEGIN
IF (TG_OP = 'DELETE') THEN
    IF EXISTS (SELECT * FROM results LIMIT 1) THEN 
        DELETE FROM results WHERE id_player = (SELECT id FROM players);
    END IF;
ELSIF (TG_OP = 'INSERT') THEN
    INSERT INTO results(id_player) VALUES (NEW.id);
END IF;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS pop_results on players;
CREATE TRIGGER pop_results
AFTER INSERT OR DELETE ON players
    FOR EACH ROW EXECUTE PROCEDURE trigger_function();

-- CREATE OR REPLACE FUNCTION function_copy() 
-- RETURNS TRIGGER AS
-- $BODY$
-- BEGIN
--     INSERT INTO
--         matches(id)
--         VALUES(new.id);
--     RETURN new;
-- END;
-- $BODY$
-- LANGUAGE plpgsql;


-- DROP TRIGGER IF EXISTS match_results on results;
-- CREATE TRIGGER match_results
-- BEFORE INSERT ON results
--     FOR EACH ROW EXECUTE PROCEDURE function_copy();

CREATE OR REPLACE FUNCTION trigger_matches()
  RETURNS trigger AS $BODY$
BEGIN
IF (TG_OP = 'DELETE') THEN
    IF EXISTS (SELECT * FROM results LIMIT 1) THEN 
        DELETE FROM results WHERE id_match = (SELECT id FROM matches);
    END IF;
END IF;
RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS matches_results on matches;
CREATE TRIGGER matches_results
AFTER DELETE ON matches
    FOR EACH ROW EXECUTE PROCEDURE trigger_matches();
