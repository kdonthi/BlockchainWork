# **Balance Organizer**

## **Table of Contents**

* [Introduction](#introduction)
* [Running the Program](#running-the-program)

## **Introduction**

This program continually updates a database with information about the balances of validators each epoch (created in "createdb.py") and correlates it with ETH 2.0 pricing information (minimum, maximum, and average exchange rates w.r.t. the US dollar) during that epoch. <br> <br>
Information about the API I am calling can be found here: https://api.prylabs.net/#/. <br> <br>
For any questions about the API, the #general section of the Prysm discord channel is a great place to ask for help: https://discord.com/channels/476244492043812875/476588476393848832.

## **Running the Program**

1) Create the database before adding anything to it (if this is your first time).
                                 ```python3 createdb.py```

2) Start the program with the following command:
                                 ```python3 listfromdb.py```

3) In addition, if you want to manually set the amount of per call, you can do so with optional command line arguments:
                                 ```python3 listfromdb.py __amountOfTransactions__ ```

