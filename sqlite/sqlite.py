import sqlite3
import time
import logging
from data import SUB_TRIAL_TIME, DB_PATH

logger = logging.getLogger("bot.sqlite.sqlite")

def create_table(db_path: str=DB_PATH) -> None:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		cur.execute("""CREATE TABLE users (user_id INT NOT NULL PRIMARY KEY,
										   subscribe INT NOT NULL,
										   registration INT NOT NULL,
										   samples INT NOT NULL,
										   username TEXT,
										   first_name TEXT,
										   last_name TEXT)
					""")

		con.commit()
		cur.close()
	except Exception as ex:
		logger.warning(ex)
	finally:
		if con:
			con.close()

def user_already_exists(user_id: int, db_path: str=DB_PATH) -> bool:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		request = cur.execute(f"""SELECT * FROM users WHERE user_id={user_id}""").fetchone()

		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		if request:
			return True

def get_user_subtime(user_id: int, db_path: str=DB_PATH) -> int:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		query = f"""SELECT subscribe FROM users WHERE user_id={user_id}"""

		sub_time = cur.execute(query).fetchone()[0]
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		return sub_time

def get_user_samples(user_id: int, db_path: str=DB_PATH) -> int:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		query = f"""SELECT samples FROM users WHERE user_id={user_id}"""

		samples = cur.execute(query).fetchone()[0]
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		return samples

def get_user_registration(user_id: int, db_path: str=DB_PATH) -> int:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		query = f"""SELECT registration FROM users WHERE user_id={user_id}"""

		registration = cur.execute(query).fetchone()[0]
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		if registration:
			return registration

def get_users_with_sub(db_path: str=DB_PATH) -> list:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		time_now = int(time.time())

		query = f"""SELECT user_id FROM users WHERE subscribe=0 OR subscribe>{time_now}"""
		users = cur.execute(query).fetchall()

		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		return [user[0] for user in users]

def get_users(db_path: str=DB_PATH) -> list:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		time_now = int(time.time())

		query = f"""SELECT user_id FROM users"""
		users = cur.execute(query).fetchall()

		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		return [user[0] for user in users]	

def user_is_sub(user_id: int, db_path: str=DB_PATH) -> bool:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		time_now = int(time.time())

		query = f"""SELECT subscribe FROM users WHERE user_id={user_id}"""
		sub = cur.execute(query).fetchone()

		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()
		if sub > time_now or sub == 0:
			return True
	
def get_table(db_path: str=DB_PATH) -> list:
	"""Для админ-панели"""
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		query = """SELECT * FROM users"""
		table = cur.execute(query).fetchall()

		cur.close()
	except Exception as ex:
		logger.warning(ex)
	finally:
		if con:
			con.close()
		return table

def register_user(user_id: int, username: str, first_name: str, last_name: str, db_path: str=DB_PATH) -> None:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		time_now = int(time.time())

		trial_time   = time_now + SUB_TRIAL_TIME
		registration = time_now
 
		query = f"""INSERT INTO users (user_id, subscribe, registration, samples, 
									   username, first_name, last_name)
					VALUES            ({user_id}, {trial_time}, {registration}, 0, '{username}', 
									  '{first_name}', '{last_name}')
				 """
		cur.execute(query)

		con.commit()
		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()

def add_user_subtime(user_id: int, extra_time: int, db_path: str=DB_PATH) -> None:
	"""В extra_time передаём кол-во секунд которое хотим добавить"""
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		# Навсегда
		if extra_time == 0:
			query = f"""UPDATE users SET subscribe=0 WHERE user_id={user_id}"""
		else:
			sub_time = get_user_subtime(user_id)
			time_now = int(time.time())

			if sub_time < time_now:
				new_sub_time = time_now + extra_time
			elif sub_time > time_now or sub_time == time_now:
				new_sub_time = sub_time + extra_time

			query = f"""UPDATE users SET subscribe={new_sub_time} WHERE user_id={user_id}"""
		cur.execute(query)

		con.commit()
		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()

def increment_user_samples(user_id: int, db_path: str=DB_PATH) -> None:
	try:
		con = sqlite3.connect(db_path)
		cur = con.cursor()

		samples = cur.execute(f"""SELECT samples FROM users WHERE user_id={user_id}""").fetchone()[0]
		cur.execute(f"""UPDATE users SET samples={samples+1} WHERE user_id={user_id}""")

		con.commit()
		cur.close()
	except Exception as ex:
		logger.critical(ex)
	finally:
		if con:
			con.close()

