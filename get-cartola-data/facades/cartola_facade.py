from datetime import datetime

import cartolafc
from cartolafc import CartolaFCError
from elasticsearch import Elasticsearch
from models.cartola_models import Atleta


class CartolaFacade(object):

    #private variables
    _path = None
    _api  = None
    _es   = None
    _doc  = None
    _elk  = None

    def __init__(self, path , elk):
        self._path = path
        self._elk = elk

        # documento de log (elasticsearch)
        self._doc = {
            'class': str(type(self)),
            'timestamp': datetime.now(),
            'method': None,
            'step': None,
            'TYPE': None
        }

        #conecta ao elasticsearch apenas se o parametro passado for diferente de none no argumento elk
        if (self._elk ):
            self._es = Elasticsearch()
            self._es.indices.create(index='cartola_api_index', ignore=400)


    # AUTHENTICATION (OAuth)
    def autenticate(self):

        self._doc['method']='autenticate'

        _retorno = False

        try:
            #abre o arquivo de autenticação e lê o conteúdo (usuário/senha do cartola)
            with open(self._path, "r") as f:
                ak = f.readlines()
            f.close()

            #registra o log de sucesso na leitura do arquivo
            self._doc['step'] = 'Credenciais de autenticação carregadas do arquivo'
            self._doc['TYPE'] = 'INFO'

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)
        except IOError as inst:

            #registra log de erro na leitura do arquivo
            self._doc['step'] = "I/O error({}):".format(inst)
            self._doc['TYPE'] = 'ERROR'
            self._doc['timestamp'] = datetime.now()

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

        try:
            us_name = ak[0].split("\n")[0]
            us_pass = ak[1].split("\n")[0]

            ##### Registra a tentativa de autenticação ######
            self._doc['step'] = 'Autenticando na API do cartola'
            self._doc['TYPE'] = 'INFO'
            self._doc['timestamp'] = datetime.now()

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)


            self._api = cartolafc.Api(email=us_name, password=us_pass,attempts=5)

            ##### Registra o sucesso na autenticação #####
            self._doc['step'] = 'Autenticado com sucesso na API do Cartola'
            self._doc['timestamp'] = datetime.now()

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type",  body=self._doc)

            _retorno = (type(self._api)!=type(None))
        except CartolaFCError as erro:

            ##### Registra a falha na tentativa de autenticação ######
            self._doc['step'] = 'Erro ao autenticar na API cartola: {}'.format(erro)
            self._doc['TYPE'] = 'ERROR'
            self._doc['timestamp'] = datetime.now()

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

            _retorno = False
        return _retorno

    #obtém a identificação numérica da rodada atual
    def get_mercado(self):
        ##### Registra o carregamento do status do mercado #####
        self._doc['method']='get_mercado'
        self._doc['timestamp']=datetime.now()
        self._doc['TYPE']='INFO'
        self._doc['step'] = 'Obtendo dados do mercado'

        if (self._elk):
            self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

        mercado = None
        try:
            mercado = self._api.mercado()
        except CartolaFCError as erro:

            ##### Registra a falha na tentativa de autenticação ######
            self._doc['step'] = 'Erro ao obter mercado: {}'.format(erro)
            self._doc['TYPE'] = 'ERROR'
            self._doc['timestamp'] = datetime.now()

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

        return mercado


    #obtem lista de todos os atletas inscritos no cartola
    def get_atletas(self):

        ##### Registra o carregamento dos atletas #####
        self._doc['method'] = 'get_atletas'
        self._doc['timestamp'] = datetime.now()
        self._doc['TYPE'] = 'INFO'
        self._doc['step'] = 'Obtendo atletas'
        if (self._elk):
            self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

        lista = []
        try:
            atletas = self._api.mercado_atletas()

            ##### Registra o carregamento dos atletas #####
            self._doc['method'] = 'get_atletas'
            self._doc['timestamp'] = datetime.now()
            self._doc['TYPE'] = 'INFO'
            self._doc['step'] = 'Atletas obtidos: {}'.format( len(atletas) )

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)


            for a in atletas:
                atleta = Atleta(a.id,
                                a.apelido,
                                a.pontos,
                                a.scout,
                                a.posicao[0],
                                a.clube.nome,
                                a.status[0])

                lista.append(atleta)
        except CartolaFCError as error:
            ##### Registra o carregamento dos atletas #####
            self._doc['method'] = 'get_atletas'
            self._doc['timestamp'] = datetime.now()
            self._doc['TYPE'] = 'ERROR'
            self._doc['step'] = 'Erro ao obter atletas: {}'.format(error)

            if (self._elk):
                self._es.index(index="cartola_api_index", doc_type="test-type", body=self._doc)

        return lista