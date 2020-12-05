import sqlite3

conn = sqlite3.connect('Logs.db')

c = conn.cursor()

c.execute("DROP TABLE Log404")

# Create table
c.execute('''CREATE TABLE Log404 (
    Id INTEGER PRIMARY KEY, 
    LogDate DATETIME,
    URL VARCHAR(300), 
    ShouldIgnore bit,
    IPAddress VARCHAR(100),
    Verb VARCHAR(10), 
    StatusCode INT, 
    Size INT, 
    Referrer VARCHAR(200), 
    Raw TEXT
    )''')

# Create an index for our most used query
c.execute("CREATE INDEX IX_URL ON Log404 (URL,ShouldIgnore,LogDate);")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()