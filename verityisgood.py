from PIL import Image, ImageGrab, ImageDraw
from pydirectinput import press, moveTo, click
from pygetwindow import getWindowsWithTitle
from time import sleep, time
from sys import exit
from os import startfile


def press_sleep(k, _d):
    press(k)
    sleep(_d)


def comp_pixel(p, ps, _t):  # сравнение двух пикселей в абсолюте
    return abs(p[0] - ps[0]) < _t and abs(p[1] - ps[1]) < _t and abs(p[2] - ps[2]) < _t


def find_first_whitepix(im):  # хелп функция для определения границ экрана
    for i in range(w // 2):
        for j in range(h // 2):
            if comp_pixel(im.getpixel((i, h - j - 1)), (255, 255, 255), 100):
                return i, j
    return 0, 0


def screen_person():  # скрин игрока
    img_screen = ImageGrab.grab()
    img_name = img_screen.crop((255 * dY + x_edge, 35 * dX * dXgame / dYgame + y_edge, 925 * dY + x_edge,
                                85 * dX * dXgame / dYgame + y_edge))
    img_screen = img_screen.crop(
        ((1280 - 256) * dY + dXframe, 0, (1280 + 256) * dY + dXframe, 2560 * dX * dXgame / dYgame))
    img_name = img_name.resize((img_screen.width, int(img_screen.width / img_name.width * img_name.height)))
    img_screen = img_screen.crop((0, 125 * dX * dXgame / dYgame - img_name.height + y_edge, img_screen.width,
                                  720 * dX * dXgame / dYgame + + y_edge))
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


def wtf2(p1, p2, dt):  # странно, но это снова работает
    for i in range(3):
        for j in range(3):
            if not comp_pixel(p1.getpixel((24 * j, 24 * i)), p2.getpixel((24 * j, 24 * i)), dt):
                return False
    return True


# считывание настроек
print("Developed by LaiQ v3.7\n")
try:
    settings = open('Settings.txt', 'r')
    key_f1 = settings.readline()[11:-1]
    key_u = settings.readline()[9:-1]
    lang = settings.readline()[10:-1]
    delay = float(settings.readline()[7:])
except FileNotFoundError:
    key_f1 = 'f1'
    key_u = 'u'
    lang = 'ru'
    delay = 0.5
    settings = open('Settings.txt', 'w')
    settings.write(f'Character: {key_f1}\n')
    settings.write(f'Friends: {key_u}\n')
    settings.write(f'Language: {lang}\n')
    settings.write(f'Delay: {delay}')
settings.close()

# поиск окна
destiny = getWindowsWithTitle('')[0]
for _t in getWindowsWithTitle('Destiny 2'):
    if _t.title == 'Destiny 2':  # идиотский поиск окна на разработчиках
        destiny = _t
        w, h = destiny.size
        break
if destiny.title == 'Destiny 2':
    w, h = destiny.size
else:
    if lang == "ru":
        print('Destiny 2 не запущена\n')
    else:
        print('Destiny 2 is not running\n')
    exit(0)

dX, dY = w / 2560, h / 1440  # коэффициент разрешений
try:
    screen_bounds = open('ScreenBounds.txt', 'r')
    w_game, h_game = [int(x) for x in screen_bounds.readline()[12:].split('x')]
    x_edge, y_edge = [int(x) for x in screen_bounds.readline()[15:].split()]
    dXframe, dYframe = max((w_game - h_game * 16 / 9) / 2, 0), max((h_game - w_game * 9 / 16) / 2, 0)
    dXgame, dYgame = w_game / w, h_game / h
    screen_bounds.close()
except FileNotFoundError:
    if lang == "ru":
        print("Программа должна настроить границы экрана")
    else:
        print("The program should adjust the screen bounds")
    if lang == "ru":
        print("Введите ваше разрешение в игре\n")
        w_game = int(input("Ширина: "))
        h_game = int(input("Высота: "))
    else:
        print("Enter your resolution in the game\n")
        w_game = int(input("Width: "))
        h_game = int(input("Height: "))
    dXgame, dYgame = w_game / w, h_game / h
    dXframe, dYframe = max((w_game - h_game * 16 / 9) / 2, 0), max((h_game - w_game * 9 / 16) / 2, 0)
    destiny.minimize()
    destiny.maximize()
    press_sleep('esc', 0)
    press_sleep('esc', 0)
    press_sleep(key_f1, delay)
    press_sleep('d', delay)
    press_sleep('d', delay)
    press_sleep('s', 0)
    press_sleep('s', 0)
    moveTo(int(2167 * dX * dXgame + dXframe), int(747 * dY * dYgame))
    click(button='left')
    sleep(delay)
    x_edge, y_edge = find_first_whitepix(ImageGrab.grab())
    press_sleep('esc', 0)
    press_sleep('esc', 0)
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
press_sleep('esc', 0)
press_sleep('esc', 0)
press_sleep(key_u, 2 * delay)
x = int(570 * dY + dXframe)
leader = -1
for playerNumber in lst:
    y = int((369 + 75 * playerNumber) * dY * dXgame / dYgame + dYframe)  # костыль, я не вывел формулу
    moveTo(int(x * dXgame), int(y * max(dXgame, dYgame)))
    pix1 = pix2 = ImageGrab.grab(bbox=(0, h // 2, 50, h // 2 + 50))
    t = 0
    while wtf2(pix1, pix2, 25) and t < delay - 0.01:  # ждём клик
        click(button='right')
        pix1 = pix2
        pix2 = ImageGrab.grab(bbox=(0, h // 2, 50, h // 2 + 50))
        sleep(0.1)
        t += 0.1
    if t >= delay - 0.01:  # если от клика нет результата - заходим на себя
        if leader != -1:  # попали на пустой слот
            break
        leader = playerNumber
        press_sleep(key_f1, delay)
    while wtf(ImageGrab.grab()):  # ждём прогрузку персонажа
        sleep(0.25)
    sleep(delay / 2)
    img = screen_person()
    if playerNumber != leader:
        press_sleep('esc', delay)
    else:
        press_sleep(key_u, 2 * delay)
    res = res.resize((img.width * 3, img.height * 2))
    res.paste(img, (playerNumber % 3 * img.width, playerNumber // 3 * img.height))
press('esc')

# вотермарк
d = ImageDraw.Draw(res)
d.text(xy=(res.width - 290 * dY, res.height - 35 * dY), text="Developed by LaiQ v3.7", fill="red",
       font_size=round(26 * dY))
res.save("Players.png")
startfile("Players.png")
