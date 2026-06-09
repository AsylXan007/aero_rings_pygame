import pygame
import random
pygame.init()

#setup game
pygame.display.set_caption('Aero rings')
pygame.display.set_icon(pygame.image.load("Aero_rings/img/planeStill.png"))
background = pygame.image.load("Aero_rings/img/eveningSkyBG.png")
size = (1280,720)
background = pygame.transform.scale(background, size)
screen = pygame.display.set_mode(size)
running = True
frame_count = 0
podbor = 0
bot=False
loopdist = 0
clickTiming = 0 

clock = pygame.time.Clock()


#Buttons
pauseButton = pygame.image.load("Aero_rings/img/pause.png")
continueButton = pygame.image.load("Aero_rings/img/continue.png")
musicOn = pygame.image.load("Aero_rings/img/musicOn.png")
musicOff = pygame.image.load("Aero_rings/img/musicOff.png")
pauseButton = pygame.transform.scale(pauseButton, (80,80))
continueButton = pygame.transform.scale(continueButton, (80,80))
musicOn = pygame.transform.scale(musicOn, (80,80))
musicOff = pygame.transform.scale(musicOff, (80,80))
button1 = pauseButton
button1_rect = button1.get_rect()
button2 = musicOn
button2_rect = button2.get_rect()

b2click = 0
paused = 0

#button coordinates
b1x, b1y, b2x, b2y = [],[],[],[]
for i in range(10,90):
    b1x.append(i)
    b1y.append(i)
    b2y.append(i)
for i in range(110,190):
    b2x.append(i)


#moving background
scroll = 0
panels = 3 #middle + left and right ones


#pictures for animation
planeStill = pygame.image.load("Aero_rings/img/planeStill.png")
planeStill = pygame.transform.scale(planeStill, (172,56))
planeUp = pygame.image.load("Aero_rings/img/planeUp.png")
planeUp = pygame.transform.scale(planeUp, (172,64))
planeDown = pygame.image.load("Aero_rings/img/planeDown.png")
planeDown = pygame.transform.scale(planeDown, (172,72))
plane = planeStill
plane_rect = plane.get_rect()
x, y = 150, 300
plane_rect[0], plane_rect[1] = x, y

ring = pygame.image.load("Aero_rings/img/pointRing.png")
ring = pygame.transform.scale(ring, (90,200)) 
ring_rect = ring.get_rect()
ring_rect.x,ring_rect.y = random.randrange(1300,1500),random.randrange(150,450)

points = 0


font = pygame.font.SysFont("calibri", 36)
font_big = pygame.font.SysFont("calibri",90)
pause_text = font_big.render(f"GAME PAUSED", True, (255,255,255))
to_unpause_text = font.render("Click anywhere to unpause the game",True, (255,255,255))

#music and sounds
pygame.mixer.music.load("Aero_rings/aud/Cipher-KevinMacleod.mp3")
pygame.mixer.music.play(-1)
ringsound = pygame.mixer.Sound("Aero_rings/aud/RingCollect.mp3")
sounds = 1
music = 1


screen.blit(background, (0, 0))
pygame.display.flip()

while running:
    if not paused: #game running
        frame_count += 1
        if frame_count == 30:
            frame_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousebutton = 1

        
        for i in range(panels):
            screen.blit(background, (i * size[0] + scroll - size[0], 0))
        
        #also moving background
        scroll-=1
        if abs(scroll)>size[0]: #for scroll exceeding bg border
            scroll = 0 

        #Plane Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and plane_rect.y > 0 and not bot:
            plane = planeUp
            plane_rect.y -= 4
        elif keys[pygame.K_s] and plane_rect.y < 650 and not bot:
            plane = planeDown
            plane_rect.y += 4
        elif keys[pygame.K_d] and plane_rect.x < 1100 and not bot:
            plane = planeStill
            plane_rect.x +=5
        elif keys[pygame.K_a] and plane_rect.x > 0 and not bot:
            plane = planeStill
            plane_rect.x -= 3

        elif keys[pygame.K_b] and not bot and clickTiming == 0:
            bot = True
            clickTiming = 12
        elif keys[pygame.K_b] and bot and clickTiming == 0:
            bot = False
            clickTiming = 12
    
        else:
            plane = planeStill


        if clickTiming > 0:
            clickTiming-=1
        #bot
        if plane_rect.x < 800 and bot:
            plane_rect.x+=5
        if bot:
            loopdist = (ring_rect.y+55 - plane_rect.y) // 4
        
        if loopdist>0 and bot:
            plane_rect.y +=4
        elif loopdist<0 and bot:
            plane_rect.y -=4

        

        #ring collection
        ring_rect.x -= 5
        if ring_rect.x < 0:
            ring_rect.x,ring_rect.y = random.randrange(1300,1500),random.randrange(150,450)
        if plane_rect.colliderect(ring_rect):
            podbor +=1
        if podbor == 6:
            points += 1
            if sounds == 1:
                ringsound.play()
            ring_rect.x,ring_rect.y = random.randrange(1300,1500),random.randrange(150,450)
            podbor = 0

        #buttons
        mx, my= pygame.mouse.get_pos() 
        if mx in b1x and my in b1y and mousebutton: #pause
            mousebutton = 0
            button1 = continueButton
            paused = 1
        if mx in b2x and my in b2y and mousebutton and music: #musicOff
            mousebutton = 0
            music = 0
            button2 = musicOff
            pygame.mixer.music.pause()
            sounds = sounds * -1
        if mx in b2x and my in b2y and mousebutton and not music: #musicOn
            mousebutton = 0
            music = 1
            button2 = musicOn
            pygame.mixer.music.unpause()
            sounds = sounds * -1
        

        screen.blit(background, (size[0],size[0]))
        screen.blit(ring, (ring_rect.x, ring_rect.y))
        screen.blit(plane, (plane_rect.x, plane_rect.y))
        screen.blit(button1, (10,10))
        screen.blit(button2, (110,10))

        Score = font.render(f"Points: {points}", True, (1,1,1))
        screen.blit(Score, (200,15)) 

    elif paused: #while game is paused (no motion, only checking if buttons are clicked)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousebutton = 1 
        screen.blit(background, (size[0],size[0]))
        screen.blit(ring, (ring_rect.x, ring_rect.y))
        screen.blit(plane, (plane_rect.x, plane_rect.y))
        screen.blit(button1, (10,10))
        screen.blit(button2, (110,10))
        screen.blit(Score, (200,15))
        screen.blit(pause_text, (400,320))
        screen.blit(to_unpause_text, (400,400))
        if mx in b1x and my in b1y and mousebutton: #unpause
            mousebutton = 0
            button1 = pauseButton
            paused = 0
        if mx in b2x and my in b2y and mousebutton and music: #musicOff
            mousebutton = 0
            music = 0
            button2 = musicOff
            pygame.mixer.music.pause()
            sounds = sounds * -1
        if mx in b2x and my in b2y and mousebutton and not music: #musicOn
            mousebutton = 0
            music = 1
            button2 = musicOn
            pygame.mixer.music.unpause()
            sounds = sounds * -1

    pygame.display.flip()
    clock.tick(30)
    mousebutton = 0 #refresh click variable
pygame.quit()