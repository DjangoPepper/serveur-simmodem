import mysql.connector

MYSQL_CONNECT_PARAMS = {
    'user': 'pi@localhost',
    'password': 'm4opvskt',
    'host': '127.0.0.1',
    'database': 'STE',
    'raise_on_warnings': True
}

class MySqlDATABASE(object):
	@staticmethod
	def get_appelant(userid) -> str:
		request = "SELECT code FROM SERVEUR WHERE id={}".format(userid)
		db = mysql.connector.connect(**MYSQL_CONNECT_PARAMS)
		c = db.cursor()
		try:
			# with db.cursor() as c:
			c.execute(request)
			APPELANT_SRV = c.fetchone()
			if APPELANT_SRV is None:
				print("erreur SQL")
				return "pas d'appelant", None

			APPELANT_SRV = APPELANT_SRV[0]
			print("{} peut appeler le serveur".format(APPELANT_SRV))
			LIST_OF_DIGIT = [int(x) for x in str(APPELANT_SRV)]
			DTMF_MSG = '1,"{}","100"'.format(','.join(str(x) for x in LIST_OF_DIGIT))
			return DTMF_MSG, APPELANT_SRV
		finally:
			c.close()
			db.close()
