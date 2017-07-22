from collections import namedtuple

Posicao = namedtuple('Posicao', ['id', 'nome', 'abreviacao'])
Status = namedtuple('Status', ['id', 'nome'])

_posicoes = {
    1: Posicao(1, u'Goleiro', 'gol'),
    2: Posicao(2, u'Lateral', 'lat'),
    3: Posicao(3, u'Zagueiro', 'zag'),
    4: Posicao(4, u'Meia', 'mei'),
    5: Posicao(5, u'Atacante', 'ata'),
    6: Posicao(6, u'Técnico', 'tec')
}

_atleta_status = {
    2: Status(2, u'Dúvida'),
    3: Status(3, u'Suspenso'),
    5: Status(5, u'Contundido'),
    6: Status(6, u'Nulo'),
    7: Status(7, u'Provável')
}

class Atleta(object):
    """ Representa um atleta (jogador ou técnico), e possui informações como o apelido, clube e pontuação obtida """

    def __init__(self, atleta_id, apelido, pontos, scout, posicao_id, clube, status_id=None):
        self.id = atleta_id
        self.apelido = apelido
        self.pontos = pontos
        self.scout = scout
        self.posicao = _posicoes[posicao_id]
        self.clube = clube
        self.status = _atleta_status[status_id] if status_id else None


class Clube(object):
    """ Representa um dos 20 clubes presentes no campeonato, e possui informações como o nome e a abreviação """

    def __init__(self, id, nome, abreviacao):
        self.id = id
        self.nome = nome
        self.abreviacao = abreviacao
