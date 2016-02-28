
#The purpose of each file
The database can manage only an even number of players, with matches that result in draw, win or lose.
_tournament.sql_  - this file is used to set up the database. I've used a table for _players_ with id and full name, a table that list _matches_ id, in the sense of ordered number of matches in a tournament. The first match will be the number 1 for all the players. Actually I do not implemented the tournaments but the tables are basically ready for that. There is a table that lists _results_ with the name of players and the reference to the match played. The match result can be only one of win, lose, draw. The order standing is obtained through a view on table _results_

_tournament.py_ - this file is used to provide access to the database via a library of functions which can add, delete or query data in the database to a client program.
_tournament\_test.py_ - this is a client program which will use the functions written in the tournament.py module. 

