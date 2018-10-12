import sqlite3 as sql
import retrieve_imdb_data as imdb

table_name = 'TVSeries'
column_names = {'TVSeries':['USER_EMAIL','TVSERIES']}
database_name='user_tv_series.db'
conn = sql.connect(database_name)
cur=conn.cursor()	

def get_distinct_email_address():
	cur.execute('SELECT DISTINCT USER_EMAIL FROM TVSeries')
	all_row = cur.fetchall()
	user_email_unique = []
	for row in all_row:
		user_email_unique.append(row[0])
	return user_email_unique


# retreive data from database, call required functions to get information about schedule, form email content text and call function to send email for given user
def make_content(user):

	cur.execute('SELECT TVSERIES FROM TVSeries WHERE USER_EMAIL="{}"'.format(user))
	all_tv = cur.fetchall()
	print(all_tv)
	for tv_title in all_tv:
		print('TVSeries: {}'.format(tv_title[0].replace('+',' ')))
		print(imdb.get_final_schedule(tv_title[0]))


user_email_unique = get_distinct_email_address()
print (user_email_unique)
for u in user_email_unique:
	print('email: {}\n'.format(u))
	make_content(u)

