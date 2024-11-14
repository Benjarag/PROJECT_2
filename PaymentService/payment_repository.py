import sqlite3
# búa til .json gagngrunn


class PaymentRepository:

    def __init__(self):
        self.connection = sqlite3.connect("payment_data/payment.db")
        self.create_database()

    def save_payment_results(self, payment_result: bool, orderid: int):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO payment_table (orderId, payment_result) VALUES (?, ?)", (orderid, payment_result,))
        self.connection.commit()

    def create_database(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment_table (id INTEGER PRIMARY KEY, orderId INTEGER, payment_result INTEGER )""")
        self.connection.commit()
