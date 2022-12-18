import server
import re


def end():
    print("\n" + "-" * 100 + "\n")


def langTest(word, lenMin=-1, lenMax=999999999):
    word = word.lower()
    len = len(word)

    if len <= lenMin or len >= lenMax:
        return 0

    if re.search(r'[^a-z_0-9]+', word) != None:
        return 0

    return 1

def register():
    print("Вы успешно зарегестрировались")
    end()


def login():
    print("Вы успешно вошли в аккаунт")
    end()


def help():
    print("Тут список всех команд")
    end()


def exit():
    print("Игра овер")
    end()
    return True


def unknown():
    print("Такой команды не существует, используйте help")
    end()
