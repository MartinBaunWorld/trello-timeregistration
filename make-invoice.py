#!/usr/bin/env python3
import sys
import json
import shutil
import requests


def generate_invoice(total_hours, invoice_number):
    with open('invoice.json', 'r') as f:
        invoice_data = json.load(f)

    invoice_data['items'][0]['quantity'] = total_hours
    invoice_data['number'] = invoice_number
    r = requests.post(
        'https://invoice-generator.com', json=invoice_data, stream=True)
    from_name = invoice_data['from'].replace(' ', '_')

    if r.status_code == 200:
        filename = f'invoice-{from_name}-{invoice_number}.pdf'
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print(f'Invoice {invoice_number} has been successfully generated!')


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print('ERROR: You need to pass two arguments to generate an invoice '
              ' - number of hours and invoice number')
        return False

    try:
        total_hours = round(float(args[0]), 2)
        invoice_number = args[1]
        generate_invoice(total_hours, invoice_number)
    except ValueError:
        print('ERROR: Make sure that first argument you pass is a number.\n'
              'Example: ./make-invoice.py 30.50 INV-2019-03')


if __name__ == '__main__':
    main()
