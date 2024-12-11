import mariadb
from geopy import distance
from random import choice

connection = mariadb.connect(
        user="dbuser",
        password="123456",
        host="127.0.0.1",
        port=3306,
        database="project",
        autocommit=True
    )
cursor = connection.cursor()

class Player:
    """An object to store the information of the player"""
    def __init__(self, player_id):
        self.id = player_id

        name = query_player_data(self.id, "player_name")
        current_funds = query_player_data(self.id, "current_funds")
        current_airport = query_player_data(self.id, "current_airport")
        coordinates = query_airport_coordinates(current_airport)
        time_left = query_player_data(self.id, "time_left")

        self.info = {
            "id": self.id,
            "name": name,
            "current_funds": current_funds,
            "current_airport": current_airport,
            "coordinates": coordinates,
            "time_left": time_left,
        }


def query_player_id(username, password):
    """Query the play's ID by username and password provided by the player after successfully login"""
    sql = f"""
        SELECT player_id
        FROM game
        WHERE game.player_name="{username}" AND game.player_password="{password}";
    """
    cursor.execute(sql)
    response = cursor.fetchone()
    if response:
        player_id = response[0]
    else:
        player_id = response
    return player_id

def query_player_data(player_id, column_name):
    """Query the specific data of a player according to the player's id and specific column name"""
    sql = f"""
        SELECT {column_name} 
        FROM game
        WHERE game.player_id="{player_id}";
    """
    cursor.execute(sql)
    response = cursor.fetchone()
    data = response[0]
    return data

def is_username_registered(username):
    """Check if a username is registered in the database"""
    sql = f"""
        SELECT player_id
        FROM game
        WHERE player_name="{username}";
    """
    cursor.execute(sql)
    response = cursor.fetchone()
    if response:
        return True
    else:
        return False 
    
def register_player(username, password):
    """Insert the new player's data into the game table"""
    initial_airport = generate_random_airport()
    sql = f"""
        INSERT INTO game
        VALUES (DEFAULT, "{username}", "{password}", DEFAULT, "{initial_airport}", DEFAULT);
    """
    cursor.execute(sql)

def generate_random_airport():
    """Generate a random airport as the initially spawned place for a new player"""
    airport_idents = query_all_airport_idents()
    airport = choice(airport_idents)
    return airport

def query_airport_coordinates(ident):
    """Query the airport table about the coordinates of an airport by its ident"""
    sql = f"""
        SELECT latitude_deg, longitude_deg
        FROM airport
        WHERE ident="{ident}";
    """
    cursor.execute(sql)
    coordinates = cursor.fetchone()
    return coordinates

def query_airport_name(ident):
    """Query the airport table about the name of an airport by its ident"""
    sql = f"""
        SELECT name
        FROM airport
        WHERE ident="{ident}";
    """
    cursor.execute(sql)
    name = cursor.fetchone()[0]
    return name

def query_all_airport_idents():
    """Query all airports ident from table airport"""
    sql = f"""
        SELECT ident 
        FROM airport;
    """
    cursor.execute(sql)
    response = cursor.fetchall()
    airport_idents = []
    for item in response:
        airport_idents.append(item[0])
    return airport_idents

def get_all_airports_info(current_airport_ident):
    airports = []
    airports_idents = query_all_airport_idents()
    for ident in airports_idents:
        airport_info = {}
        airport_info["ident"] = ident
        airport_info["name"] = query_airport_name(ident)
        airport_info["coordinates"] = query_airport_coordinates(ident)
        airport_info["travel_time"] = get_travel_time(current_airport_ident, ident)
        airports.append(airport_info)
    return airports

def get_distance(ident1, ident2):
    """Return the distance between two airports by idents"""
    coordinates1 = query_airport_coordinates(ident1)
    coordinates2 = query_airport_coordinates(ident2)
    return distance.distance(coordinates1, coordinates2).km

def get_travel_time(ident1, ident2):
    """Return the travel time of two airports by idents"""
    distance = get_distance(ident1, ident2)
    travel_time = distance / 500

    return float(f"{travel_time:.1f}")
    
def update_player_time_left(player_id, time_left):
    """Update the player's time left"""
    sql = f"""
        UPDATE game
        SET time_left={time_left}
        WHERE player_id={player_id};
    """
    cursor.execute(sql)

def update_player_current_airport(player_id, current_airport):
    """Update the player's current airport"""
    sql = f"""
        UPDATE game
        SET current_airport="{current_airport}"
        WHERE player_id={player_id};
    """
    cursor.execute(sql)

def query_goods_info(ident):
    """Query all goods info of a store by its ident"""
    goods = []

    sql = f"""
        SELECT gida.goods_id, g.name, gida.buy_price, gida.sell_price, gida.stock
        FROM goods_in_different_airport as gida, goods as g
        WHERE gida.airport_ident="{ident}" 
        AND gida.goods_id=g.id;
    """
    cursor.execute(sql)
    result = cursor.fetchall()

    for good in result:
        goods_info = {}
        goods_info["goods_id"] = good[0]
        goods_info["name"] = good[1]
        goods_info["buy_price"] = good[2]
        goods_info["sell_price"] = good[3]
        goods_info["stock"] = good[4]
        goods.append(goods_info)

    return goods

def query_player_inventory(player_id, current_airport_ident):
    """Query the player's inventory"""
    inventory = []

    sql = f"""
        SELECT pi.goods_id,g.name, pi.quantity, gida.sell_price   
        FROM player_inventory as pi, goods_in_different_airport as gida, goods as g
        WHERE pi.player_id={player_id}
        AND gida.airport_ident="{current_airport_ident}"
        AND pi.goods_id=gida.goods_id
        AND pi.goods_id=g.id;
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    
    for good in result:
        goods_info = {
            "goods_id": good[0],
            "goods_name": good[1],
            "quantity": good[2],
            "sell_price": good[3]
        }
        inventory.append(goods_info)

    return inventory

def update_player_funds(player_id, funds):
    """Update the player's current funds in database"""
    sql = f"""
        UPDATE game
        SET current_funds={funds}
        WHERE player_id={player_id};
    """
    cursor.execute(sql)

def update_player_inventory(player_id, goods_id, number):
    """Update the player's inventory"""
    # query the number of the goods in inventory table
    sql = f"""
    SELECT quantity
    FROM player_inventory
    WHERE goods_id={goods_id}
    AND player_id={player_id}
    """
    cursor.execute(sql)
    quantity = cursor.fetchone()

    # check if the goods data exists in the player's inventory
    if quantity is None:
        sql = f"""
        INSERT INTO player_inventory
        VALUE ({player_id}, {goods_id}, {number});
        """
        cursor.execute(sql)
    else:
        quantity = quantity[0]
        # delete the goods data in inventory
        if quantity + number == 0:
            sql = f"""
            DELETE FROM player_inventory
            WHERE goods_id={goods_id}
            AND player_id={player_id};
            """
            cursor.execute(sql)
        # update the goods data in inventory
        else:
            sql = f"""
            UPDATE player_inventory
            SET quantity={number} + {quantity}
            WHERE goods_id={goods_id}
            AND player_id={player_id};
            """
            cursor.execute(sql)

def update_store_stock(airport_ident, goods_id, number):
    """Update the goods' stock of a airport with specific ident number"""
    sql = f"""
    UPDATE goods_in_different_airport
    SET stock=stock + {number}
    WHERE airport_ident="{airport_ident}"
    AND goods_id={goods_id};
    """
    cursor.execute(sql)

def initialize_goods_in_different_airports():
    """Initialize the goods_in_different_airports table before the game begins."""
    cursor.execute(f'DELETE FROM goods_in_different_airport;')
    sql = '''insert into goods_in_different_airport
    values 
        ('KATL',1,143,125,5),
        ('KATL',2,148,132,6),
        ('KATL',3,140,117,6),
        ('KATL',4,158,142,5),
        ('KATL',5,111,97,12),
        ('KATL',6,129,105,6),
        ('KATL',7,140,114,7),
        ('KATL',8,112,95,12),
        ('KATL',9,87,77,15),
        ('KATL',10,82,66,17),
        ('KATL',11,139,122,9),
        ('KATL',12,149,128,9),
        ('KATL',13,144,122,5),
        ('KATL',14,157,138,5),
        ('KATL',15,87,74,17),
        ('KATL',16,81,65,18),
        ('KATL',17,134,116,8),
        ('KATL',18,152,127,9),
        ('KATL',19,124,110,9),
        ('KATL',20,108,92,13),
        ('KATL',21,110,94,12),
        ('KATL',22,158,138,9),
        ('KATL',23,82,68,16),
        ('KATL',24,95,80,17),
        ('KATL',25,135,110,9),
        ('KATL',26,123,103,9),
        ('KATL',27,142,122,9),
        ('KATL',28,136,118,8),
        ('KATL',29,126,111,7),
        ('KATL',30,134,118,6),
        ('KAUS',1,144,123,9),
        ('KAUS',2,157,131,5),
        ('KAUS',3,94,76,17),
        ('KAUS',4,88,74,18),
        ('KAUS',5,111,97,12),
        ('KAUS',6,121,101,5),
        ('KAUS',7,142,128,7),
        ('KAUS',8,112,95,12),
        ('KAUS',9,154,128,8),
        ('KAUS',10,133,119,5),
        ('KAUS',11,154,136,8),
        ('KAUS',12,154,130,9),
        ('KAUS',13,138,117,5),
        ('KAUS',14,135,111,9),
        ('KAUS',15,147,126,6),
        ('KAUS',16,152,127,8),
        ('KAUS',17,140,125,6),
        ('KAUS',18,151,132,6),
        ('KAUS',19,130,114,7),
        ('KAUS',20,108,92,13),
        ('KAUS',21,110,94,12),
        ('KAUS',22,159,129,9),
        ('KAUS',23,143,122,8),
        ('KAUS',24,135,109,6),
        ('KAUS',25,82,66,18),
        ('KAUS',26,92,80,15),
        ('KAUS',27,94,80,18),
        ('KAUS',28,89,75,15),
        ('KAUS',29,91,78,18),
        ('KAUS',30,80,67,16),
        ('KBNA',1,88,75,16),
        ('KBNA',2,89,76,15),
        ('KBNA',3,135,109,9),
        ('KBNA',4,159,141,6),
        ('KBNA',5,111,97,12),
        ('KBNA',6,85,69,15),
        ('KBNA',7,126,110,5),
        ('KBNA',8,112,95,12),
        ('KBNA',9,124,107,6),
        ('KBNA',10,141,125,6),
        ('KBNA',11,99,85,17),
        ('KBNA',12,93,79,18),
        ('KBNA',13,81,68,18),
        ('KBNA',14,99,84,16),
        ('KBNA',15,120,102,6),
        ('KBNA',16,122,109,5),
        ('KBNA',17,132,108,7),
        ('KBNA',18,135,112,9),
        ('KBNA',19,148,128,5),
        ('KBNA',20,108,92,13),
        ('KBNA',21,110,94,12),
        ('KBNA',22,120,97,5),
        ('KBNA',23,126,108,6),
        ('KBNA',24,128,110,5),
        ('KBNA',25,135,113,5),
        ('KBNA',26,156,138,5),
        ('KBNA',27,135,112,5),
        ('KBNA',28,156,125,6),
        ('KBNA',29,128,103,5),
        ('KBNA',30,122,101,5),
        ('KBOS',1,126,102,6),
        ('KBOS',2,121,104,9),
        ('KBOS',3,84,73,16),
        ('KBOS',4,96,85,15),
        ('KBOS',5,111,97,12),
        ('KBOS',6,150,130,7),
        ('KBOS',7,151,128,8),
        ('KBOS',8,112,95,12),
        ('KBOS',9,137,116,5),
        ('KBOS',10,123,100,7),
        ('KBOS',11,140,118,7),
        ('KBOS',12,123,105,9),
        ('KBOS',13,144,122,5),
        ('KBOS',14,141,124,9),
        ('KBOS',15,157,134,7),
        ('KBOS',16,151,124,6),
        ('KBOS',17,132,114,5),
        ('KBOS',18,133,113,9),
        ('KBOS',19,159,137,9),
        ('KBOS',20,108,92,13),
        ('KBOS',21,110,94,12),
        ('KBOS',22,139,113,5),
        ('KBOS',23,140,119,6),
        ('KBOS',24,134,108,5),
        ('KBOS',25,85,75,15),
        ('KBOS',26,92,80,18),
        ('KBOS',27,95,77,15),
        ('KBOS',28,99,83,17),
        ('KBOS',29,80,71,17),
        ('KBOS',30,99,89,18),
        ('KBUF',1,123,101,7),
        ('KBUF',2,148,119,7),
        ('KBUF',3,155,136,7),
        ('KBUF',4,155,136,5),
        ('KBUF',5,111,97,12),
        ('KBUF',6,121,99,8),
        ('KBUF',7,141,119,6),
        ('KBUF',8,112,95,12),
        ('KBUF',9,98,83,16),
        ('KBUF',10,96,82,18),
        ('KBUF',11,149,123,6),
        ('KBUF',12,138,120,6),
        ('KBUF',13,125,108,5),
        ('KBUF',14,138,114,9),
        ('KBUF',15,88,73,18),
        ('KBUF',16,88,76,18),
        ('KBUF',17,155,130,9),
        ('KBUF',18,155,125,7),
        ('KBUF',19,137,112,7),
        ('KBUF',20,108,92,13),
        ('KBUF',21,110,94,12),
        ('KBUF',22,123,104,5),
        ('KBUF',23,81,68,16),
        ('KBUF',24,97,85,18),
        ('KBUF',25,151,129,7),
        ('KBUF',26,128,107,8),
        ('KBUF',27,147,121,9),
        ('KBUF',28,145,117,5),
        ('KBUF',29,134,114,8),
        ('KBUF',30,154,132,5),
        ('KDEN',1,130,107,8),
        ('KDEN',2,154,131,7),
        ('KDEN',3,126,112,5),
        ('KDEN',4,122,109,9),
        ('KDEN',5,111,97,12),
        ('KDEN',6,141,121,7),
        ('KDEN',7,124,105,7),
        ('KDEN',8,112,95,12),
        ('KDEN',9,88,74,17),
        ('KDEN',10,93,83,18),
        ('KDEN',11,139,117,6),
        ('KDEN',12,146,122,5),
        ('KDEN',13,127,108,7),
        ('KDEN',14,153,128,8),
        ('KDEN',15,91,77,16),
        ('KDEN',16,92,76,15),
        ('KDEN',17,152,133,6),
        ('KDEN',18,138,123,9),
        ('KDEN',19,136,116,7),
        ('KDEN',20,108,92,13),
        ('KDEN',21,110,94,12),
        ('KDEN',22,123,99,5),
        ('KDEN',23,95,78,17),
        ('KDEN',24,84,73,18),
        ('KDEN',25,132,118,9),
        ('KDEN',26,143,122,9),
        ('KDEN',27,127,112,6),
        ('KDEN',28,132,111,6),
        ('KDEN',29,140,123,6),
        ('KDEN',30,141,122,7),
        ('KDFW',1,128,112,8),
        ('KDFW',2,147,118,5),
        ('KDFW',3,122,109,9),
        ('KDFW',4,159,133,7),
        ('KDFW',5,111,97,12),
        ('KDFW',6,151,134,7),
        ('KDFW',7,130,110,8),
        ('KDFW',8,112,95,12),
        ('KDFW',9,87,75,17),
        ('KDFW',10,88,75,16),
        ('KDFW',11,139,116,6),
        ('KDFW',12,128,109,9),
        ('KDFW',13,127,106,6),
        ('KDFW',14,153,126,5),
        ('KDFW',15,96,78,17),
        ('KDFW',16,89,79,15),
        ('KDFW',17,128,105,5),
        ('KDFW',18,145,121,5),
        ('KDFW',19,152,137,8),
        ('KDFW',20,108,92,13),
        ('KDFW',21,110,94,12),
        ('KDFW',22,142,117,6),
        ('KDFW',23,90,78,18),
        ('KDFW',24,86,76,15),
        ('KDFW',25,153,126,6),
        ('KDFW',26,154,131,7),
        ('KDFW',27,122,109,6),
        ('KDFW',28,160,130,9),
        ('KDFW',29,132,118,6),
        ('KDFW',30,127,104,6),
        ('KDTW',1,142,115,9),
        ('KDTW',2,134,120,7),
        ('KDTW',3,148,124,7),
        ('KDTW',4,124,111,6),
        ('KDTW',5,111,97,12),
        ('KDTW',6,125,107,5),
        ('KDTW',7,158,141,7),
        ('KDTW',8,112,95,12),
        ('KDTW',9,99,83,18),
        ('KDTW',10,94,84,15),
        ('KDTW',11,150,125,5),
        ('KDTW',12,154,136,7),
        ('KDTW',13,142,118,5),
        ('KDTW',14,126,101,6),
        ('KDTW',15,89,73,17),
        ('KDTW',16,100,89,17),
        ('KDTW',17,156,125,6),
        ('KDTW',18,156,130,5),
        ('KDTW',19,139,121,5),
        ('KDTW',20,108,92,13),
        ('KDTW',21,110,94,12),
        ('KDTW',22,123,101,6),
        ('KDTW',23,100,81,16),
        ('KDTW',24,97,85,17),
        ('KDTW',25,121,106,6),
        ('KDTW',26,158,133,6),
        ('KDTW',27,130,114,7),
        ('KDTW',28,130,114,8),
        ('KDTW',29,122,101,5),
        ('KDTW',30,153,126,6),
        ('KJFK',1,149,124,9),
        ('KJFK',2,146,117,8),
        ('KJFK',3,94,76,18),
        ('KJFK',4,100,82,15),
        ('KJFK',5,111,97,12),
        ('KJFK',6,131,116,9),
        ('KJFK',7,154,131,8),
        ('KJFK',8,112,95,12),
        ('KJFK',9,154,137,7),
        ('KJFK',10,127,103,5),
        ('KJFK',11,154,136,6),
        ('KJFK',12,136,121,6),
        ('KJFK',13,156,125,6),
        ('KJFK',14,128,106,5),
        ('KJFK',15,138,117,7),
        ('KJFK',16,150,130,7),
        ('KJFK',17,133,116,5),
        ('KJFK',18,147,127,5),
        ('KJFK',19,158,142,7),
        ('KJFK',20,108,92,13),
        ('KJFK',21,110,94,12),
        ('KJFK',22,140,123,7),
        ('KJFK',23,135,116,5),
        ('KJFK',24,125,110,7),
        ('KJFK',25,83,69,15),
        ('KJFK',26,86,76,18),
        ('KJFK',27,89,73,18),
        ('KJFK',28,99,88,17),
        ('KJFK',29,91,78,16),
        ('KJFK',30,81,67,16),
        ('KLAS',1,151,132,9),
        ('KLAS',2,130,114,6),
        ('KLAS',3,86,74,18),
        ('KLAS',4,83,73,15),
        ('KLAS',5,111,97,12),
        ('KLAS',6,159,138,9),
        ('KLAS',7,145,128,6),
        ('KLAS',8,112,95,12),
        ('KLAS',9,146,131,9),
        ('KLAS',10,138,118,8),
        ('KLAS',11,140,124,9),
        ('KLAS',12,127,109,9),
        ('KLAS',13,132,112,9),
        ('KLAS',14,143,125,9),
        ('KLAS',15,137,112,7),
        ('KLAS',16,130,113,8),
        ('KLAS',17,124,109,7),
        ('KLAS',18,144,116,8),
        ('KLAS',19,149,133,5),
        ('KLAS',20,108,92,13),
        ('KLAS',21,110,94,12),
        ('KLAS',22,142,114,7),
        ('KLAS',23,121,103,5),
        ('KLAS',24,149,122,7),
        ('KLAS',25,99,86,17),
        ('KLAS',26,91,79,15),
        ('KLAS',27,99,85,15),
        ('KLAS',28,95,82,15),
        ('KLAS',29,100,84,18),
        ('KLAS',30,86,77,17),
        ('KLAX',1,129,114,7),
        ('KLAX',2,152,123,5),
        ('KLAX',3,84,67,16),
        ('KLAX',4,83,73,16),
        ('KLAX',5,111,97,12),
        ('KLAX',6,156,137,8),
        ('KLAX',7,127,106,6),
        ('KLAX',8,112,95,12),
        ('KLAX',9,142,121,5),
        ('KLAX',10,148,121,8),
        ('KLAX',11,151,125,6),
        ('KLAX',12,136,121,5),
        ('KLAX',13,141,123,9),
        ('KLAX',14,132,117,5),
        ('KLAX',15,155,128,5),
        ('KLAX',16,159,138,8),
        ('KLAX',17,149,127,7),
        ('KLAX',18,134,115,9),
        ('KLAX',19,121,100,5),
        ('KLAX',20,108,92,13),
        ('KLAX',21,110,94,12),
        ('KLAX',22,130,112,7),
        ('KLAX',23,126,109,8),
        ('KLAX',24,156,134,5),
        ('KLAX',25,97,87,16),
        ('KLAX',26,92,75,18),
        ('KLAX',27,97,87,18),
        ('KLAX',28,95,77,15),
        ('KLAX',29,100,85,18),
        ('KLAX',30,83,71,18),
        ('KMIA',1,137,110,9),
        ('KMIA',2,126,107,6),
        ('KMIA',3,157,133,5),
        ('KMIA',4,126,111,9),
        ('KMIA',5,111,97,12),
        ('KMIA',6,144,129,5),
        ('KMIA',7,94,83,17),
        ('KMIA',8,112,95,12),
        ('KMIA',9,145,127,5),
        ('KMIA',10,126,112,9),
        ('KMIA',11,135,112,9),
        ('KMIA',12,132,118,5),
        ('KMIA',13,135,116,9),
        ('KMIA',14,145,118,9),
        ('KMIA',15,148,133,6),
        ('KMIA',16,127,108,9),
        ('KMIA',17,84,72,17),
        ('KMIA',18,82,67,18),
        ('KMIA',19,85,70,18),
        ('KMIA',20,108,92,13),
        ('KMIA',21,110,94,12),
        ('KMIA',22,96,82,17),
        ('KMIA',23,153,125,5),
        ('KMIA',24,131,109,8),
        ('KMIA',25,120,96,7),
        ('KMIA',26,133,109,5),
        ('KMIA',27,155,124,8),
        ('KMIA',28,124,105,6),
        ('KMIA',29,151,122,9),
        ('KMIA',30,131,108,7),
        ('KORD',1,121,106,7),
        ('KORD',2,137,112,5),
        ('KORD',3,157,134,5),
        ('KORD',4,150,125,6),
        ('KORD',5,111,97,12),
        ('KORD',6,138,116,5),
        ('KORD',7,136,116,9),
        ('KORD',8,112,95,12),
        ('KORD',9,83,75,18),
        ('KORD',10,95,76,15),
        ('KORD',11,157,129,5),
        ('KORD',12,156,140,5),
        ('KORD',13,132,110,9),
        ('KORD',14,129,110,8),
        ('KORD',15,88,76,15),
        ('KORD',16,88,77,15),
        ('KORD',17,158,141,6),
        ('KORD',18,135,111,5),
        ('KORD',19,128,106,5),
        ('KORD',20,108,92,13),
        ('KORD',21,110,94,12),
        ('KORD',22,131,112,8),
        ('KORD',23,83,72,16),
        ('KORD',24,83,73,16),
        ('KORD',25,149,130,9),
        ('KORD',26,144,121,8),
        ('KORD',27,152,132,9),
        ('KORD',28,128,107,5),
        ('KORD',29,148,131,7),
        ('KORD',30,123,99,8),
        ('KSEA',1,148,131,9),
        ('KSEA',2,154,125,5),
        ('KSEA',3,121,107,8),
        ('KSEA',4,160,128,6),
        ('KSEA',5,111,97,12),
        ('KSEA',6,156,128,6),
        ('KSEA',7,93,81,16),
        ('KSEA',8,112,95,12),
        ('KSEA',9,134,114,7),
        ('KSEA',10,135,120,7),
        ('KSEA',11,123,107,9),
        ('KSEA',12,139,112,6),
        ('KSEA',13,129,104,8),
        ('KSEA',14,141,113,8),
        ('KSEA',15,135,121,7),
        ('KSEA',16,133,115,6),
        ('KSEA',17,87,74,18),
        ('KSEA',18,87,75,16),
        ('KSEA',19,97,85,18),
        ('KSEA',20,108,92,13),
        ('KSEA',21,110,94,12),
        ('KSEA',22,81,66,18),
        ('KSEA',23,145,117,9),
        ('KSEA',24,121,109,6),
        ('KSEA',25,149,130,8),
        ('KSEA',26,149,130,7),
        ('KSEA',27,133,114,8),
        ('KSEA',28,154,130,9),
        ('KSEA',29,129,111,8),
        ('KSEA',30,157,134,8),
        ('KSFO',1,122,109,8),
        ('KSFO',2,133,108,5),
        ('KSFO',3,83,72,18),
        ('KSFO',4,82,68,18),
        ('KSFO',5,111,97,12),
        ('KSFO',6,123,108,6),
        ('KSFO',7,145,127,5),
        ('KSFO',8,112,95,12),
        ('KSFO',9,131,112,9),
        ('KSFO',10,151,136,5),
        ('KSFO',11,134,112,9),
        ('KSFO',12,155,135,8),
        ('KSFO',13,152,131,9),
        ('KSFO',14,158,142,8),
        ('KSFO',15,142,127,5),
        ('KSFO',16,144,126,5),
        ('KSFO',17,158,127,8),
        ('KSFO',18,127,102,7),
        ('KSFO',19,158,140,5),
        ('KSFO',20,108,92,13),
        ('KSFO',21,110,94,12),
        ('KSFO',22,134,115,5),
        ('KSFO',23,142,126,5),
        ('KSFO',24,138,118,6),
        ('KSFO',25,82,67,16),
        ('KSFO',26,84,68,17),
        ('KSFO',27,96,78,18),
        ('KSFO',28,85,69,16),
        ('KSFO',29,97,81,15),
        ('KSFO',30,95,79,17);'''
    cursor.execute(sql)


if __name__ == "__main__":
    initialize_goods_in_different_airports()