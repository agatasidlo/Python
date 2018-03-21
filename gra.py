import pygame
import random

pygame.init()

moleInHole = 9 * [False] # od 0 do 9
moleInHoleNotTab = 15 # od 1 do 10
holeInfo = 9 * [0, 0] # od 0 do 9

moleTime = 1000

x1 = 30
y1 = 70
o = 20
r = 120

points = 0
highScore = 0

chance = 5

width = 800
height = 600

red = (200,0,0)
green = (0,200,0)
 
mole_width = 73

nrOfMoles = 1

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Whac-a-mole')
clock = pygame.time.Clock()
 
moleImg = pygame.image.load('mole.jpg')
gameIcon = pygame.image.load('mole.jpg')

pygame.display.set_icon(gameIcon)

pause = False
endOfGame = False
wantQuit = False
 
def point (score):
	global highScore
	global chance
	gameDisplay.fill(pygame.Color("white"), (x1, 20, 190, 45))
	font = pygame.font.SysFont("comicsansms", y1-20)
	text = font.render("Points: "+str(score), True, pygame.Color("green"))
	gameDisplay.blit(text, (x1,20))

	gameDisplay.fill(pygame.Color("white"), (x1+1.5*r+2*o, 20, 190, 45))
	font = pygame.font.SysFont("comicsansms", y1-20)
	text = font.render("Chances: "+str(chance), True, pygame.Color("green"))
	gameDisplay.blit(text, (x1+1.5*r+2*o,20))
	
	gameDisplay.fill(pygame.Color("black"), (140, 3*r+3*o+y1+10, 250, 45))
	text = font.render("Best score: "+str(highScore), True, pygame.Color("orange"))
	gameDisplay.blit(text, (140, 3*r+3*o+y1+10))

def hole (holeX, holeY, holeW, holeH, color):
	pygame.draw.rect(gameDisplay, color, [holeX, holeY, holeW, holeH])

def text_objects (text, font):
	textSurface = font.render(text, True, pygame.Color("black"))
	return textSurface, textSurface.get_rect()

def button (textOnButton,x,y,w,h,ic,ac,action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action ()
	else:
		pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
	smallText = pygame.font.SysFont("Arial",20)
	textSurf, textRect = text_objects(textOnButton, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)

def quitgame ():
	global wantQuit
	wantQuit = False
	pygame.quit()
	quit()

def notQuit ():
	global moleInHole
	global wantQuit
	wantQuit = False
	gameDisplay.fill(pygame.Color("white"), (width/2, height/2, 400, 300))
	moleInHole = 9 * [False]
	screenInit ()
	hole (x1+(r+o), y1+(r+o)*2, r, r, pygame.Color("purple"))
	hello (15)

def wantToQuit ():
	global wantQuit
	wantQuit = True
	gameDisplay.fill(pygame.Color("white"))
	font = pygame.font.SysFont("comicsansms", 100)
	text = font.render("Are you sure", True, pygame.Color("red"))
	gameDisplay.blit(text, (100, height/6))
	text2 = font.render("you want to quit?", True, pygame.Color("red"))
	gameDisplay.blit(text2, (120, height/6+100))
	while wantQuit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		button("Yes", 150, 300, 100, 50, red, pygame.Color("pink"), quitgame)
		button("No", 150, 400, 100, 50, green, red, notQuit)

		pygame.display.update()
		clock.tick(15)

def hello (numberOfHole): # od 0 do 9
	global moleInHole
	global start
	global moleInHoleNotTab

	holeNr = random.randrange(9)+1	

	if numberOfHole != 15:
		if moleInHole[holeNr-1] == True:
			while moleInHole[holeNr-1]:
				holeNr = random.randrange(9)+1

	moleInHole[holeNr-1] = True
	if numberOfHole != 15:
		moleInHole[numberOfHole] = False
	
	moleInHoleNotTab = holeNr
	x = holeInfo[holeNr-1][0]+r/2-20
	y = holeInfo[holeNr-1][1]+r/2-24
	
	for i in range (1, nrOfMoles+1):
		gameDisplay.blit(moleImg,(x,y))

	start = pygame.time.get_ticks()

	for event in pygame.event.get ():
		if event.type == pygame.QUIT:
			wantToQuit ()

def screenInit ():
	global holeInfo
	gameDisplay.fill(pygame.Color("white"))
	for a in range (1, 4):
		for b in range (1, 4):
			holeInfo[(b + (a-1)*3)-1] = [x1+(r+o)*(b-1), y1+(r+o)*(a-1)]
			hole (x1+(r+o)*(b-1), y1+(r+o)*(a-1), r, r, pygame.Color("purple"))

def newGame ():
	global points
	global highScore
	global chance
	global moleTime
	global endOfGame
	global moleInHole
	moleTime = 1000
	if points > highScore:
		highScore = points
	points = 0
	chance = 5
	endOfGame = False
	screenInit ()
	moleInHole = 9 * [False]
	hello (moleInHoleNotTab-1)

def pausee ():
	global pause
	if not pause:
		pause = True
	else:
		pause = False
	pauseText ()

def pauseText ():
	if pause:
		text = pygame.font.SysFont("Arial",115)
		TextSur, TextRec = text_objects("Paused", text)
		TextRec.center = ((x1+1.5*r+o),(height/2))
		gameDisplay.blit(TextSur, TextRec)
		moleInHole = 9 * [False]
	else:
		screenInit ()
		hello (15)

def gameOver ():
	global endOfGame
	global highScore
	global points
	endOfGame = True
	if points > highScore:
		highScore = points
	point (points)
	text = pygame.font.SysFont("Arial",70)
	TextSur, TextRec = text_objects("Game Over", text)
	TextRec.center = ((x1+1.5*r+o),(height/2))
	gameDisplay.blit(TextSur, TextRec)

def menu ():
	button ("New Game", ((width-3*r-x1-2*o)/2 + x1 + 3*r + 2*o - 50), 150, 100, 50, pygame.Color("red"), pygame.Color("pink"), newGame)
	button ("Pause", ((width-3*r-x1-2*o)/2 + x1 + 3*r + 2*o - 50), 250, 100, 50, pygame.Color("red"), pygame.Color("pink"), pausee)
	button ("Quit", ((width-3*r-x1-2*o)/2 + x1 + 3*r + 2*o - 50), 350, 100, 50, red, green, wantToQuit)
	pygame.display.update()
	clock.tick(15)

def game_loop():
	global pause
	global points
	global moleInHole
	global start
	global moleTime
	global endOfGame
	global chance
	
	pointsChange = 5

	x = (width * 0.45)
	y = (height * 0.8)

	gameExit = False
	
	screenInit ()
	hello (15)
	while not gameExit:
		menu ()
		if points >= pointsChange:
			pointsChange += 5
			moleTime -= 150
		if chance <= 0:
			gameOver ()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				wantToQuit ()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pausee ()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse = pygame.mouse.get_pos()
				if not pause and not endOfGame:
					for i in range (1, 10):
						if holeInfo[i-1][0] < mouse[0] < (holeInfo[i-1][0]+r) and holeInfo[i-1][1] < mouse[1] < (holeInfo[i-1][1]+r):
							if moleInHole[i-1] == True:
								gameDisplay.fill(pygame.Color("purple"), (holeInfo[i-1][0],holeInfo[i-1][1],r,r))
								points += 1
								hello (i-1)

		point (points)

		if not pause and not endOfGame:
			end = pygame.time.get_ticks()
			if end-start > moleTime:
				chance -= 1
				screenInit ()
				hello (moleInHoleNotTab-1)

game_loop ()
pygame.quit()
quit()
