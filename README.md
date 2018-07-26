# Introduction

FisherDetector is a simple python program that uses OpenDota API to detect players who are using a low-rank account to gain advantages in matching.


# How to use it

Download the python file, create file "users.txt" in the same directory

In "users.txt", enlist all the userIDs you want to investigate, example "users.txt":

>136516407  
>60518558  
>209267092  
>887160947  


And in the python file, if you have an OpenDota APIKEY, fill it in. If not, that's okay, just the query numers are limited (see https://www.opendota.com/api-keys)

Run it (**in python3**), if the player is denoted as "FISHING", you gotta beware of this game, it could be a trap.

If you don't know if you have python, or how to run a python file, here's the tutorials:


>[Installation of python](https://www.python.org/getit/)

>[Run python file](https://www.pythoncentral.io/execute-python-script-file-shell/)

Or you can ask me if you know me in real life XD

# How to get a user's ID

In Dota client, open up the player's profile, look for "Friend ID", this is it.

You can also open up the player's Steam profile page, copy the url, like "https://steamcommunity.com/id/runningfastli/", paste it into [steamIDFinder](https://steamidfinder.com/), look for steamID3, which is like "[U:1:136516407]", the number "136516407" will be the user id you need.

# How does it work

For now the strategy is simple, if a player recently often wins overwhelmingly, the player will be noted as "FISHING". 
