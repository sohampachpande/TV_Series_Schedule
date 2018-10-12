import sqlite3 as sql
import re
import email_func
import retrieve_imdb_data as imdb

# Create a database to store queries
table_name = 'TVSeries'
column_names = {'TVSeries':['USER_EMAIL','TVSERIES']}
database_name='user_tv_series.db'

conn = sql.connect(database_name)
cur = conn.cursor()
# We keep the tuple (user_email, tvseries) unique so that entries don't get duplicated
conn.execute('CREATE TABLE IF NOT EXISTS TVSeries(USER_EMAIL TEXT NOT NULL,TVSERIES TEXT,UNIQUE(USER_EMAIL,TVSERIES))')

# get list of all distinct email addresses in database
def get_distinct_email_address():
	cur.execute('SELECT DISTINCT USER_EMAIL FROM TVSeries')
	all_row = cur.fetchall()
	user_email_unique = []
	for row in all_row:
		user_email_unique.append(row[0])
	return user_email_unique


# retreive data from database, call required functions to get information about schedule, form email content text and call function to send email for given user
def make_content(user):
	body_content=''
	cur.execute('SELECT TVSERIES FROM TVSeries WHERE USER_EMAIL="{}"'.format(user))
	all_tv = cur.fetchall()
	print(all_tv)
	for tv_title in all_tv:
		body_content += 'TVSeries: {}\nStatus: {}\n\n'.format(tv_title[0].replace('+',' '), imdb.get_final_schedule(tv_title[0]))
		print('TVSeries: {}'.format(tv_title[0].replace('+',' ')))
		print(imdb.get_final_schedule(tv_title[0]))
	return body_content


# take input
user_dict = {}
n = int(input("Enter number of users: ")) 
for k in range(n):
	email = input("\nEnter email address:")
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		print('\nThe email entered is syntatically incorrect')
		email = input("\nEnter email address again: ")
	# split the tv series titles and store them in a list
	tv_string = input("\nEnter TV series names seperated by a comma: ")
	tv_string = tv_string.replace(' ','+')
	tv_list = tv_string.split(',')
	user_dict.update({email:tv_list})

# store input in database
for user in user_dict:
	for tv_s in user_dict[user]:
			conn.execute('INSERT OR IGNORE INTO TVSeries(USER_EMAIL,TVSERIES) VALUES(?,?)', (user, tv_s))
			conn.commit()

# send mails
m = input("Enter 'all' (without quotes) if you want to mail to all the user emails.\nEnter comma seperated email-ids and mail would be sent to the email existing in the database:")
user_email_unique = get_distinct_email_address()
if m == 'all':
	for u in user_email_unique:
		body_content = make_content(u)
		email_func.send_email(body_content, u)
else:
	email_list = m.replace(' ','').split(',')
	for u in email_list:
		if u in user_email_unique:
			body_content = make_content(u)
			email_func.send_email(body_content, u)
