import sqlite3
from flask import Flask, request

app = Flask(__name__)


def pdb_update(db_name='Phones.db', sql=''):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    result_data = cur.fetchall()
    con.close()
    return result_data


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/phones/create")
def phone_create():
    contact_name = request.args['contact_name']
    phone_value = request.args['phone_value']
    if phone_value.isdigit() and contact_name != '':
        sql = f'''
        INSERT INTO Phones(contactName, phoneValue)
        VALUES ('{contact_name}', '{int(phone_value)}');
        '''
        pdb_update('Phones.db', sql)
        return '<h1>Phone created!!</h1>'
    else:
        return '<h1>Incorrect data!!!</h1>'


@app.route("/phones/update")
def phone_update():
    contact_name = request.args['contact_name']
    phone_value = request.args['phone_value']
    phone_id = request.args['phone_id']
    if phone_value.isdigit() and contact_name != '':
        sql = f'''
            UPDATE Phones
            SET contactName = '{contact_name}', phoneValue = '{phone_value}'
            WHERE phoneID = '{phone_id}'
            '''
        pdb_update('Phones.db', sql)
        return '<h1>Phone changed!!</h1>'
    else:
        return '<h1>Incorrect data!!!</h1>'


@app.route("/phones/delete")
def phone_delete():
    delete_cursor = request.args['cursor']
    delete_data = request.args['data']
    cursor_mapping = {
        'phone_value': 'phoneValue',
        'phone_id': 'phoneID',
        'contact_name': 'contactName'
    }
    if delete_cursor in cursor_mapping:
        delete_cursor = cursor_mapping[delete_cursor]
    else:
        return '<h1>Incorrect data!!!</h1>'
    sql = f'''
        DELETE FROM Phones 
        WHERE {delete_cursor} = '{delete_data}'; 
    '''
    pdb_update('Phones.db', sql)
    return '<h1>Phone deleted!!</h1>'


@app.route("/phones/read")
def phone_read():
    sql = 'SELECT * FROM Phones;'
    return pdb_update('Phones.db', sql)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
