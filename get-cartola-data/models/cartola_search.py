#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 12:27:45 2017

@author: Marku
@documentation: obtém os scouts e dados da api do cartolafc para análise.
"""

import argparse
import cartolafc
import csv
import pandas as pd


# COMMAND PARSER
def cartolaFC_parser():
    global modelo, file

    # USE EXAMPLES:
    # =-=-=-=-=-=-=
    # % cartola_search --clube sf                           --- searches term in SF geographic box <DEFAULT = none>
    # % cartola_search --modelo {mercado,clube,atleta}      --- searches term in SF geographic box <DEFAULT = none>

    # % cartola_search <search term> -l en          --- searches term with lang=en (English) <DEFAULT = en>
    # % cartola_search <search term> -t {m,r,p} --- searches term of type: mixed, recent, or popular <DEFAULT = recent>
    # % cartola_search <search term> -c 12      --- searches term and returns 12 tweets (count=12) <DEFAULT = 1>
    # % cartola_search <search term> -o {ca, tx, id, co, rtc)   --- searches term and sets output options <DEFAULT = ca, tx>

    # Parse the command
    parser = argparse.ArgumentParser(description='Cartola Search')
    parser.add_argument('--clube', action='store', dest='clube', help='Nome do clube da Série A')
    parser.add_argument('--modelo', action='store', dest='modelo', help='{mercado,clube,atleta,atletas}')
    parser.add_argument('--f', action='store', dest='file', help='Nome do arquivo de saída dos dados')

    args = parser.parse_args()

    # modelo
    modelo = args.modelo
    if (not (modelo)):
        modelo = 'mercado'

    if (not (modelo in ('mercado', 'atleta', 'atletas', 'clube'))):
        print("WARNING: Search type must be one of: mercado, atleta, atletas or clube")
        exit()

    file = args.file
    if (not (file)):
        file = 'cartola_data.csv'

    print("modelo:{}, file:{}".format(modelo, file))


# AUTHENTICATION (OAuth)
def api_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()

    us_name = ak[0].split("\n")[0]
    us_pass = ak[1].split("\n")[0]

    # print("User Name:{}".format(us_name))
    # print("User Pass:{}".format(us_pass))

    api = cartolafc.Api(email=us_name, password=us_pass)
    return api


# GET MARKET INFO
def get_market(api):
    m = api.mercado()

    csvFile = open(file, 'w')
    csvWriter = csv.writer(csvFile)

    rows = ['aviso', 'fechamento', 'rodada_atual', 'status', 'times_escalados']

    csvWriter.writerow(rows)
    rows = [m.aviso, str(m.fechamento), str(m.rodada_atual), m.status.nome, str(m.times_escalados)]
    csvWriter.writerow(rows)
    csvFile.close()


def get_atletas(api):
    m = api.mercado()

    if m.status.id == 2:
        print('Mercado Fechado. Impossível obter atletas')
        exit()

    csvFile = open(file, 'w')
    csvWriter = csv.writer(csvFile)

    rows = ["id", "apelido", "clube", "posicao", "ultima_pontuacao",
            "status", "FD", "G", "CA", "FC", "FS", "DD", "GS", "PP", "SG", "CV", "FT", "A", "PE",
            "RB", "DP", "I", "FF", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12",
            "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12"]

    csvWriter.writerow(rows)

    for a in api.mercado_atletas():
        scouts = {'FD': 0, 'G': 0, 'CA': 0, 'FC': 0, 'FS': 0, 'DD': 0, 'GS': 0, 'PP': 0, 'SG': 0, 'CV': 0, 'FT': 0,
                  'A': 0, 'PE': 0, 'RB': 0, 'DP': 0, 'I': 0, 'FF': 0}

        try:

            for l in a.scout.items():
                scouts[l[0]] = l[1]
        except AttributeError:
            print("Erro no atleta id={} nome={} scouts={}".format(a.id, a.apelido, a.scout))

        row = [a.id, a.apelido, a.clube.nome, a.posicao[1], a.pontos, a.status[1]]

        for l in scouts.items():
            row.append(l[1])

        hist_pont = api.pontuacao_atleta(id=a.id)

        for l in hist_pont:
            row.append(l.pontos)

        for l in hist_pont:
            row.append(l.preco)

        csvWriter.writerow(row)

    csvFile.close()


# MAIN ROUTINE
def main():
    global api, cmax, locords

    # OAuth key file
    authfile = '../../auth.k'

    cartolaFC_parser()
    api = api_oauth(authfile)

    if (api):
        # print("API INICIADA {}".format(api) )
        if (modelo == 'mercado'):
            get_market(api)
        elif (modelo == 'atletas'):
            get_atletas(api)


            # tw_search(api)


if __name__ == "__main__":
    main()

