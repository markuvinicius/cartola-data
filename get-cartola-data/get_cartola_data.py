import argparse

from cache import MyCache
from facades.cartola_facade import CartolaFacade
from facades.mongo_facade import PyMongoFacade


def parse_parameters():
    parser = argparse.ArgumentParser(description='Cartola Search')

    parser.add_argument('-option',  action='store', dest='option', help='Opcoes {fu:force_update}')
    parser.add_argument('-auth', action='store',dest='auth', help='Path do arquivo de autenticação')
    parser.add_argument('-elk' , action='store',dest='elk', help='Define uso do ElasticSearch')

    args = parser.parse_args()
    result = {}

    if ( args.option != None ):
        result['option']=args.option

    if ( args.auth != None ):
        result['auth']=args.auth
    else:
        result['auth']='./../auth.k'

    if (args.elk != None ):
        result['elk'] = True
    else:
        result['elk'] = False

    return result

# MAIN ROUTINE
def main():
    #parse dos parâmetros de entrada e carga em cache
    cache = MyCache(parse_parameters())

    #instancia classe facade do cartola
    cartola_facade = CartolaFacade(cache.cache['auth'],
                                   cache.cache['elk'])

    if cartola_facade.autenticate():
        #obtém dados do mercado
        mercado = cartola_facade.get_mercado()

        #instancia classe facade do mongo
        mongo_facade = PyMongoFacade()

        #pesquisa se a rodada atual já está salva no mongo
        rodada_existe = mongo_facade.rodada_exists(mercado.rodada_atual)

        #se rodada já existir no mongo, só atualiza se FORCE UPDATE foi usado
        if (rodada_existe):
            if (cache.cache['option']=='fu'):
                # obtém lista atualizada de atletas
                lista = cartola_facade.get_atletas()

                #persiste dados dos atletas no mongodb
                result = mongo_facade.insert_atletas(lista,mercado.rodada_atual)
        else:
            # obtém lista atualizada de atletas
            lista = cartola_facade.get_atletas()

            # persiste dados dos atletas no mongodb
            result = mongo_facade.insert_atletas(lista, mercado.rodada_atual)



if __name__ == "__main__":
    main()

