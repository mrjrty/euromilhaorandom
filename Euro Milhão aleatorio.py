# encoding=utf-8

from socket import *
from _thread import *
import pickle, random, time

client = 0
clients = []
vencedora = []
apostas = []
max_connections = 2

def gen_Nums(q, inf, sup):
    num_sol = []

    for i in range(q):
        num=random.randint(inf, sup)
        while num in num_sol:
            num=random.randint(inf, sup)
        num_sol.append(num)

    return num_sol

def chaveVencedora():

    num_sol=gen_Nums(5,1,50)

    est_sol=gen_Nums(2,1,12)

    for i in range(5):
        vencedora.append(num_sol[i])
    for i in range(2):
        vencedora.append(str(est_sol[i]) + "*")



def threaded_client(c, s):
    global client
    pontos = 0

    while 1:
        b_data = s.recv(4096)
        chave = pickle.loads(b_data)
        if not b_data:
            break

        for i in range(7):
            if chave[i] in vencedora:
                pontos += 1

        chave.append(pontos)

        apostas[c].extend(chave)
    s.close()

def main():
    global client
    print(vencedora)
    tcp_s = socket(AF_INET, SOCK_STREAM)
    tcp_s.bind(("127.0.0.1", 1247))
    for i in range(max_connections):
        apostas.append([])

    tcp_s.listen(max_connections)

    try:
        while client < max_connections:
            client_s, client_addr = tcp_s.accept()
            clients.append(client_s)
            print('Connected to: ' + client_addr[0] + ':' + str(client_addr[1]))

            start_new_thread(threaded_client, (client, client_s,))
            client += 1

        print("Verificando se há algum vencedor...")
        time.sleep(40)
        for i in range(max_connections):
            if(apostas[i][7] == 7):
                reply = "Parabéns venceste!"
                clients[i].send(str.encode(reply))
            else:
                reply = "Melhor sorte para a próxima! Acertaste " + str(apostas[i][7]) + " números."
                clients[i].send(str.encode(reply))



    except KeyboardInterrupt:
        tcp_s.close()

    tcp_s.close()


chaveVencedora()
main()
