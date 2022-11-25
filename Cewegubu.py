import account

exit = False

while not(exit):
    command = input("Введите команду\n>>>   ")
    print("")

    if (command == "register") or (command == "reg"):
        account.register()

    elif (command == "login") or (command == "log"):
        account.login()

    elif command == "help":
        account.help()

    elif command == "exit":
        exit = account.exit()

    else:
        account.unknown()
