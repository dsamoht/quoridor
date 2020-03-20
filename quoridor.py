""" Module Quoridor qui contient les classes Quoridor et QuoridorError.
"""

import copy
import networkx as nx

class QuoridorError(Exception):
    """ Classe QuoridorError qui affiche des message d'erreur en cas d'exception.
    """

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return str(self.message)


class Quoridor():
    """ Classe Quoridor qui contient toutes les méthodes nécessaires pour le jeu.
    """

    def __init__(self, joueurs, murs=None):
        """ Class Quoridor Game """

        if "__iter__" not in dir(joueurs):
            raise QuoridorError("La variable 'joueurs' n'est pas itérable.")
        taille = 0
        for i in joueurs:
            taille += 1
            if taille > 2:
                raise QuoridorError("L'itérable 'joueurs' contient plus de deux valeurs.")

        # Traitement
        self.joueurs = [{}, {}]
        self.type_coup = ''
        self.pos = []

        for i, elem in enumerate(joueurs):
            if isinstance(elem, dict):
                if elem['murs'] > 10 or elem['murs'] < 0:
                    raise QuoridorError("Un joueurs peut placer entre 0 et 10 murs.")
                self.joueurs[i] = elem
            if isinstance(elem, str):
                if i == 0:
                    self.joueurs[0] = {'nom': elem, 'murs': 10, 'pos': (5, 1)}
                if i == 1:
                    self.joueurs[1] = {'nom': elem, 'murs': 10, 'pos': (5, 9)}

        if self.joueurs[0]['pos'] == self.joueurs[1]['pos']:
            raise QuoridorError("Cette position est occupée.")

        for i in range(2):
            if min(self.joueurs[i]['pos']) < 1 or max(self.joueurs[i]['pos']) > 9:
                raise QuoridorError("Cette position est invalide.")

        # Traitement de l'arguments "murs"
        self.murs = None
        if murs:
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' doit être un dictionnaire.")
            self.murs = murs
        if not murs:
            self.murs = {'horizontaux': [], 'verticaux': []}

        # Traitement du nombre total de murs (placés et plaçables)
        if (self.joueurs[0]['murs'] + self.joueurs[1]['murs']
                + len(self.murs['horizontaux']) + len(self.murs['verticaux'])) != 20:
            raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20.")

        # Traitement de la position des murs (respect des dimensions du damier)
        self.pos_invalide_murs_h = []
        self.pos_invalide_murs_v = []

        if self.murs['horizontaux']:
            for pos in self.murs['horizontaux']:
                if pos[0] not in range(1, 9) or pos[1] not in range(2, 10):
                    raise QuoridorError('Position de mur invalide.')
                if pos in self.pos_invalide_murs_h:
                    raise QuoridorError('Position de mur invalide.')
                self.pos_invalide_murs_h += [list(pos), list((pos[0]-1, pos[1])),
                                             list((pos[0]+1, pos[1]))]
                self.pos_invalide_murs_v += [list((pos[0]+1, pos[1]-1))]

        if self.murs['verticaux']:
            for pos in self.murs['verticaux']:
                if pos[0] not in range(2, 10) or pos[1] not in range(1, 9):
                    raise QuoridorError('Position de mur invalide.')
                if pos in self.pos_invalide_murs_v:
                    raise QuoridorError('Position de mur invalide.')
                self.pos_invalide_murs_h += [list((pos[0]-1, pos[1]+1))]
                self.pos_invalide_murs_v += [list(pos), list((pos[0], pos[1]-1)),
                                             list((pos[0], pos[1]+1))]

        self.etat = dict(zip(['joueurs', 'murs'], [self.joueurs, self.murs]))

    def état_partie(self):
        """ État """
        return self.etat

    def __str__(self):
        """ ASCII """
        self.etat = self.état_partie()

        mat = [[' ' for _ in range(39)] for _ in range(17)]
        for index in range(17):
            mat[index][2] = mat[index][38] = '|'
            for y in range(4, 39, 4):
                if index % 2 == 0:
                    mat[index][y] = '.'
                    mat[index][0] = str([9, 8, 7, 6, 5, 4, 3, 2, 1][(index//2)])

        j_pos_ligne = 16 - ((self.etat['joueurs'][0]['pos'][1]) - 1) * 2
        j_pos_colonne = 4 * self.etat['joueurs'][0]['pos'][0]
        a_pos_ligne = 16 - ((self.etat['joueurs'][1]['pos'][1]) - 1) * 2
        a_pos_colonne = 4 * self.etat['joueurs'][1]['pos'][0]
        mat[j_pos_ligne][j_pos_colonne] = '1'
        mat[a_pos_ligne][a_pos_colonne] = '2'

        mur_h_list = []
        mur_v_list = []

        if self.etat['murs']['horizontaux']:
            for mur_h in self.etat['murs']['horizontaux']:
                mur_h_list.append([16 - (mur_h[1] - 1) * 2 + 1, 4 * mur_h[0] - 1])

        if self.etat['murs']['verticaux']:
            for mur_v in self.etat['murs']['verticaux']:
                mur_v_list.append([16 - (mur_v[1] - 1) * 2, 4 * mur_v[0] - 2])

        for elem in mur_h_list:
            mat[elem[0]][elem[1]:(elem[1]+7)] = '-------'

        for elem in mur_v_list:
            for i in range(3):
                mat[elem[0]-i][elem[1]] = '|'

        for x in range(17):
            mat[x] = ''.join(mat[x])

        ascii_str = (f"Légende: 1={self.joueurs[0]['nom']}, 2={self.joueurs[1]['nom']}\n"
                     + "   -----------------------------------\n"
                     + "\n".join(mat) + "\n" + "--|-----------------------------------\n"
                     + "  | 1   2   3   4   5   6   7   8   9")
        return ascii_str

    def construire_graphe(self, joueurs, murs_horizontaux, murs_verticaux):
        """ Network of Available Moves """
        graphe = nx.DiGraph()

        # pour chaque colonne du damier
        for x in range(1, 10):
            # pour chaque ligne du damier
            for y in range(1, 10):
                # ajouter les arcs de tous les déplacements possibles pour cette tuile
                if x > 1:
                    graphe.add_edge((x, y), (x-1, y))
                if x < 9:
                    graphe.add_edge((x, y), (x+1, y))
                if y > 1:
                    graphe.add_edge((x, y), (x, y-1))
                if y < 9:
                    graphe.add_edge((x, y), (x, y+1))

        # retirer tous les arcs qui croisent les murs horizontaux
        for x, y in murs_horizontaux:
            graphe.remove_edge((x, y-1), (x, y))
            graphe.remove_edge((x, y), (x, y-1))
            graphe.remove_edge((x+1, y-1), (x+1, y))
            graphe.remove_edge((x+1, y), (x+1, y-1))

        # retirer tous les arcs qui croisent les murs verticaux
        for x, y in murs_verticaux:
            graphe.remove_edge((x-1, y), (x, y))
            graphe.remove_edge((x, y), (x-1, y))
            graphe.remove_edge((x-1, y+1), (x, y+1))
            graphe.remove_edge((x, y+1), (x-1, y+1))

        # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
        j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])
        # traiter le cas des joueurs adjacents
        if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
            graphe.remove_edge(j1, j2)
            graphe.remove_edge(j2, j1)

            def ajouter_lien_sauteur(noeud, voisin):
                """
                :param noeud: noeud de départ du lien.
                :param voisin: voisin par dessus lequel il faut sauter.
                """
                saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

                if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                    graphe.add_edge(noeud, saut)

                else:
                # ajouter les sauts en diagonale
                    for saut in graphe.successors(voisin):
                        graphe.add_edge(noeud, saut)

            ajouter_lien_sauteur(j1, j2)
            ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
        for x in range(1, 10):
            graphe.add_edge((x, 9), 'B1')
            graphe.add_edge((x, 1), 'B2')

        return graphe

    def déplacer_jeton(self, joueur, position):
        """ Move Player at Specified Position """
        if joueur not in range(1, 3):
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2")
        if (position[0] or position[1]) not in range(1, 10):
            raise QuoridorError("La position spécifiée est en dehors du damier")
        if position not in self.construire_graphe([self.joueurs[0]['pos'],
            self.joueurs[1]['pos']],
            self.murs['horizontaux'], 
            self.murs['verticaux']).successors(tuple(self.joueurs[joueur-1]['pos'])):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        else:
            self.joueurs[joueur-1]['pos'] = position
        return self

    def jouer_coup(self, joueur):
        """ Automatic Move """
        
        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
    
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        #Construction du chemin le plus rapide pour joueur 1 et 2
        graphe = self.construire_graphe([self.joueurs[0]['pos'],
                 self.joueurs[1]['pos']], self.murs['horizontaux'],
                 self.murs['verticaux'])

        chemin1 = nx.shortest_path(graphe, tuple(self.joueurs[0]['pos']), 'B1')
        chemin2 = nx.shortest_path(graphe, tuple(self.joueurs[1]['pos']), 'B2')

        self.type_coup = 'D'
        self.pos = list(chemin1[1:-1][0])

        coord_mur = ()
        if joueur == 1: #Si c'est le joueur 1:
            if len(chemin1) <= len(chemin2) or self.joueurs[0]['murs'] == 0:
                #Décide de faire un déplacement
                self.déplacer_jeton(1, chemin1[1:-1][0])
                self.type_coup = 'D'
                self.pos = list(chemin1[1:-1][0])
            else:
                for i in range(1, len(chemin2)-1):
                    try:
                        if chemin2[i-1][0] > chemin2[i][0]:       #J2 va vers l'Ouest
                            coord_mur = (chemin2[i][0]+1, chemin2[i][1])
                            if coord_mur[1] == 9: # Gestion des bornes
                                coord_mur = chemin2[i][0], chemin2[i][1]-1
                            self.placer_mur(1, coord_mur, 'vertical')
                            self.type_coup = 'MV'
                            self.pos = list(coord_mur)
                            # Décide de placer un mur vertical en J2(x+1, y)
                        elif chemin2[i-1][0] < chemin2[i][0]:    #J2 va vers l'Est
                            coord_mur = chemin2[i]
                            if coord_mur[1] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0], chemin1[i][1]-1
                            self.placer_mur(1, coord_mur, 'vertical')
                            self.type_coup = 'MV'
                            self.pos = list(coord_mur)
                            #Décide de placer un mur vertical en J2(x, y)
                        elif chemin2[i-1][1] > chemin2[i][1]:    #J2 va vers le Sud
                            coord_mur = (chemin2[i][0], chemin2[i][1]+1)
                            if coord_mur[0] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0]-1, chemin1[i][1]
                            self.placer_mur(1, coord_mur, 'horizontal')
                            self.type_coup = 'MH'
                            self.pos = list(coord_mur)
                            #Décide de placer un mur horizontal en J2(x, y+1)
                        elif chemin2[i-1][1] < chemin2[i][1]:   #J2 va vers le Nord
                            coord_mur = chemin2[i]
                            if coord_mur[0] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0]-1, chemin1[i][1]
                            self.placer_mur(1, coord_mur, 'horizontal')
                            self.type_coup = 'MH'
                            self.pos = list(coord_mur)
                            #Décide de placer un mur horizontal en J2(x, y)
                    except QuoridorError:
                        pass
                    else:
                        break

        else:           #Si c'est le joueur 2
            if len(chemin2) <= len(chemin1) or self.joueurs[1]['murs'] == 0:
                #Décide de faire un déplacement
                self.déplacer_jeton(joueur, chemin2[1:][0])

            else:
                for i in range(1, len(chemin1)-1):
                    try:
                        if chemin1[i-1][0] > chemin1[i][0]:       #J1 va vers l'Ouest
                            coord_mur = (chemin1[i][0]+1, chemin1[i][1])
                            if coord_mur[1] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0], chemin1[i][1]-1
                            self.placer_mur(joueur, coord_mur, 'vertical')
                            # Décide de placer un mur vertical en J1(x+1, y)
                        elif chemin1[i-1][0] < chemin1[i][0]:    #J1 va vers l'Est
                            coord_mur = chemin1[i]
                            if coord_mur[1] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0], chemin1[i][1]-1
                            self.placer_mur(joueur, coord_mur, 'vertical')
                            #Décide de placer un mur vertical en J2(x, y)
                        elif chemin1[i-1][1] > chemin1[i][1]:    #J1 va vers le Sud
                            coord_mur = (chemin1[i][0], chemin1[i][1]+1)
                            if coord_mur[0] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0]-1, chemin1[i][1]
                            self.placer_mur(joueur, coord_mur, 'horizontal')
                            #Décide de placer un mur horizontal en J1(x, y+1)
                        elif chemin1[i-1][1] < chemin1[i][1]:   #J1 va vers le Nord
                            coord_mur = chemin1[i]
                            if coord_mur[0] == 9: # Gestion des bornes
                                coord_mur = chemin1[i][0]-1, chemin1[i][1]
                            self.placer_mur(joueur, coord_mur, 'horizontal')
                            #Décide de placer un mur horizontal en J1(x, y)
                    except QuoridorError:
                        pass
                    else:
                        break
        return self

    def partie_terminée(self):
        """ Print the Winner """

        self.win = False
        if self.joueurs[0]['pos'][1] == 9:
            self.win = 1
        if self.joueurs[1]['pos'][1] == 1:
            self.win = 2
        return self.win

    def placer_mur(self, joueur, position, orientation):
        """ Place Wall at Position with Orientation """
        murs_temp = copy.deepcopy(self.murs)

        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2")

        if self.joueurs[joueur-1]['murs'] == 0:
            raise QuoridorError("Tous les murs du joueur sont déjà placés.")

        if orientation == 'horizontal':
            murs_temp['horizontaux'].append(list(position))
            if list(position) in self.murs['horizontaux']:
                raise QuoridorError("Un mur occupe déjà cette position.")
            if list(position) in self.pos_invalide_murs_h:
                raise QuoridorError("Position invalide pour cette orientation.")
            if position[0] not in range(1, 9) or position[1] not in range(2, 10):
                raise QuoridorError("Position invalide pour cette orientation.")
            if (not nx.has_path(self.construire_graphe([self.joueurs[0]['pos'],
                  self.joueurs[1]['pos']], murs_temp['horizontaux'],
                  murs_temp['verticaux']), tuple(self.joueurs[0]['pos']), 'B1')
                  or not nx.has_path(self.construire_graphe([self.joueurs[0]['pos'],
                  self.joueurs[1]['pos']],
                  murs_temp['horizontaux'],
                  murs_temp['verticaux']), tuple(self.joueurs[1]['pos']), 'B2')):
                raise QuoridorError("Position invalide pour cette orientation.")
            else:
                self.murs['horizontaux'].append(list(position))
                self.joueurs[joueur-1]['murs'] -= 1
                self.pos_invalide_murs_h += [list(position), list((position[0]-1, position[1])),
                list((position[0]+1, position[1]))]
                self.pos_invalide_murs_v += [list((position[0]+1, position[1]-1))]
    
        if orientation == 'vertical':
            murs_temp['verticaux'].append(list(position))
            if list(position) in self.murs['verticaux']:
                raise QuoridorError("Un mur occupe déjà cette position.")
            if list(position) in self.pos_invalide_murs_v:
                raise QuoridorError("Position invalide pour cette orientation.")
            if position[0] not in range(2, 10) or position[1] not in range(1, 9):
                raise QuoridorError("Position invalide pour cette orientation.")
            if (not nx.has_path(self.construire_graphe([self.joueurs[0]['pos'],
                  self.joueurs[1]['pos']], murs_temp['horizontaux'],
                  murs_temp['verticaux']), tuple(self.joueurs[0]['pos']), 'B1')
                  or not nx.has_path(self.construire_graphe([self.joueurs[0]['pos'],
                  self.joueurs[1]['pos']],
                  murs_temp['horizontaux'],
                  murs_temp['verticaux']), tuple(self.joueurs[1]['pos']), 'B2')):
                raise QuoridorError("Position invalide pour cette orientation.")
            else:
                self.murs['verticaux'].append(list(position))
                self.joueurs[joueur-1]['murs'] -= 1
                self.pos_invalide_murs_h += [list((position[0]-1, position[1]+1))]
                self.pos_invalide_murs_v += [list(position), list((position[0], position[1]-1)),
                                             list((position[0], position[1]+1))]
        return self
