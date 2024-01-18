import os
from urllib.parse import quote_plus
from sqlalchemy import MetaData, Table, create_engine, insert
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class EdatLogService:
    """ Serviço de persistência de log """

    def __init__(self, aplicacao: str) -> None:
        """ Construtor da classe 

            :param aplicacao: nome da aplicação. O nome trata-se do mesmo nome da tabela alvo.
        """
        metadata = MetaData()
        self.__conn = self.__get_connection()
        self.__tabela = Table(aplicacao, metadata, autoload_with=self.__conn.engine, extend_existing=True)

    def __get_connection(self):
        """ Método privado para obter a conexão com o banco de dados de log 

            :return: Connection -> conexão com o banco de dados
        """
        try:
            USERNAME = quote_plus(os.environ.get('USUARIO_AVALIACAO', default=''))
            PASSWORD = quote_plus(os.environ.get('SENHA_AVALIACAO', default=''))
            HOST = os.environ.get('HOST_AVALIACAO', default='')
            PORT = os.environ.get('PORT_AVALIACAO', default=46002)
            DB = os.environ.get('DB_LOG', default='logs')

            SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}"

            engine = create_engine(SQLALCHEMY_DATABASE_URI)
            connection = engine.connect()

            return connection

        except Exception as e: 
            logger.error(msg=f'Erro ao conectar no banco de dados: {str(e)}')
            raise Exception(e)

    def salvar(self, **kwargs) -> None:
        """
            Método para persistir em tabela informações relevantes sobre o evento realizado pelo usuário.

            :param kwargs: campos nomeados para inserir na tabela correspondente.
        """
        try:
            stmt = insert(self.__tabela).values(kwargs)
            self.__conn.execute(stmt)

        except Exception as e:
            logger.error(msg=f'Erro ao salvar na tabela {self.__tabela} de logs: {str(e)}')
            raise Exception(e)

