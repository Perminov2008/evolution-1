try:
    from bot import Bot
    import pygame

    match 1:
        case 1:
            print("Все ок")
except ImportError:
    print("Вы долбаеб, ")
except SyntaxError:
    print("У вас не стоит версия питона 3.10, надо скачать ее")


