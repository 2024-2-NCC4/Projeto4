import sqlite3
import pandas as pd
from local_settings import caminho

class DataBaseCon:
    def __init__(self):

        self.caminho = caminho
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.caminho)
            print("Conexão feita com o banco de dados")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None

    def fetch_data(self, query):
        try:
            if self.conn:
                lista = []
                cursor = self.conn.cursor()  #
                cursor.execute(query)
                result = cursor.fetchall()
                lista.append(result)
                cursor.close()
                return lista
            else:
                print("Conexão não está ativa.")
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return None

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada com sucesso.")

if __name__ == "__main__":
    db = DataBaseCon()
    db.conectar()
