# Bank Management System
# This program stores and manages customer records.

import argparse
import os
import sqlite3
import sys

db_kind = ''
mycon = None
mycursor = None

table_sql = """create table if not exists customer (
    customer_id int primary key,
    name varchar(30),
    YOB varchar(5),
    IFSC varchar(15),
    phone_number int
)"""

users = {'Manager': 'Manager1', 'Employee': 'Employee1', 'customer': 'admin'}


def load_env_file(path):
    if not os.path.exists(path):
        return

    f = open(path, 'r')
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key not in os.environ:
            os.environ[key] = value
    f.close()


def connect_mysql():
    import mysql.connector as ms

    db_name = os.environ.get('DB_NAME', 'bank')
    con = ms.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', '3306')),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', '')
    )

    cur = con.cursor()
    cur.execute('create database if not exists ' + db_name)
    cur.execute('use ' + db_name)
    cur.close()

    return con


def start_database(wanted, sqlite_file):
    global db_kind, mycon, mycursor

    if wanted in ('mysql', 'auto'):
        try:
            mycon = connect_mysql()
            db_kind = 'mysql'
        except ImportError:
            if wanted == 'mysql':
                print('mysql connector is not installed')
                print('run: pip install -r requirements.txt')
                sys.exit(1)
            print('[info] mysql connector not found, using sqlite')
        except Exception as error:
            if wanted == 'mysql':
                print('could not connect to mysql:', error)
                sys.exit(1)
            print('[info] mysql is not available, using sqlite')

    if db_kind == '':
        mycon = sqlite3.connect(sqlite_file)
        db_kind = 'sqlite'

    if db_kind == 'mysql':
        mycursor = mycon.cursor(buffered=True)
        print('database in use : mysql ->', os.environ.get('DB_NAME', 'bank'))
    else:
        mycursor = mycon.cursor()
        print('database in use : sqlite ->', sqlite_file)

    mycursor.execute(table_sql)
    mycon.commit()


def run(query, values=()):
    if db_kind == 'mysql':
        query = query.replace('?', '%s')
    mycursor.execute(query, values)
    return mycursor


def close_database():
    if mycon is not None:
        try:
            mycon.close()
        except Exception:
            pass


def ask(message):
    try:
        return input(message)
    except EOFError:
        print()
        close_database()
        sys.exit(0)


def ask_number(message):
    while True:
        value = ask(message).strip()
        if value.isdigit():
            return int(value)
        print('enter numbers only')


def ask_text(message):
    while True:
        value = ask(message).strip()
        if value:
            return value
        print('this cannot be empty')


def customer_exists(cid):
    run('select customer_id from customer where customer_id=?', (cid,))
    return mycursor.fetchone() is not None


def insert():
    print()
    print("------------ WELCOME TO INSERT CUSTOMER RECORD WINDOW ----------")
    print()

    ans = 'yep'
    while ans == 'yep':
        cid = ask_number('enter customer account number : ')

        if customer_exists(cid):
            print('##this account number is already used, record not saved##')
        else:
            name = ask_text('enter name of the customer : ')
            yob = ask_text('enter year of birth of the customer : ')
            ifsc = ask_text('enter branch IFSC code : ')
            phone = ask_number('enter last 4 digits of mobile phone number : ')

            run(
                'insert into customer '
                '(customer_id,name,YOB,IFSC,phone_number) '
                'values (?,?,?,?,?)',
                (cid, name, yob, ifsc, phone)
            )
            mycon.commit()
            print('##record saved##')

        ans = ask('add more(yep=Yes or nope=No) : ').strip().lower()


def show_heading():
    print('%-14s %-22s %-6s %-14s %-8s' %
          ('customer_id', 'name', 'YOB', 'IFSC', 'phone'))
    print('-' * 68)


def show_row(row):
    print('%-14s %-22s %-6s %-14s %-8s' %
          (row[0], row[1], row[2], row[3], row[4]))


def search():
    print()
    print("------------ WELCOME TO SEARCH CUSTOMER RECORD WINDOW ----------")
    print()

    cid = ask_number('enter customer_id : ')
    run('select * from customer where customer_id=?', (cid,))
    row = mycursor.fetchone()

    if row is None:
        print('no such customer_id')
    else:
        show_heading()
        show_row(row)


def display():
    print()
    print("------------ WELCOME TO DISPLAY CUSTOMER RECORD WINDOW ----------")
    print()

    run('select * from customer order by customer_id')
    rows = mycursor.fetchall()

    print('total records found are : ', len(rows))

    if not rows:
        return

    show_heading()
    for row in rows:
        show_row(row)


def update():
    print()
    print("------------ WELCOME TO UPDATE CUSTOMER RECORD WINDOW ----------")
    print()

    cid = ask_number('enter customer_id to search for : ')
    run('select * from customer where customer_id=?', (cid,))
    row = mycursor.fetchone()

    if row is None:
        print('record not found')
        return

    print('##record found-details are##')
    show_heading()
    show_row(row)

    print('1.update name')
    print('2.update YOB')
    print('3.update IFSC')
    print('4.update phone')

    choice = ask_number('enter your choice : ')

    if choice == 1:
        value = ask_text('enter new name : ')
        run('update customer set name=? where customer_id=?', (value, cid))

    elif choice == 2:
        value = ask_text('enter new YOB : ')
        run('update customer set YOB=? where customer_id=?', (value, cid))

    elif choice == 3:
        value = ask_text('enter new IFSC : ')
        run('update customer set IFSC=? where customer_id=?', (value, cid))

    elif choice == 4:
        value = ask_number('enter new phone number : ')
        run('update customer set phone_number=? where customer_id=?',
            (value, cid))

    else:
        print('wrong choice, nothing was changed')
        return

    mycon.commit()
    print('##record updated##')


def delete():
    print()
    print("------------ WELCOME TO DELETE CUSTOMER RECORD WINDOW ----------")
    print()

    more = 'yes'
    while more == 'yes':
        cid = ask_number('enter customer id : ')

        if customer_exists(cid):
            run('delete from customer where customer_id=?', (cid,))
            mycon.commit()
            print('** record deleted**')
        else:
            print('no such customer_id')

        more = ask('do you want to delete more record(yes/no) ? ').strip().lower()


def choose():
    while True:
        print()
        print('1.insert your record')
        print('2.search your record')
        print('3.display your record')
        print('4.update your record')
        print('5.delete your record')
        print('6.Exit')

        choice = ask_number('enter your choice number: ')

        if choice == 1:
            insert()
        elif choice == 2:
            search()
        elif choice == 3:
            display()
        elif choice == 4:
            update()
        elif choice == 5:
            delete()
        elif choice == 6:
            print('Goodbye!')
            break
        else:
            print('TRY AGAIN')


def login():
    tries = 3

    while tries > 0:
        username = ask('enter your username : ')
        password = ask('enter your password : ')

        if username in users and users[username] == password:
            print('LOGIN SUCCESSFUL')
            return True

        tries -= 1
        if tries:
            print('TRY AGAIN,', tries, 'attempt(s) left')

    print('too many wrong attempts, closing the program')
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Bank Management System (command line)'
    )
    parser.add_argument(
        '--db',
        choices=['auto', 'mysql', 'sqlite'],
        default='auto',
        help='database to use'
    )
    parser.add_argument(
        '--sqlite-file',
        default='bank.db',
        help='file used for sqlite'
    )
    parser.add_argument(
        '--env-file',
        default='.env',
        help='file containing database settings'
    )

    args = parser.parse_args()

    load_env_file(args.env_file)
    start_database(args.db, args.sqlite_file)

    print()
    print('### WELCOME TO BANK MANAGEMENT ###')
    print()

    if login():
        choose()

    close_database()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('stopped by the user')
        close_database()
