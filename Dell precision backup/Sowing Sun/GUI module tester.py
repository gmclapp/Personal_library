import pygame
import sys
import CommonGUIElements as GUI
pygame.init()

screen = pygame.display.set_mode((512,512))
pygame.display.set_caption('Button Module')

fpsClock = pygame.time.Clock()

Red=pygame.Color(255,0,0)
Blue=pygame.Color(0,0,255)
Green=pygame.Color(0,255,0)
White=pygame.Color(255,255,255)
Black=pygame.Color(0,0,0)
        
test_Button = GUI.Button(screen, x=0, y=40)
test_Button2 = GUI.Button(screen, x=0, y=300, label = 'Button')

disp_message = GUI.screen_message(screen, 'Hello world!', 10, 10, White, Red)

Buttons = [test_Button, test_Button2]

while True:
    screen.fill(Black)
    #test_Button.y += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass
            #KEYS
        if event.type == pygame.KEYUP:
            pass
            #KEYS
        if event.type == pygame.MOUSEMOTION:
            for button in Buttons:
                button.button_status(event.pos[0], event.pos[1])
            #COORDS (POS, REL, BUTTONS)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in Buttons:
                    print(button.label, ': ', button.button_status(event.pos[0], event.pos[1], release = 1))
            #(POS, BUTTON)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in Buttons:
                    print(button.label, ': ', button.button_status(event.pos[0], event.pos[1], click = 1))
            #(POS, BUTTON)
            
        if event.type == pygame.QUIT:
            pass
            pygame.quit(); sys.exit();
        #print(str(event))

    
    test_Button.draw_button()
    test_Button2.draw_button()
    disp_message.draw()
    pygame.display.update()
    fpsClock.tick(60)

