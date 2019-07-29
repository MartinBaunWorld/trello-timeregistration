# trello-timeregistration

Helps you track time using Trello comments.
Just add `used 10` to add 10 minutes to your time sheet on a given task.
**To make sure you track all time do not archive or edit comments.**

## How to setup

1. Go to https://trello.com/app-key and get your API key
2. `cp boards-example.json boards.json` and open boards.json and edit the name, api key, token, board id (you can find that when you browse the site)
3. run `./sum_trello_time.py`

## Invoicing

1. `cp invoice-example.json invoice.json` and edit invoice.json file with variables you need
2. run `./sum_trello_time.py -i` or `./sum_trello_time.py --invoice` to generate PDF file based on your trello registered time

