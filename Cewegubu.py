import account
import server
from threading import Thread

exit = False

def gameBody():
    while not(exit):
        command = input("Введите команду\n>>>\t")
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

def serverListener():
    server.

th1 = Thread(target=gameBody, args=())
th2 = Thread(target=server.serverAnswer, args=())

th1.start()
th2.start()
