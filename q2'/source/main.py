import client
import server
import time
from multiprocessing import Process

if __name__ == "__main__":
    S = input('输入服务器线程数：(如为0则自动从1-5)')
    C = input('输入客户端线程数：(如为0则自动从1-5)')
    Server = Process(target=server.serverMain, args=(int(S),))
    Client = Process(target=client.clientMain, args=(int(C),))
    Server.Daemon = True
    Client.Daemon = True
    Server.start()
    time.sleep(1)
    Client.start()
    Server.join()
    Client.join()