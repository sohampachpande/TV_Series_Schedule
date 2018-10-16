import sqlite3 as sql
import re
import email_func
import retrieve_imdb_data as imdb

# Create a database to store queries
database_name = 'user_tv_series.db'

conn = sql.connect(database_name)
cur = conn.cursor()
# Database has 2 columns
# USER_EMAIL contains user email address
# TVSERIES contains 1 TV series entered by user
# LAST_STATUS tells us whether last mail send was successful(1) or not. If not, it contains error details
# For every tv series entered by the user, there would be seperate entry in table with same user email address
# We keep the tuple (user_email, tvseries) unique so that entries don't get duplicated
conn.execute('CREATE TABLE IF NOT EXISTS TVSeries(USER_EMAIL TEXT NOT NULL,TVSERIES TEXT, LAST_STATUS TEXT DEFAULT 1 ,UNIQUE(USER_EMAIL,TVSERIES))')

# get list of all distinct email addresses in database


def get_distinct_email_address():
    # Distinct gives unique USER_EMAIL
    cur.execute('SELECT DISTINCT USER_EMAIL FROM TVSeries')
    all_row = cur.fetchall()
    user_email_unique = []
    for row in all_row:
        user_email_unique.append(row[0])
    return user_email_unique


# retreive user data from database, call required functions to get information about schedule
# form email content text and call function to send email for given user
def make_content(user):
    body_content = ''
    # Find all TV series for given email address
    cur.execute(
        'SELECT TVSERIES FROM TVSeries WHERE USER_EMAIL="{}"'.format(user))
    all_tv = cur.fetchall()
    for tv_title in all_tv:
        # Call function from imdb.py file to get air time of next episode/season or end year
        body_content += 'TVSeries: {}\nStatus: {}\n\n'.format(
            tv_title[0].replace('+', ' '), imdb.get_final_schedule(tv_title[0]))
        # print('TVSeries: {}'.format(tv_title[0].replace('+',' ')))
        # print(imdb.get_final_schedule(tv_title[0]))
    return body_content


# take input
user_dict = {}
n = int(input("Enter number of users: "))
for k in range(n):
    email = input("\nEnter email address:")
    # check for syntax error in email address using regular expression
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print('\nThe email entered is syntatically incorrect')
        email = input("\nEnter email address again: ")
    tv_string = input("\nEnter TV series names seperated by a comma: ")
    # split the tv series titles bu using seperator ',' and store them in a list
    tv_list = tv_string.split(',')
    user_dict.update({email: tv_list})

# store input in database
for user in user_dict:
    for tv_s in user_dict[user]:
        conn.execute(
            'INSERT OR IGNORE INTO TVSeries(USER_EMAIL,TVSERIES) VALUES(?,?)', (user, tv_s))
        conn.commit()

# send mails according to input
m = input("\nEnter comma seperated email-ids and mail would be sent to the email existing in the database\nEnter 'all' (without quotes) if you want to mail to all the user emails:\n")

# get unique email address present in database
user_email_unique = get_distinct_email_address()

if m == 'all':
    # send mail to all email addresses in database
    for u in user_email_unique:
        body_content = make_content(u)
        email_func.send_email(body_content, u)
else:
    # send mail only to email addresses specified
    email_list = m.replace(' ', '').split(',')
    for u in email_list:
        if u in user_email_unique:
            body_content = make_content(u)
            status = email_func.send_email(body_content, u)
            # if mail delivery failed, store error details in database
            if status != 1:
                conn.execute(
                    'UPDATE TVSeries SET LAST_STATUS=? WHERE USER_EMAIL=?', (e, u))
