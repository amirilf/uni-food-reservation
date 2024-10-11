import requests
from bs4 import BeautifulSoup
from core.account.auth import get_page_or_exception
from utility.config import TRANSACTIONS_URL


def get_transactions(session: requests.Session) -> list | Exception:
    """
    Extract user last transactions
    
    Ideal return list includes:
        - details
            - transaction type
            - food
            - meal time
            - day name
            - date
            - quantity (always 1)
            - unit price
        - index
        - title
        - date
        - time
        - amount
        - remaining credit
    
    But there could be transactions like "افزایش اعتبار" which they don't have details
    so the first item is just an empty list in those cases.
    """

    content = get_page_or_exception(session, TRANSACTIONS_URL).content
    
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'id': 'cphMain_grdContent'})

    if not table:
        raise Exception("No transactions found.")

    rows = table.find_all('tr', recursive=False)
    
    if not rows:
        raise Exception("No transactions found.")

    transactions = []

    for row in rows:
        columns = row.find_all('td', recursive=False)

        transaction_detail = []
        transaction_index = columns[1].text.strip()
        transaction_title = columns[2].text.strip()
        transaction_date = columns[3].text.strip()
        transaction_time = columns[4].text.strip()
        transaction_amount = columns[5].text.strip()
        remaining_credit = columns[6].text.strip()
        
        details_table = columns[0].find("table")
        if details_table:            
            table_rows = details_table.find_all('tr', recursive=False)[1:]

            for detail_row in table_rows:
                
                detail_columns = detail_row.find_all('td')
                transaction_type = detail_columns[0].text.strip()
                food_item = detail_columns[1].text.strip()
                meal_time = detail_columns[2].text.strip()
                day_of_week = detail_columns[3].text.strip()
                date = detail_columns[4].text.strip()
                quantity = detail_columns[5].text.strip()
                price = detail_columns[6].text.strip()
                
                transaction_detail.append([transaction_type, food_item, meal_time, day_of_week, date, quantity, price])

        transactions.append([transaction_detail, transaction_index, transaction_title, transaction_date, transaction_time, transaction_amount, remaining_credit])

    return transactions
