#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit() 
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit() 
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    res = c.fetchone()
    conn.close()
    return int(res[0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (fullname) VALUES (%s);", (name,))
    conn.commit() 
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id_player, points, matches, fullname FROM view_points INNER JOIN players ON id_player = id \
        ORDER BY points DESC, matches DESC ;")
    rows = c.fetchall()
    conn.close()
    return [(id_player, fullname, int(points), int(matches)) for id_player, points, matches, fullname in rows] 


def reportMatch(draw, matchN, winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      draw: boolean value, true if the match is drawn
      matchN: the id number of the match played by winner and loser
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    if draw:
        args = [(winner, matchN, "Draw", False), (loser, matchN, "Draw", False)]
    else:
        args = [(winner, matchN, "Win", False), (loser, matchN, "Lose", False)]
    records_template = ','.join(['%s'] * len(args))
    # check if matches foreign index is already present
    c.execute("SELECT * FROM matches WHERE id = %s;", (matchN,))
    if c.fetchone() is not None:
        insert_query = 'INSERT INTO results (id_player, id_match, result, byeresult) values {0}'.format(records_template)
        c.execute(insert_query, args)
    else:
        c.execute('INSERT INTO matches (id) values (%s);', (matchN,))
        insert_query = 'INSERT INTO results (id_player, id_match, result, byeresult) values {0}'.format(records_template)
        c.execute(insert_query, args)
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    plyrs = playerStandings()
    
    plyrs = zip([row[0] for row in plyrs], [row[1] for row in plyrs])
    
    return [(plyrs[i][0],plyrs[i][1],plyrs[i+1][0],plyrs[i+1][1]) for i in range(0, len(plyrs), 2)]
  

