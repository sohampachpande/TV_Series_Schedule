import sqlite3 as sql
import re

# Create a database to store queries
table_name = 'TVSeries'
column_names = {'TVSeries':['USER_EMAIL','TVSERIES']}
database_name='user_tv_series.db'

conn = sql.connect(database_name)
# cur = conn.cursor()
conn.execute('CREATE TABLE IF NOT EXISTS TVSeries(USER_EMAIL BLOB NOT NULL,TVSERIES TEXT)')

# take input
user_dict = {}
n = int(input("Enter number of users: ")) 
for k in range(n):
	email = input("\nEnter email address:")
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		print('\nThe email entered is syntatically incorrect')
		email = input("\nEnter email address again: ")
	# seperate the tv series titles and store them in a list
	tv_string = input("\nEnter TV series names seperated by a comma: ")
	tv_string = tv_string.replace(' ','+')
	tv_list = tv_string.split(',')
	user_dict.update({email:tv_list})

print(user_dict)

# store input in database
for user in user_dict:
	for tv_s in user_dict[user]:
			conn.execute('INSERT INTO TVSeries(USER_EMAIL,TVSERIES) VALUES(?,?)', (user, tv_s))
			conn.commit()