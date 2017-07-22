from facades.cartola_facade import CartolaFacade


# MAIN ROUTINE
def main():
    # OAuth key file
    authfile = '../../auth.k'
    cartola_facade = CartolaFacade(path=authfile)

    if cartola_facade.autenticate():
        lista = cartola_facade.get_atletas()





if __name__ == "__main__":
    main()

