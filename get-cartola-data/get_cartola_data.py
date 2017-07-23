import argparse

from cache import MyCache
from facades.cartola_facade import CartolaFacade
from facades.mongo_facade import PyMongoFacade


def parse_parameters():
    parser = argparse.ArgumentParser(description='Cartola Search')

    parser.add_argument('-option',  action='store', dest='option', help='Opcoes {fu:force_update}')
    parser.add_argument('-auth', action='store',dest='auth', help='Path do arquivo de autenticação')

    args = parser.parse_args()
    result = {}

    if ( args.option != None ):
        result['option']=args.option

    if ( args.auth != None ):
        result['auth']=args.auth


    return result

# MAIN ROUTINE
def main():
    #parse dos parâmetros de entrada e carga em cache
    cache = MyCache(parse_parameters())

    #instancia classe facade do cartola
    cartola_facade = CartolaFacade(cache.cache['auth'])

    if cartola_facade.autenticate():
        #obtém dados do mercado
        mercado = cartola_facade.get_mercado()

        #instancia classe facade do mongo
        mongo_facade = PyMongoFacade()

        #pesquisa se os dados da rodada atual já existem no banco
        mercado_rodada_atual = mongo_facade.get_rodada_object_id(mercado.rodada_atual)

        if (cache.cache['option']!='fu'):
            #caso não existam dados salvos
            if (type(mercado_rodada_atual) == None ) | (len(mercado_rodada_atual)==0) :
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

