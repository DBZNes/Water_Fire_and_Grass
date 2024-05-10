import pygame, sys
from network import Network
from button import Menu_button
import pickle

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = get_font(18)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = get_font(20)
        text = font.render("Waiting for Player...", 1, "white", True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        win.fill("#d7fcd4")
        ig_bg = pygame.image.load("assests/ingame.png")
        win.blit(ig_bg, (0, 426))
        font = get_font(20)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

def get_font(size):
    return pygame.font.Font("assests/font.ttf", size)

btns = [Button("Water", 45, 500, "blue"), Button("Fire", 280, 500, "red"), Button("Grass", 500, 500, "green")]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = get_font(50)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, "gold")
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, "black")
            else:
                text = font.render("You Lost...", 1, "red")

            win.blit(text, (width/2 - text.get_width()/2, 100))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    BG = pygame.image.load("assests/menu1.png")
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # win.fill((128, 128, 128))
        win.blit(BG, (0,0))
        font = get_font(30)
        text = font.render("Grass, Fire & Water", 1, "black")
        win.blit(text, (80,200))

        menu_mouse_pos = pygame.mouse.get_pos()

        play_button = Menu_button(image=pygame.image.load("assests/Play Rect.png"), pos=(350, 350),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Menu_button(image=pygame.image.load("assests/Quit Rect.png"), pos=(350, 450),
                             text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        
        for button in [play_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(win)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    run = False
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

    main()

while True:
    menu_screen()