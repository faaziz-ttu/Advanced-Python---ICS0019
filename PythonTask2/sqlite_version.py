import sqlite3

#  Create SQLite database DINERS
conn = sqlite3.connect('diners.db')
c = conn.cursor()

#  Create table named PROVIDER
command1 = """CREATE TABLE IF NOT EXISTS PROVIDER (ID INTEGER PRIMARY KEY, ProviderName TEXT)"""
c.execute(command1)

# Create table named CANTEEN which is related to PROVIDER
command2 = """CREATE TABLE IF NOT EXISTS CANTEEN
             (ID INTEGER PRIMARY KEY,
              ProviderID INTEGER,
              Name TEXT,
              Location TEXT,
              time_open TEXT,
              time_closed TEXT,
              FOREIGN KEY (ProviderID) REFERENCES PROVIDER(ID))"""
c.execute(command2)

# 2) Insert IT College canteen data by separate statement, other canteens as one list
provider_name = "Bitt OÜ"
canteen_name = "bitStop KOHVIK"

# check if "Bitt OÜ" already exists in PROVIDER table
c.execute("SELECT ID FROM PROVIDER WHERE ProviderName=?", (provider_name,))
result = c.fetchone()
if result:
    provider_id = result[0]
else:
    c.execute("INSERT INTO PROVIDER (ProviderName) VALUES (?)", (provider_name,))
    provider_id = c.lastrowid

# check if "bitStop KOHVIK" already exists in CANTEEN table
c.execute("SELECT ID FROM CANTEEN WHERE Name=?", (canteen_name,))
result = c.fetchone()
if result:
    canteen_id = result[0]
else:
    c.execute("INSERT INTO CANTEEN ( ProviderID, Name, Location, time_open, time_closed) VALUES (?,?,?,?,?)",
              (provider_id, canteen_name, "IT College, Raja 4c", "9:30", "16:00"))
    canteen_id = c.lastrowid

canteen_data = [
    ("Rahva Toit", "Economics- and social science building canteen", "Akadeemia tee 3", "8:30", "18:30"),
    ("Rahva Toit", "Library canteen", "Akadeemia tee 1/Ehitajate tee 7", "8:30", "19:00"),
    ("Baltic Restaurants Estonia AS", "Main building Deli cafe", "Ehitajate tee 5, U01 building", "9:00", "16:30"),
    ("Baltic Restaurants Estonia AS", "Main building Daily lunch restaurant", "Ehitajate tee 5, U01 building", "9:00",
     "16:30"),
    ("Rahva Toit", "U06 building canteen", "", "9:00", "16:00"),
    ("Baltic Restaurants Estonia AS", "Natural Science building canteen", "Akadeemia tee 15, SCI building", "9:00",
     "16:00"),
    ("Baltic Restaurants Estonia AS", "ICT building canteen", "Raja 15/Mäepealse 1", "9:00", "16:00"),
    ("TTÜ Sport OÜ", "Sports building canteen", "Männiliiva 7, S01 building", "11:00", "20:00")
]

#inserting data into canteen and provider table
for provider_name, canteen_name, location, time_open, time_closed in canteen_data:
    # check if canteen already exists in CANTEEN table for not adding duplicate data to database
    c.execute("SELECT ID FROM CANTEEN WHERE Name=?", (canteen_name,))
    result = c.fetchone()
    if result:
        continue
        # insert CANTEEN data
    c.execute("INSERT INTO CANTEEN (ProviderID, Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?, ?)",
              (provider_id, canteen_name, location, time_open, time_closed))

    # check if provider already exists in PROVIDER table for not adding duplicate data to database
    c.execute("SELECT ID FROM PROVIDER WHERE ProviderName=?", (provider_name,))
    result = c.fetchone()
    if result:
        provider_id = result[0]
    else:
        # insert PROVIDER data
        c.execute("INSERT INTO PROVIDER (ProviderName) VALUES (?)", (provider_name,))
        provider_id = c.lastrowid
    #commit inserts to database
    conn.commit()

# 3) Create query for canteens which are open 09.00-16.20 (full period)
c.execute("""
    SELECT * FROM CANTEEN 
    WHERE time_open <= '09:00' AND time_closed >= '16:20'
""")

results = c.fetchall()

for row in results:
    print(row)

print(end = '\n\n')
# 4) Create query for canteens which are serviced by Baltic Restaurants Estonia AS.
c.execute("""
    SELECT * FROM CANTEEN
    INNER JOIN PROVIDER ON PROVIDER.ID = CANTEEN.ProviderID
    WHERE PROVIDER.ProviderName = 'Baltic Restaurants Estonia AS'
""")

results = c.fetchall()

for row in results:
    print(row)