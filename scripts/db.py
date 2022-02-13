import psycopg2

class Database:
	@staticmethod
	def statements(mode):
		if mode == "insert_post":
			return "INSERT INTO posts VALUES(%s, %s, %s, %s, %s) RETURNING id;"
		if mode == "insert_last_id":
			return "INSERT INTO last_id VALUES(%s) RETURNING id;"
		if mode == "delete_last_id":
			return "DELETE FROM last_id"
	def __init__(self, username, password):
		self.__conn = psycopg2.connect("dbname=parler user=%s password=%s" % (username, password))
		
	
	def insert(self, statement, data):
		cur = self.__conn.cursor()
		cur.execute(statement, data)
		self.__conn.commit()
	def get(self, table):
		cur = self.__conn.cursor()
		cur.execute("SELECT * FROM %s" % table)
		return cur.fetchone()
	def close(self):
		self.__conn.close()