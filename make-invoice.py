#!/usr/bin/env python3
import sys
import json
import shutil
import requests


def generate_invoice(filename):
    with open(filename, 'r') as f:
        invoice_data = json.load(f)

    r = requests.post(
        'https://invoice-generator.com', json=invoice_data, stream=True)
    invoice_number = invoice_data['number']

    if r.status_code == 200:
        with open(filename.split('.json')[0] + '.pdf', 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print(f'Invoice {invoice_number} has been successfully generated!')


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print('ERROR: You need to pass one argument to generate an invoice '
              ' - invoice json')
        return False

    try:
        filename = args[0]
        generate_invoice(filename)
    except ValueError:
        from traceback import format_exc
        print(format_exc())
        print('ERROR: Make sure that first argument you pass is the invoice data.\n'
              'Example: ./make-invoice.py invoice-1904.json')


if __name__ == '__main__':
    main()
