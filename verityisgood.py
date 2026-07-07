from PIL import Image
from pyautogui import screenshot, size
from pydirectinput import press, leftClick, moveTo, rightClick
from pygetwindow import getWindowsWithTitle
from time import sleep
from sys import exit
from os import startfile

def press05(k):
    press(k)
    sleep(0.5)

def comp_pixel(p, ps, t):  # сравнение двух пикселей в абсолюте
    return abs(p[0] - ps[0]) < t and abs(p[1] - ps[1]) < t and abs(p[2] - ps[2]) < t


def find_first_whitepix(im):  # хелп функция для определения границ экрана
    for i in range(w // 2):
        for j in range(h // 2):
            if comp_pixel(im.getpixel((i, h - j - 1)), (255, 255, 255), 100):
                return i, j
    return 0, 0


def screen_person():  # скрин игрока
    img_screen = screenshot()
    img_name = img_screen.crop((256 * dY + x_edge, 35 * dY + y_edge, 925 * dY + x_edge, 80 * dY + y_edge))
    img_screen = img_screen.crop(((1280 - 256) * dY + dXframe, 0, (1280 + 256) * dY + dXframe, 2560 * dY))
    img_name = img_name.resize((img_screen.width, int(img_screen.width / img_name.width * img_name.height)))
    img_screen = img_screen.crop((0, 125 * dY - img_name.height + y_edge, img_screen.width, 720 * dY))
    img_screen.paste(img_name)
    return img_screen


def wtf(im):  # странно, но оно работает
    tx, ty = (w - dXframe * 2) // 30, h // 20
    center = im.getpixel((w // 2, h // 2 + ty * 3))  # костыль, чтобы не попасть на мышку
    for i in range(5):
        for j in range(5):
            if (not comp_pixel(im.getpixel((w // 2 + tx * (j - 2), h // 2 + ty * (i - 2))), center, 25)
                    and i != 2 and j != 2):  # костыль, чтобы не попасть на мышку
                return False
                # центральный пиксель не похож на соседние
    return True  # анлак


def wtf2(p1, p2):  # странно, но это снова работает
    _x, _y = 0, 0
    for i in range(5):
        for j in range(5):
            if not comp_pixel(p1.getpixel((_x + 20 * j, _y + 20 * i)), p2.getpixel((_x + 20 * j, _y + 20 * i)), 1):
                return False

    return True


#считывание настроек
print("Developed by LaiQ\n")
try:
    settings = open('Settings.txt', 'r')
    key_f1 = settings.readline()[11:-1]
    key_u = settings.readline()[9:-1]
    lang = settings.readline()[10:]
except FileNotFoundError:
    settings = open('Settings.txt', 'w')
    settings.write("Inventory: f1\n")
    key_f1 = "f1"
    key_u = "u"
    lang = "ru"
    settings.write("Friends: u\n")
    settings.write("Language: ru")
settings.close()
try:
    destiny = getWindowsWithTitle('Destiny 2')[0]
except IndexError:
    if lang == "ru":
        print('Destiny 2 не запущена\n')
    else:
        print('Destiny 2 is not running\n')
    exit(0)
w, h = size()
try:
    screen_bounds = open('ScreenBounds.txt', 'r')
    w_game, h_game = [int(x) for x in screen_bounds.readline()[12:].split('x')]
    x_edge, y_edge = [int(x) for x in screen_bounds.readline()[15:].split()]
    dY, dXframe = h / 1440, (w - h * 16 / 9) / 2  # коэффициент разрешений и ширина рамок
    screen_bounds.close()
except FileNotFoundError:
    if lang == "ru":
        print("Введите ваше разрешение в игре\n")
        w_game = int(input("Ширина: "))
        h_game = int(input("Длина: "))
    else:
        print("Enter your resolution in the game\n")
        w_game = int(input("Width: "))
        h_game = int(input("Height: "))

    if lang == "ru":
        print("Программа должна настроить границы экрана")
    else:
        print("The program should adjust the screen bounds")
    destiny.minimize()
    destiny.maximize()
    sleep(1)
    press05('esc')
    press05(key_f1)
    sleep(0.5)
    press05('d')
    press05('d')
    press05('s')
    press05('s')
    dY, dXframe = h / 1440, (w - h * 16 / 9) / 2  # коэффициент разрешений и ширина рамок
    moveTo(int((2167 * dY + dXframe)*w_game/w), int(747 * dY * h_game/h))
    sleep(0.5)
    leftClick()
    sleep(0.5)
    x_edge, y_edge = find_first_whitepix(screenshot())
    press05('esc')
    press05('esc')
    if lang == "ru":
        print('Перезапустите программу')
    else:
        print("Restart the program")
    screen_bounds = open('ScreenBounds.txt', 'w')
    screen_bounds.write(f"Resolution: {w_game}x{h_game}\n")
    screen_bounds.write(f"Screen Bounds: {x_edge} {y_edge}")
    screen_bounds.close()
    input("Press any key to exit...")
    exit(0)


if lang == "ru":
    mes = ("Введите номера игроков, которых надо сфотографировать\n"
           "Если надо сфотографировать всю команду, введите 0\n")
else:
    mes = ("Enter the numbers of the players you want to photograph\n"
           "If you want to take a photo of the entire team, enter 0\n")
lst = list(map(lambda x: int(x) - 1, input(mes).split()))

try:
    res = Image.open("Players.png")
except FileNotFoundError:
    res = Image.new(mode="RGB", size=(1280, 720), color="black")  # если файла нет, создадим пустое фото
if lst[0] == -1:
    res = Image.new(mode="RGB", size=(1280, 720), color="black")
    lst = [0, 1, 2, 3, 4, 5]

destiny.minimize()
destiny.maximize()
x = int(570 * dY + dXframe)
press05('esc')
press05(key_u)
sleep(0.5)
leader = -1
for playerNumber in lst:
    y = int((369 + 75 * playerNumber) * dY)
    moveTo(int(x * w_game/w), int(y*h_game/h))
    sleep(0.5)
    pix1 = screenshot().crop((x + 100, y + 100, x + 200, y + 200))
    rightClick()
    sleep(0.5)
    pix2 = screenshot().crop((x + 100, y + 100, x + 200, y + 200))
    if wtf2(pix1, pix2):  # если от клика нет результата - заходим на себя
        if leader!= -1: # попали на пустой слот
            break
        leader = playerNumber
        press05(key_f1)
    while wtf(screenshot()):  # ждём прогрузку персонажа
        sleep(0.1)
    sleep(0.25)
    img = screen_person()
    if playerNumber != leader:
        press05('esc')
    else:
        press05(key_u)
        sleep(0.5)
    res = res.resize((img.width * 3, img.height * 2))
    res.paste(img, (playerNumber % 3 * img.width, playerNumber // 3 * img.height))
press('esc')
res.save("Players.png")
startfile("Players.png")
input("Press any key to exit...")