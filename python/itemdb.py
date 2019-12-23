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
		try:
			self.connect()
			self.cursor.execute(sql)
			self.con.commit()

		except Exception as e:
			self.cursor.rollback()
			raise e
		finally:
			self.cursor.close()
			self.con.close()

	"""
	cartテーブル内にある指定したcart_idが保有する商品情報をすべて取得する
	"""
	def get_items_info(self, cart_id):
		jans_sql = "SELECT jan FROM cart WHERE cart_id = {}".format(cart_id)

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