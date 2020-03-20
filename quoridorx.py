""" Importation modules """
from quoridor import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random


class QuoridorX(Quoridor):
	""" GUI Class """

	def __init__(self, joueurs, murs=None):
		""" Pygame Window"""
		super().__init__(joueurs, murs)
		pygame.init()
		self.display_width = 800
		self.display_height = 600
		
		# Load Sounds
		pygame.mixer.music.load("ressources/sounds/crystel_8bit.wav")
		self.error_sound = pygame.mixer.Sound("ressources/sounds/8-bit-error.wav")
		
		# Set Colors
		self.black = (0, 0, 0)
		self.white = (255, 255, 255)
		self.red = (240, 0, 0)
		self.dark_blue = (72, 118, 255)
		self.light_blue = (0, 191, 255)


		# Load Images
		self.game_title = pygame.image.load("ressources/images/quoridor_menu_2.0.png")
		j1_img = pygame.image.load("ressources/images/runner.png")
		self.j1_img = pygame.transform.scale(j1_img, (56, 56))
		self.j1_img_rect = self.j1_img.get_rect()
		self.j1_img_rect.center = (28, 28)
		j2_img = pygame.image.load("ressources/images/8bit_good.png")
		self.j2_img = pygame.transform.scale(j2_img, (56, 56))
		self.j2_img_rect = self.j2_img.get_rect()
		self.j2_img_rect.center = (28, 28)
		self.background_img = pygame.image.load("ressources/images/9x9_background_2.0.png")
		self.green_circle_img = pygame.image.load("ressources/images/green_circle_56x56pp_alpha.png")
		self.sound_on_img = pygame.image.load("ressources/images/speaker.png")
		self.sound_off_img = pygame.image.load("ressources/images/speaker_off.png")
		j1_face_img = pygame.image.load("ressources/images/runner_face.png")
		j2_face_img = pygame.image.load("ressources/images/8bit_good_face.png")
		self.j1_face_img = pygame.transform.scale(j1_face_img, (170, 170))
		self.j2_face_img = pygame.transform.scale(j2_face_img, (170, 170))

        # Set Pygame Window
		self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
		pygame.display.set_caption("Quoridor")
		pygame.display.set_icon(self.j1_face_img)
		self.clock = pygame.time.Clock()

		# Commands to Pixels
		self.posX_j = {1: 36, 2: 102, 3: 168, 4: 234, 5: 300, 6: 366, 7: 432, 8: 498, 9: 564}
		self.posY_j = {9: 36, 8: 102, 7: 168, 6: 234, 5: 300, 4: 366, 3: 432, 2: 498, 1: 564}
		self.posX_H = {1: 8, 2: 74, 3: 140, 4: 206, 5: 272, 6: 338, 7: 404, 8: 470}
		self.posY_H = {2: 526, 3: 460, 4: 394, 5: 328, 6: 262, 7: 196, 8: 130, 9: 64}
		self.posX_V = {2: 64, 3: 130, 4: 196, 5: 262, 6: 328, 7: 394, 8: 460, 9: 526}
		self.posY_V = {8: 8, 7: 74, 6: 140, 5: 206, 4: 272, 3: 338, 2: 404, 1: 470}

		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play(-1)
		self.start_menu()


	def green_circle(self, player=1):
		""" Player's Available Moves """
		mouse = pygame.mouse.get_pos()
		graphe = self.construire_graphe([self.joueurs[0]['pos'], self.joueurs[1]['pos']], self.murs['horizontaux'], self.murs['verticaux'])
		pos_list = list(graphe.successors(self.joueurs[player-1]['pos']))
		for pos in pos_list:
			if type(pos) != tuple:
				pos_list.remove(pos)
			elif (self.posX_j[pos[0]] - 28) < mouse[0] < (self.posX_j[pos[0]] + 28) and (self.posY_j[pos[1]] - 28) < mouse[1] <  (self.posY_j[pos[1]] + 28):
				self.game_display.blit(self.green_circle_img, (self.posX_j[pos[0]] - 28, self.posY_j[pos[1]] - 28))
				return pos
	
	def sound_button(self, image, x, y, action=None):
		""" Sound Switches """
		mouse = pygame.mouse.get_pos()
		if x-5 < mouse[0] < x + 35 and y-5 < mouse[1] < y + 35:
			pygame.draw.rect(self.game_display, self.red, (x-5, y-5, 40, 40))
			if pygame.mouse.get_pressed()[0] and action:
				action()
		else:
			pygame.draw.rect(self.game_display, self.black, (x-5, y-5, 40, 40))

		self.game_display.blit(image, (x, y))

	def quitgame(self):
		""" Quit Pygame """
		pygame.quit()
		quit()

	def button(self, text, pos_x, pos_y, width, height, inactive_col, active_col, action=None):
		""" Create Button Interaction """
		mouse = pygame.mouse.get_pos()
		pygame.draw.rect(self.game_display, self.black, (pos_x - 5, pos_y - 5, width + 10, height + 10))
	
		if pos_x + width > mouse[0] > pos_x and pos_y + height > mouse[1] > pos_y:
			pygame.draw.rect(self.game_display, active_col, (pos_x, pos_y, width, height))
			if pygame.mouse.get_pressed()[0] and action != None:
				action()
		else:
			pygame.draw.rect(self.game_display, inactive_col, (pos_x, pos_y, width, height))

		smallText = pygame.font.Font("freesansbold.ttf", 13)
		textSurf, textRect = self.text_object(text, smallText, self.white)
		textRect.center = ((pos_x + (width/2)), (pos_y + (height/2)))
		self.game_display.blit(textSurf, textRect)

	def text_object(self, text, font, color):
		""" Create Text Objects """
		textSurface = font.render(text, True, color)
		return textSurface, textSurface.get_rect()

	def start_menu(self):
		""" Main Menu Window """
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quitgame()
			self.game_display.blit(self.game_title, (0, 0))

			self.button("1 PLAYER", self.display_width//2 - 50, 300, 100, 50, self.light_blue, self.dark_blue, self.game_loop_1)
			self.button("2 PLAYERS", self.display_width//2 - 50, 370, 100, 50, self.light_blue, self.dark_blue, self.game_loop_2)
			self.button("QUIT", self.display_width//2 - 50, 480, 100, 50, self.light_blue, self.dark_blue, self.quitgame)

			self.sound_button(self.sound_off_img, 750, 550, self.music_off)
			self.sound_button(self.sound_on_img, 700, 550, self.music_on)

			pygame.display.update()

	def walls_windows(self):
		""" Display Player's Remaining Number of Walls """
		smallText = pygame.font.Font("freesansbold.ttf", 26)
		textSurf_1, textRect_1 = self.text_object(f" {self.joueurs[1]['murs']}", smallText, self.black)
		textRect_1.center = (720, 190)
		textSurf_2, textRect_2 = self.text_object(f" {self.joueurs[0]['murs']}", smallText, self.black)
		textRect_2.center = (720, 405)
		self.game_display.blit(textSurf_1, textRect_1)
		self.game_display.blit(textSurf_2, textRect_2)
		
	
	def walls(self):
		""" Display Walls """
		for pos in self.murs['horizontaux']:
			x, y = pos
			pygame.draw.rect(self.game_display, self.red, (self.posX_H[x], self.posY_H[y], 122, 10))

		for pos in self.murs['verticaux']:
			x, y = pos
			pygame.draw.rect(self.game_display, self.red, (self.posX_V[x], self.posY_V[y], 10, 122))
	
	def possible_walls(self):
		""" Interactive Available Walls Moves """
		mouse = pygame.mouse.get_pos()
		for i in range(1, 9):
			if self.posX_H[i] < mouse[0] < self.posX_H[i] + 56:
				for j in range(2, 10):
					if self.posY_H[j] < mouse[1] < self.posY_H[j] + 10:
						if [i, j] not in self.pos_invalide_murs_h:
							pygame.draw.rect(self.game_display, (255, 175, 175), (self.posX_H[i], self.posY_H[j], 122, 10))
							return (i, j), 'horizontal'
		
		for i in range(2, 10):
			if self.posX_V[i] < mouse[0] < self.posX_V[i] + 10:
				for j in range(1, 9):
					if self.posY_V[j] < mouse[1] < self.posY_V[j] + 56:
						if [i, j] not in self.pos_invalide_murs_v:
							pygame.draw.rect(self.game_display, (255, 175, 175), (self.posX_V[i], self.posY_V[j], 10, 122))
							return (i, j), 'vertical'
		
	def game_loop_1(self):
		""" Single Player Loop """
		winner = None
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quitgame()
				if event.type == pygame.MOUSEBUTTONDOWN:
					try:
						if self.possible_walls():
							self.placer_mur(1, self.possible_walls()[0], self.possible_walls()[1])
							self.jouer_coup(2)
							if self.partie_terminée():
								continue
						elif self.green_circle():
							self.déplacer_jeton(1, self.green_circle())
							self.jouer_coup(2)
							if self.partie_terminée():
								continue
					except QuoridorError:
						if not self.partie_terminée():
							pygame.mixer.Sound.play(self.error_sound)
			if self.partie_terminée():
				winner=self.partie_terminée()

			# Display everything
			if winner:
				self.background()
				self.sound_button(self.sound_off_img, 765, 5, self.music_off)
				self.sound_button(self.sound_on_img, 720, 5, self.music_on)
				self.end_game_menu(winner)
			else:
				self.background()
				self.j1()
				self.j2()
				self.walls()
				self.green_circle()
				self.walls_windows()
				self.possible_walls()
				self.sound_button(self.sound_off_img, 765, 5, self.music_off)
				self.sound_button(self.sound_on_img, 720, 5, self.music_on)
				self.button("MAIN MENU", 690, 470, 100, 50, (0, 191, 255), (72, 118, 255), action=self.back_menu)
				self.button("QUIT", 690, 540, 100, 50, (0, 191, 255), (72, 118, 255), action=self.quitgame)


			pygame.display.update()

		self.clock.tick(60)

	def game_loop_2(self):
		""" Multiplayer Loop """
		winner = None
		player = 1
		while True:
			if player == 1:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.quitgame()
					if event.type == pygame.MOUSEBUTTONDOWN:
						try:
							if self.possible_walls():
								self.placer_mur(1, self.possible_walls()[0], self.possible_walls()[1])
								player = 2
								if self.partie_terminée():
									continue
							elif self.green_circle(1):
								self.déplacer_jeton(1, self.green_circle())
								player = 2
								if self.partie_terminée():
									continue
						except QuoridorError:
							if not self.partie_terminée():
								pygame.mixer.Sound.play(self.error_sound)
			if player == 2:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.quitgame()
					if event.type == pygame.MOUSEBUTTONDOWN:
						try:
							if self.possible_walls():
								self.placer_mur(2, self.possible_walls()[0], self.possible_walls()[1])
								player = 1
								if self.partie_terminée():
									continue
							elif self.green_circle(2):
								self.déplacer_jeton(2, self.green_circle(2))
								player = 1
								if self.partie_terminée():
									continue
						except QuoridorError:
							if not self.partie_terminée():
								pygame.mixer.Sound.play(self.error_sound)
			if self.partie_terminée():
				winner=self.partie_terminée()
			
			# Display everything
			if winner:
				self.background()
				self.sound_button(self.sound_off_img, 765, 5, self.music_off)
				self.sound_button(self.sound_on_img, 720, 5, self.music_on)
				self.end_game_menu(winner)
			else:
				self.background()
				self.j1()
				self.j2()
				self.walls()
				if player == 1:
					self.green_circle(1)
				else:
					self.green_circle(2)
				self.walls_windows()
				self.possible_walls()
				self.sound_button(self.sound_off_img, 765, 5, self.music_off)
				self.sound_button(self.sound_on_img, 720, 5, self.music_on)
				self.button("MAIN MENU", 690, 470, 100, 50, (0, 191, 255), (72, 118, 255), action=self.back_menu)
				self.button("QUIT", 690, 540, 100, 50, (0, 191, 255), (72, 118, 255), action=self.quitgame)
			
			pygame.display.update()

		self.clock.tick(60)



	def j1(self):
		""" Display Player 1 """
		x, y = self.joueurs[0]['pos']
		self.game_display.blit(self.j1_img, (self.posX_j[x] - 28 , self.posY_j[y] - 28 ))

	def j2(self):
		""" Display Player 2 """
		x, y = self.joueurs[1]['pos']
		self.game_display.blit(self.j2_img, (self.posX_j[x] - 28 , self.posY_j[y] - 28 ))

	def background(self):
		""" Display Game Background """
		self.game_display.blit(self.background_img, (0, 0))

	def music_off(self):
		""" Music Off Button """
		pygame.mixer.music.set_volume(0)

	def music_on(self):
		""" Music On Button """
		pygame.mixer.music.set_volume(0.1)
	
	def back_menu(self):
		""" Display Main Menu """
		self.__init__(['1','2'])
	
	def end_game_menu(self, winner):
		""" Game Over Menu """

		pygame.draw.rect(self.game_display, self.black, (self.display_width//3 - 150, self.display_height//3 - 30, 390, 230))
		pygame.draw.rect(self.game_display, self.white, (self.display_width//3 - 140, self.display_height//3 - 20, 370, 210))
		self.button("MAIN MENU", 360, 250, 100, 50, (0, 191, 255), (72, 118, 255), action=self.back_menu)
		self.button("QUIT", 360, 320, 100, 50, (0, 191, 255), (72, 118, 255), action=self.quitgame)

		smallText = pygame.font.Font("freesansbold.ttf", 22)
		textSurf_1, textRect_1 = self.text_object("GAME OVER", smallText, self.black)
		textRect_1.center = (410, 215)
		self.game_display.blit(textSurf_1, textRect_1)


		if winner == 1:
			pygame.draw.rect(self.game_display, self.black, (self.display_width//3 - 130, self.display_height//3 - 10, 190, 190))
			pygame.draw.rect(self.game_display, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) , (self.display_width//3 - 120, self.display_height//3, 170, 170))
			self.game_display.blit(self.j1_face_img, (self.display_width//3 - 120, self.display_height//3))
		else:
			pygame.draw.rect(self.game_display, self.black, (self.display_width//3 - 130, self.display_height//3 - 10, 190, 190))
			pygame.draw.rect(self.game_display, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.display_width//3 - 120, self.display_height//3, 170, 170))
			self.game_display.blit(self.j2_face_img, (self.display_width//3 - 120, self.display_height//3))
