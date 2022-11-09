import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="knife_shop",
            user="postgres",
            password="root",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def select(self, query):
        self.cur.execute(query)
        data = self.prepare_data(self.cur.fetchall())

        return data

    def insert(self, query):
        self.cur.execute(query)
        self.con.commit()

    def prepare_data(self, data):
        entities = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                entities += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return entities
