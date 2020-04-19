# The Battle at Thalrock

Install termcolor to get pretty colors when running in powershell or a linux terminal.

`pip install termcolor`

To run a randomized pre-programmed battle (the battle that occured at Thalrock)

`python .\battle.py`

Give the program a "seed string" and it will run in a deterministic fashion (the same outcome every time).

`python .\battle.py someseeed`

Give a numeric value after the seed to set the base delay between messages (in seconds). The default is 0.25.

`python .\battle.py someseed 0.1`

--

To run your own battles:

a. import `field.py` and initialize a `field.Battlefield`. Then run `battlefield.skirmish(n)` where n is the unit initiative place.

b. import `battle.py`, initialize a `field.Battlefield`, then run `battle.Battle(battlefield)`




