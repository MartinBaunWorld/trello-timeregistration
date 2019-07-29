#!/usr/bin/env python3
import sys
import json
import shutil
import requests


def get_board(board_id, key, token):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"

    querystring = {
        "cards": "open",
        "card_fields": ["id"],
        "fields": "cards"
    }

    querystring.update({
        "key": key,
        "token": token,
    })

    response = requests.request("get", url, params=querystring)
    return response.json()


def get_card_data(card_id, key, token):
    url = f"https://api.trello.com/1/cards/{card_id}/actions"

    querystring = {
        "actions": ["commentCard"],
    }

    querystring.update({
        "key": key,
        "token": token,
    })

    response = requests.request("get", url, params=querystring)
    return response.json()


def filter_type(username, comments):
    return [
        comment for comment in comments
        if comment['type'] == 'commentCard'
    ]


def filter_username(username, comments):
    return [
        comment for comment in comments
        if comment['memberCreator']['username'] == username
    ]


def filter_date(date, comments):
    return [
        comment for comment in comments
        if comment['date'].startswith(date)
    ]


def filter_used(comments):
    return [
        comment for comment in comments
        if comment['data']['text'].lower().strip().startswith('used')
    ]


def count_user_of_board(
        board_id, trello_key, trello_token, date, username):
    total_used = 0
    lists = get_board(board_id, trello_key, trello_token)
    for list in lists:
        cards = list['cards']
        for card in cards:
            card_id = card['id']
            comments = get_card_data(card_id, trello_key, trello_token)
            comments = filter_type(date, comments)
            comments = filter_username(username, comments)
            comments = filter_date(date, comments)
            comments = filter_used(comments)
            for c in comments:
                total_used += \
                    int(c['data']['text'].lower().strip().strip('used '))
    return total_used


def generate_invoice(total_hours):
    with open('invoice.json', 'r') as f:
        invoice_data = json.load(f)
        invoice_data['items'][0]['quantity'] = total_hours
        r = requests.post('https://invoice-generator.com', json=invoice_data, stream=True)
        if r.status_code == 200:
            filename = f'invoice-{invoice_data["number"]}.pdf'
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                print(f'{filename} has been sucessfully generated')


if __name__ == '__main__':
    with open('boards.json', 'r') as f:
        boards = json.load(f)

    total_hours = 0
    for board in boards:
        total_used = count_user_of_board(
            board['id'],
            board['trello_key'],
            board['trello_token'],
            board['date'],
            board['username'],
        )
        total_hours += total_used / 60
        print(f'{board["username"]} on board {board["name"]} on month {board["date"]} {round(total_used / 60, 2)}') # noqa
    total_hours = round(total_hours, 2)
    print(f'Total hours: {total_hours}')

    for arg in sys.argv[1:]:
        if arg == '-i' or arg == '--invoice':
            generate_invoice(total_hours)
