# TV Series Schedule Bot
Initially, the program asks for gmail user name and password details for the center. Note: The password is not encrypted.
This program takes user's Email address and TV series names as input.
It emails the details of streaming date of next episode/season or the year completion of the TV series in question. If information is not found due to spelling errors or incorrect titles then 'Not Found' is mailed

The program includes spell correct to deal with minor spelling mistakes by the user.

The required information is obtained from IMDb website.

Run app.py to open the script

The functions of the files are:
app.py                : Main script. Takes and stores inputs. Makes appropriate calls to functions to facilitate desired task
retrieve_imdb_data.py : Scraps IMDb and returns required dates
spell_correct.py      : Returns correct spelling of tv series. It can deal with upto 2 character mistakes in the spelling entered by the                          user. Mistakes include deletion, substitution, insertion and transposition.
email_func.py         : Sends email to users using gmail SMTP.
