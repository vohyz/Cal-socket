import client
import server
import time
from multiprocessing import Process

if __name__ == "__main__":
    Server = Process(target=server.serverMain)
    Client = Process(target=client.clientMain)
    Server.Daemon = True
    Client.Daemon = True
    Server.start()
    time.sleep(1)
    Client.start()
    Server.join()
    Client.join()