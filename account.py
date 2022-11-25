import server

def end():
    print("\n" + "-" * 100 + "\n")

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