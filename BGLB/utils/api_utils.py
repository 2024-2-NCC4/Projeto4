from flask import Flask, jsonify
from connection import DataBaseCon

app = Flask(__name__)


class APIUtils:
    def __init__(self):
        self.db_conn = DataBaseCon()

    def get_pcd_info(self):
        querySim = "SELECT COUNT (*) FROM DADOS_PLANILHA_2022 dp WHERE dsc_pcd LIKE 'Sim'"
        queryNao = "SELECT COUNT (*) FROM DADOS_PLANILHA_2022 dp WHERE dsc_pcd LIKE 'Não'"

        self.db_conn.conectar()
        pcdSimresult = self.db_conn.fetch_data(querySim)
        pcdNaoresult = self.db_conn.fetch_data(queryNao)
        self.db_conn.fechar_conexao()

        pcdSim = pcdSimresult[0][0] if pcdSimresult else 0
        pcdNao = pcdNaoresult[0][0] if pcdNaoresult else 0

        return{
            'Sim' : pcdSim,
            'Nao' : pcdNao
        }


    def get_faixa_etarias(self):
        # Consultas para as faixas etárias
        query_18_25 = """
        SELECT
        SUM(CASE WHEN dsc_idade BETWEEN 18 AND 25 THEN 1 ELSE 0 END) AS faixa_18_25
        FROM DADOS_PLANILHA_2022
        """
        query_26_35 = """
        SELECT
        SUM(CASE WHEN dsc_idade BETWEEN 26 AND 35 THEN 1 ELSE 0 END) AS faixa_26_35
        FROM DADOS_PLANILHA_2022
        """
        query_36_50 = """
        SELECT
        SUM(CASE WHEN dsc_idade BETWEEN 36 AND 50 THEN 1 ELSE 0 END) AS faixa_36_50
        FROM DADOS_PLANILHA_2022
        """
        query_50_plus = """
        SELECT
        SUM(CASE WHEN dsc_idade > 50 THEN 1 ELSE 0 END) AS faixa_50_plus
        FROM DADOS_PLANILHA_2022
        """

        self.db_conn.conectar()
        faixa_result_18_25 = self.db_conn.fetch_data(query_18_25)
        faixa_result_26_35 = self.db_conn.fetch_data(query_26_35)
        faixa_result_36_50 = self.db_conn.fetch_data(query_36_50)
        faixa_result_50_plus = self.db_conn.fetch_data(query_50_plus)
        self.db_conn.fechar_conexao()

        faixa_18_25 = faixa_result_18_25[0][0] if faixa_result_18_25 else 0
        faixa_26_35 = faixa_result_26_35[0][0] if faixa_result_26_35 else 0
        faixa_36_50 = faixa_result_36_50[0][0] if faixa_result_36_50 else 0
        faixa_50_plus = faixa_result_50_plus[0][0] if faixa_result_50_plus else 0

        return {
            'faixa_18_25': faixa_18_25,
            'faixa_26_35': faixa_26_35,
            'faixa_36_50': faixa_36_50,
            'faixa_50_plus': faixa_50_plus
        }
    def get_etnia(self):
        queryBranca = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022 WHERE dsc_cor_raca_etnia LIKE 'Branca'"
        queryParda = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022  WHERE dsc_cor_raca_etnia LIKE 'Parda'"
        queryPreta = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022  WHERE dsc_cor_raca_etnia LIKE 'Preta'"
        queryIndio = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022  WHERE dsc_cor_raca_etnia LIKE 'Indígena'"
        queryAmarela = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022  WHERE dsc_cor_raca_etnia LIKE 'Amarela'"
        queryOutro = "SELECT COUNT(*) FROM DADOS_PLANILHA_2022  WHERE dsc_cor_raca_etnia LIKE 'Outra'"

        self.db_conn.conectar()
        Branca_result = self.db_conn.fetch_data(queryBranca)
        Parda_result = self.db_conn.fetch_data(queryParda)
        Preta_result = self.db_conn.fetch_data(queryPreta)
        Indio_result = self.db_conn.fetch_data(queryIndio)
        Amarela_result = self.db_conn.fetch_data(queryAmarela)
        Outro_result = self.db_conn.fetch_data(queryOutro)
        self.db_conn.fechar_conexao()

        branca = Branca_result[0][0] if Branca_result else 0
        parda = Parda_result[0][0] if Parda_result else 0
        preta = Preta_result[0][0] if Preta_result else 0
        indio = Indio_result[0][0] if Indio_result else 0
        amarela = Amarela_result[0][0] if Amarela_result else 0
        outro = Outro_result[0][0] if Outro_result else 0

        return{
            'Branca' : branca,
            'Parda': parda,
            'Preta': preta,
            'Indio': indio,
            'Amarela': amarela,
            'Outro': outro
        }

    def get_contagem_genero(self):
        # Consultas para contagem de gênero
        query_masculino = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_genero = 'Masculino'
        """
        query_feminino = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_genero = 'Feminino'
        """
        query_outros = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_genero NOT IN ('Masculino', 'Feminino')
        """

        self.db_conn.conectar()
        masculino_result = self.db_conn.fetch_data(query_masculino)
        feminino_result = self.db_conn.fetch_data(query_feminino)
        outros_result = self.db_conn.fetch_data(query_outros)
        self.db_conn.fechar_conexao()

        masculino = masculino_result[0][0] if masculino_result else 0
        feminino = feminino_result[0][0] if feminino_result else 0
        outros = outros_result[0][0] if outros_result else 0

        return {
            'Masculino': masculino,
            'Feminino': feminino,
            'Prefiro não dizer / Outros': outros
        }

    def get_faixa_salarial(self):
        # Consultas para as faixas salariais
        query_1001_2000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 1.001/mês a R$ 2.000/mês'
        """

        query_2001_3000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 2.001/mês a R$ 3.000/mês'
        """

        query_3001_4000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 3.001/mês a R$ 4.000/mês'
        """

        query_4001_6000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 4.001/mês a R$ 6.000/mês'
        """

        query_6001_8000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 6.001/mês a R$ 8.000/mês'
        """

        query_8001_12000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 8.001/mês a R$ 12.000/mês'
        """

        query_12001_16000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 12.001/mês a R$ 16.000/mês'
        """

        query_16001_20000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 16.001/mês a R$ 20.000/mês'
        """

        query_20001_25000 = """
        SELECT COUNT(*) 
        FROM DADOS_PLANILHA_2022
        WHERE dsc_area_formacao = 'de R$ 20.001/mês a R$ 25.000/mês'
        """

        # Conectando ao banco de dados
        self.db_conn.conectar()

        # Executando as consultas para cada faixa salarial
        faixa_1001_2000 = self.db_conn.fetch_data(query_1001_2000)[0][0] if self.db_conn.fetch_data(
            query_1001_2000) else 0
        faixa_2001_3000 = self.db_conn.fetch_data(query_2001_3000)[0][0] if self.db_conn.fetch_data(
            query_2001_3000) else 0
        faixa_3001_4000 = self.db_conn.fetch_data(query_3001_4000)[0][0] if self.db_conn.fetch_data(
            query_3001_4000) else 0
        faixa_4001_6000 = self.db_conn.fetch_data(query_4001_6000)[0][0] if self.db_conn.fetch_data(
            query_4001_6000) else 0
        faixa_6001_8000 = self.db_conn.fetch_data(query_6001_8000)[0][0] if self.db_conn.fetch_data(
            query_6001_8000) else 0
        faixa_8001_12000 = self.db_conn.fetch_data(query_8001_12000)[0][0] if self.db_conn.fetch_data(
            query_8001_12000) else 0
        faixa_12001_16000 = self.db_conn.fetch_data(query_12001_16000)[0][0] if self.db_conn.fetch_data(
            query_12001_16000) else 0
        faixa_16001_20000 = self.db_conn.fetch_data(query_16001_20000)[0][0] if self.db_conn.fetch_data(
            query_16001_20000) else 0
        faixa_20001_25000 = self.db_conn.fetch_data(query_20001_25000)[0][0] if self.db_conn.fetch_data(
            query_20001_25000) else 0

        # Fechando a conexão
        self.db_conn.fechar_conexao()

        # Retornando os dados em um formato JSON
        return {
            'faixa_1001_2000': faixa_1001_2000,
            'faixa_2001_3000': faixa_2001_3000,
            'faixa_3001_4000': faixa_3001_4000,
            'faixa_4001_6000': faixa_4001_6000,
            'faixa_6001_8000': faixa_6001_8000,
            'faixa_8001_12000': faixa_8001_12000,
            'faixa_12001_16000': faixa_12001_16000,
            'faixa_16001_20000': faixa_16001_20000,
            'faixa_20001_25000': faixa_20001_25000
        }


# Instanciando a classe de utilidades
api_utils = APIUtils()


# Rota para os dados de faixa etária
@app.route("/data1", methods=["GET"])
def get_faixa_etarias():
    faixa_etarias = api_utils.get_faixa_etarias()
    return jsonify(faixa_etarias)


# Rota para os dados de gênero
@app.route("/data2", methods=["GET"])
def get_contagem_genero():
    contagem_genero = api_utils.get_contagem_genero()
    return jsonify(contagem_genero)

@app.route("/data3", methods=["GET"])
def get_faixa_salarial():
    faixa_salarial = api_utils.get_faixa_salarial()
    return jsonify(faixa_salarial)

@app.route("/data4", methods=["GET"])
def get_etnia():
    contagem_etnia = api_utils.get_etnia()
    return jsonify(contagem_etnia)
@app.route("/data5" , methods=["GET"])
def get_pcd():
    pcdUtils = api_utils.get_pcd_info()
    return jsonify(pcdUtils)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
