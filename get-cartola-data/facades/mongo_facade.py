from pymongo import MongoClient


class PyMongoFacade(object):

    _connection_url = 'mongodb://localhost:27017'
    _client=None

    _db_cartola='cartola-fc'
    _db=None


    def __init__(self):
        self._client = MongoClient(self._connection_url)
        self._db = self._client[self._db_cartola]

    def insert_atletas(self,atletas,rodada):
        list_atletas = [atleta.__dict__ for atleta in atletas]
        _rodada = [{'id_rodada':rodada,'atletas':list_atletas}]

        result = self._db.mercado.insert_many(_rodada)

        return result

    def get_rodada_object_id(self,rodada):
        document = self._db.mercado.find({'id_rodada': rodada})
        return document[0]['_id']


    def get_mercado_rodada(self,rodada):
        lista=None
        try:
            document = self._db.mercado.find({'id_rodada':rodada})

            lista=[atleta for atleta in document]
        except:
            print('erro ao pesquisar no mongo')

        return lista


