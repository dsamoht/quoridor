""" Importation des modules
"""
import argparse
import copy
import quoridorx
import quoridor


def analyser_commande():
    """ Retourne le parser d'arguments """
    parser = argparse.ArgumentParser(description='Quoridor')
    parser.add_argument('-a', '--ASCII', help='Mode ASCII', action='store_true')
    parser.add_argument('-x', '--graphique', help='Mode Graphique.', action='store_true')
    return parser.parse_args()


def quoridor_game():
    """ Boucles de jeu """

    if analyser_commande().ASCII:
    #Mode manuel contre le serveur
        jeu = quoridor.Quoridor([f"Joueur", 'RCXD'])
        game_state = {}
        while True: #Boucle de jeu
            print(jeu)
            try:
                while True: #Boucle d'input
                    type_coup = input("Entrez le TYPE de coup: \nD / d -- DÉPLACEMENT du pion\n"
                                      "MV / mv -- Placer un MUR VERTICAL\n"
                                      "MH / mh -- Placer un MUR HORIZONTAL\n: ").upper()
                    pos_x = int(input('Entrez la coordonnée HORIZONTALE (x) du coup: '))
                    pos_y = int(input('Entrez la coordonnée VERTICALE (y) du coup: '))
                    position = [pos_x, pos_y]
                    if (pos_x and pos_y) in range(1, 10) and type_coup in ['D', 'MV', 'MH']:
                        break
                    else:
                        print('Entrez un coup VALIDE.')
                        continue
                if type_coup == "D":
                    jeu.déplacer_jeton(1, (pos_x, pos_y))
                elif type_coup == "MV":
                    jeu.placer_mur(1, (pos_x, pos_y), "vertical")
                elif type_coup == "MH":
                    jeu.placer_mur(1, (pos_x, pos_y), "horizontal")
            except ValueError:
                print("Entrez un coup VALIDE.")
            except quoridor.QuoridorError as err:
                print(err)
                continue
            if jeu.partie_terminée():
                print(jeu.win)
                break
            #Coup du robot
            jeu.jouer_coup(2)
            if jeu.partie_terminée():
                print(jeu.win)
                break

    elif analyser_commande().graphique:
        jeu = quoridorx.QuoridorX(['Joueur', 'RCXD'])


if __name__ == '__main__':
    analyser_commande()
    quoridor_game()