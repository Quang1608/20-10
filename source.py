# Cái này mình làm hơi vội nên một số chỗ thuật toán sẽ khá là ngây thơ với cả nhìn code cũng không được gọn gàng cho lắm,
# một số chỗ mình chú thích bằng tiếng anh vì mình thấy tiện, cộng với việc mình ít tìm hiểu library trong python nên 
# là mình hầu như tự viết các function nên có thể hơi lủng củng, mong mọi người thông cảm nhé thanks

import pygame
import time

pygame.font.init()
pygame.mixer.init()

# Constants
PNGDIR = "pngs//"
FONTDIR = "fonts//"
SOUNDSDIR = "sounds//"
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(FONTDIR + "DejaVuSans-Oblique.ttf", 24)
TIME_PER_FRAME = 0.07

# Pngs
rosep = pygame.image.load(PNGDIR + "rose.png").convert_alpha()
giftp = pygame.image.load(PNGDIR + "gift.png").convert_alpha()
envelopep = pygame.image.load(PNGDIR + "envelope.png").convert_alpha()

small_rosep = pygame.transform.scale(rosep, (128, 128))
small_giftp = pygame.transform.scale(giftp, (450, 450))

# Animation variables
isFading = False
fadeDirection = 1 # 1 - fade in; 2 - fade out
movingObj = None
initPos = (1, 1)
targetPos = (10, 20) # (X, Y)
initDistance = 123
curTransparency = 0

# Main variable
currentstep = 0

# functions, classes
def fromScale(x: float, y: float) -> tuple:
    # Convert scale to pixel
    return (WIDTH * x, HEIGHT * y)

def setFadingObject(obj: object, fadeDir: int, targetPosition: tuple):
    global isFading, fadeDirection, movingObj, initPos, targetPos, curTransparency, initDistance

    isFading = True
    fadeDirection = fadeDir
    movingObj = obj
    initPos = obj.obj_rect.center
    targetPos = targetPosition
    initDistance = ((targetPos[0] - movingObj.obj_rect.center[0])** 2 + (targetPos[1] - movingObj.obj_rect.center[1])** 2)** 0.5 # Pythagoras

    if fadeDir == 1: 
        obj.SetTransparency(0)
        if targetPos == initPos: curTransparency = 0
    elif fadeDir == 2: 
        obj.SetTransparency(255)
        if targetPos == initPos: curTransparency = 255

class Text:
    global FONT

    def __init__(self, text: str, width: int, height: int):
        self.text_box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.text_surface = FONT.render(text, True, (0, 0, 0))  # Render the text
        self.obj_rect = self.text_surface.get_rect()
        self.text_box_surface.blit(self.text_surface, self.obj_rect) # Blit the text onto the text box surface

    def SetTransparency(self, target_t: int):
        self.text_box_surface.set_alpha(target_t)
        pygame.display.update()

    def SetPosition(self, target_x: int, target_y: int):
        SCREEN.fill((255, 255, 255), self.obj_rect) # Delete the previous text

        self.obj_rect.center = (target_x, target_y)
        SCREEN.blit(self.text_box_surface, (self.obj_rect)) # Draw a new one

        pygame.display.update()


class Picture:
    def __init__(self, png):
        self.png = png
        self.obj_rect = png.get_rect()
        self.width, self.height = self.png.get_size()

    def SetTransparency(self, target_t: int):
        self.png.set_alpha(target_t)
        pygame.display.update()

    def SetPosition(self, target_x: int, target_y: int):
        SCREEN.fill((255, 255, 255), self.obj_rect) # Delete the previous image

        self.obj_rect.center = (target_x, target_y)
        SCREEN.blit(self.png, (self.obj_rect)) # Draw a new one

        pygame.display.update()

    """
    def FadeIn(self, target_x, target_y, tweentime):
        frames_count = int(tweentime / (1 / FADE_FPS))
        if frames_count == 0: return

        init_x = self.obj_rect.center[0]
        init_y = self.obj_rect.center[1]

        for i in range(frames_count):
            # Change transparency of each pixel to initial transparency
            self.SetTransparency(int(255 * ((i + 1) / frames_count)))

            # Change position of the image
            self.obj_rect.center = (int(init_x + (target_x - init_x) * ((i + 1) / frames_count)),
                                    int(init_y + (target_y - init_y) * ((i + 1) / frames_count)))
            
            SCREEN.fill((255, 255, 255), self.obj_rect) # Delete the previous image
            SCREEN.blit(self.png, (self.obj_rect)) # Draw a new one
            pygame.display.update()

            time.sleep(1 / FADE_FPS)
    """
# ----------------------------------------------------------------------------------------------------------------------
def main():
    global isFading, fadeDirection, movingObj, initPos, targetPos, currentstep, curTransparency

    run = True

    pygame.display.set_caption("loichuc")
    pygame.display.set_icon(envelopep)

    SCREEN.fill((255, 255, 255))
    pygame.display.update()

    initText = Text("Bật âm lượng để có trải nghiệm tốt nhất", 750, 200)
    initText.SetTransparency(0)
    initText.SetPosition(fromScale(0.5, 0.5)[0], fromScale(0.5, 0.5)[1])

    present = Picture(small_giftp)
    present.SetTransparency(0)
    present.SetPosition(fromScale(0.5, 0.5)[0], fromScale(0.5, 0.5)[1])

    presentText = Text("Nhấn để mở hộp quà", 600, 200)
    presentText.SetTransparency(0)
    presentText.SetPosition(fromScale(0.5, 0.9)[0], fromScale(0.5, 0.9)[1])

    time.sleep(2)

    while run:
        if isFading:
            # This block handles animations
            distance = ((targetPos[0] - movingObj.obj_rect.center[0])** 2 + (targetPos[1] - movingObj.obj_rect.center[1])** 2)** 0.5 # Pythagoras
            isIdle = (targetPos[0] - initPos[0] == 0) and (targetPos[1] - initPos[1] == 0)

            movingObj.SetPosition(movingObj.obj_rect.center[0] + (targetPos[0] - initPos[0]) * 0.02,
                                movingObj.obj_rect.center[1] + (targetPos[1] - initPos[1]) * 0.02)

            # notes:
            # If the object isnt going to stand still then we will change both transparency and position
            # If the object is going to stand still then we change transparency only

            if fadeDirection == 1: # Fade in (increase transparency)
                if isIdle: 
                    curTransparency += 6
                    movingObj.SetTransparency(min(255, curTransparency))
                else: movingObj.SetTransparency(int(255 * ((initDistance - distance) / initDistance)))
            elif fadeDirection == 2: # Fade out (decrease transparency)
                if isIdle:
                    curTransparency -= 6
                    movingObj.SetTransparency(max(0, curTransparency))
                else: movingObj.SetTransparency(int(255 - 255 * (distance / initDistance)))

            if distance < 20 and not isIdle:
                if fadeDirection == 1: movingObj.SetTransparency(255)
                elif fadeDirection == 2: movingObj.SetTransparency(0)

                isFading = False
                movingObj = None
                currentstep += 1
        
            elif isIdle:
                if (fadeDirection == 1 and curTransparency >= 255) or (fadeDirection == 2 and curTransparency <= 0):
                    isFading = False
                    movingObj = None
                    currentstep += 1
            
            time.sleep(TIME_PER_FRAME)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and currentstep == 4:
                setFadingObject(present, 2, fromScale(0.5, 0.5))
                pygame.mixer.music.load(SOUNDSDIR + "sfx.mp3")
                print("loaded")
                pygame.mixer.music.play(0)

        # ...
        # Bat am luong de trai nghiem tot nhat
        if currentstep == 0 and not isFading:
            isFading = True

            setFadingObject(initText, 1, fromScale(0.5, 0.5))

        if currentstep == 1 and not isFading:
            isFading = True

            setFadingObject(initText, 2, fromScale(0.5, 0.5))
        # Hien thi hop qua
        if currentstep == 2 and not isFading:
            isFading = True

            setFadingObject(present, 1, fromScale(0.5, 0.5))
        # Hien thi huong dan mo qua
        if currentstep == 3 and not isFading:
            isFading = True

            setFadingObject(presentText, 1, fromScale(0.5, 0.9))

        # Tat huong dan mo qua
        if currentstep == 5 and not isFading:
            isFading = True

            setFadingObject(presentText, 2, fromScale(0.5, 0.9))
        # Hien thi bong hoa
        if currentstep == 6 and not isFading:
            isFading = True
            rose = Picture(small_rosep)
            rose.SetPosition(fromScale(0.5, 0.35)[0], fromScale(0.5, 0.35)[1])

            setFadingObject(rose, 1, fromScale(0.5, 0.2))
        # Hien thi loi chuc 1
        if currentstep == 7 and not isFading:
            isFading = True

            text1 = Text("Nhân ngày 20/10, mình thay mặt mọi người trong CSC", 750, 200)
            text1.SetPosition(fromScale(0.5, 0.5)[0], fromScale(0.5, 0.5)[1])

            setFadingObject(text1, 1, fromScale(0.5, 0.5))
        # Hien thi loi chuc 2
        if currentstep == 8 and not isFading:
            isFading = True

            text1 = Text("Chúc các bạn nữ 1 ngày 20/10 thật vui vẻ, hạnh phúc", 750, 200)
            text1.SetPosition(fromScale(0.5, 0.55)[0], fromScale(0.5, 0.55)[1])

            setFadingObject(text1, 1, fromScale(0.5, 0.55))
        # Hien thi loi chuc 3
        if currentstep == 9 and not isFading:
            isFading = True

            text1 = Text("và luôn tươi tắn như đóa hoa kia nhé", 750, 200)
            text1.SetPosition(fromScale(0.5, 0.6)[0], fromScale(0.5, 0.6)[1])

            setFadingObject(text1, 1, fromScale(0.5, 0.6))

        # Hien thi loi ket
        if currentstep == 10 and not isFading:
            isFading = True

            text1 = Text("Cảm ơn các bạn đã xem ;-;", 750, 200)
            text1.SetPosition(fromScale(0.5, 0.8)[0], fromScale(0.5, 0.8)[1])

            setFadingObject(text1, 1, fromScale(0.5, 0.8))


    pygame.quit()


if __name__ == "__main__":

    main()