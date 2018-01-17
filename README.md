# lunch-lottery

This is a simple python script for creating random lunch lottery pairs (or triples if an odd amount of participants). This script also persists already drawn picks and tries to avoid those pairs in the next shuffle. Also, the participants can be changed each time based on who wants to participate.

# Usage

Call with `python lottery.py 'Adam Jon Mary Jane Max Zulu Roger'`

This will print the resulting pairs into the console, eg.

```
This week:
Jon & Zulu & Max
Roger & Jane
Mary & Adam
Total of 3 combinations with a duplicate score of 0
```

# Resetting old pairs
You can reset all the previous pairs by adding `-r` when starting the script.

eg. `python lottery.py 'Adam Jon Mary Jane Max Zulu Roger'`

Take care, as this *ultimately* deletes all the previous pairs from `data.json`. You might want to back up `data.json`.
