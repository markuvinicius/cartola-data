import cartolafc
import json

from models.cartola_models import Atleta

class CartolaFacade(object):

    _path = None
    _api  = None

    def __init__(self, path):
        self._path = path

    # AUTHENTICATION (OAuth)
    def autenticate(self):
        _retorno = False

        try:
            with open(self._path, "r") as f:
                ak = f.readlines()
            f.close()

            us_name = ak[0].split("\n")[0]
            us_pass = ak[1].split("\n")[0]

            print("User Name:{}".format(us_name))
            print("User Pass:{}".format(us_pass))

            self._api = cartolafc.Api(email=us_name, password=us_pass,attempts=5)
            _retorno = True
        except:
            _retorno = False

        return _retorno

    #obtem lista de todos os atletas inscritos no cartola
    def get_atletas(self):
        atletas = self._api.mercado_atletas()
        lista=[]

        for a in atletas:
            atleta = Atleta(a.id,
                            a.apelido,
                            a.pontos,
                            a.scout,
                            a.posicao[0],
                            a.clube.nome,
                            a.status[0])

            lista.append(atleta)

        return atleta