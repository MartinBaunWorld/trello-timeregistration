#!/usr/bin/env python3
import requests
import json


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


if __name__ == '__main__':
    with open('boards.json', 'r') as f:
        boards = json.load(f)

    for board in boards:
        total_used = count_user_of_board(
            board['id'],
            board['trello_key'],
            board['trello_token'],
            board['date'],
            board['username'],
        )
        print(f'{board["username"]} on board {board["name"]} on month {board["date"]} {round(total_used/60, 2)}') # noqa
