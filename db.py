import sqlite3

DATABASE = 'database-cnj.db'
dbName = DATABASE
class Connect(object):

	def __init__(self):
		print('DB init...')
		
		try:
			print('try connect data base')
			self.conn = sqlite3.connect(dbName)
			self.cursor = self.conn.cursor()
            
			print("Database:", dbName)
            
			self.cursor.execute('SELECT SQLITE_VERSION()')
			self.data = self.cursor.fetchone()
            
			print("SQLite version: %s" % self.data)
			
			self.schema()
			#return True
		except sqlite3.Error as errors:
			print(f"Errors: {errors}")
			return False
    
	def schema(self):
		if self.conn:
			self.conn.execute("""
				CREATE TABLE IF NOT EXISTS peticao (
					id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
					num_processo TEXT,
					arquivo TEXT,
					rota TEXT,
                    texto_peticao TEXT
				);
				"""
			)
	
	def insertPeticao(self, dados):
		if self.conn:
			self.cursor.execute('INSERT INTO peticao (num_processo, arquivo, rota, texto_peticao) VALUES (?, ?, ?, ?)', (dados[0], dados[1], dados[2], dados[3]))
			self.conn.commit()
			print('Peticao: %s inserido...' %self.cursor.lastrowid)

			
	def closeDB(self):
		if self.conn:
			self.conn.close()
			print("Conexão fechada.")
