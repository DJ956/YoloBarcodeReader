import MySQLdb

class itemdb:
	def __init__(self, host, user, pw, db):
		self.host = host
		self.user = user
		self.pw = pw
		self.db = db

	def connect(self):
		self.con = MySQLdb.connect(
			host = self.host,
			user = self.user,
			passwd = self.pw,
			db = self.db,
			charset= "utf8")

		self.cursor = self.con.cursor()

	"""
	itemテーブルにそのJANコードの商品が存在するか確かめる
	"""
	def exists(self,  code):
		sql = "SELECT * FROM item WHERE jan IN ({})".format(code)
		print("sql:{}".format(sql))
		try:
			self.connect()
			self.cursor.execute(sql)
			result = self.cursor.fetchall()
			
			return (len(result) != 0)

		except Exception as e:
			self.con.rollback()
			raise e
		finally:
			self.cursor.close()
			self.con.close()

	"""
	指定されたカートidに商品janコードを追加する
	"""
	def insert(self, code, cart_id):
		if not self.exists(code):
			return False

		sql = "INSERT INTO cart(jan, cart_id) VALUES({}, {})".format(code, cart_id)
		print("sql:{}".format(sql))
		try:
			self.connect()
			self.cursor.execute(sql)
			self.con.commit()
		except Exception as e:
			self.con.rollback()
			raise e
		finally:
			self.cursor.close()
			self.con.close()

	"""
	cartテーブルから指定されたカートidかつjanを削除する
	"""
	def delete(self, code, cart_id):
		sql = "DELETE FROM cart WHERE jan = {} AND cart_id = {}".format(code, cart_id)
		print("sql:{}".format(sql))
		try:
			self.connect()
			self.cursor.execute(sql)
			self.con.commit()

		except Exception as e:
			self.cursor.rollback()
			raise e
		finally:
			self.cursor.rollback()
			self.con.close()

	"""
	cartテーブル内にある指定したcart_idが保有する商品情報をすべて取得する
	"""
	def get_items_info(self, cart_id):
		jans_sql = "SELECT jan FROM cart WHERE cart_id = {}".format(cart_id)

		print("sql:{}".format(jans_sql))
		try:
			self.connect()
			self.cursor.execute(jans_sql)
			jans = self.cursor.fetchall()			
			result = []
			
			for jan in jans:	
				sql = "SELECT title, price FROM item WHERE jan = {}".format(jan[0])
				self.cursor.execute(sql)
				item = self.cursor.fetchall()
				result.append(item)
			
			return result
		except Exception as e:
			self.cursor.rollback()
			raise e
		finally:
			self.cursor.close()
			self.con.close()

def main():
	db = itemdb(host = "localhost", user="rabit", pw = "pass", db="rapid_cart")
	db.connect()

	cart_id = 1

	item1 = 4902011731118 
	item2 = 4903333066254
	item3 = 9784844333937
	item3_2 = 9784844333937

	"""
	db.insert(item1, cart_id)
	db.insert(item2, cart_id)
	db.insert(item3, cart_id)
	db.insert(item3_2, cart_id)
	"""

	result = db.get_items_info(cart_id)
	for item in result:
		print(item)
		print("-"*100)

if __name__ == "__main__":
	main()
