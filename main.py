import random
import time
from enum import Enum
from input_handler import InputHandler
import sys

__name__ = "__test__"


class DiskSchedulingAlgorithm (Enum):
    SCAN = 1
    CSCAN = 2


# noinspection PyShadowingNames
def SCAN(nblocks, visit_requests: list[int], initial_head_position):
    order: list[int] = []
    seek_time = 0

    if initial_head_position < nblocks//2:  # Cabeça de leitura está mais a esquerda

        for head_position in range(initial_head_position, -1, -1):  # Leitura da posição inicial até a extrema esquerda
            seek_time += 1
            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

        seek_time += initial_head_position + 1  # Simulação da cabeça voltando da extrema esquerda para a posição inicial

        for head_position in range((initial_head_position + 1), nblocks):  # Leitura de posição a direita da posição inicial até a extrema direita
            seek_time += 1
            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

    else:  # Cabeça de leitura está mais a direita ou no meio

        for head_position in range(initial_head_position, nblocks):  # Leitura da posição inicial até a extrema direita
            seek_time += 1
            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

        seek_time += initial_head_position + 1  # Simulação da cabeça voltando da extrema direita para a posição inicial

        for head_position in range(initial_head_position - 1, -1, -1):  # Leitura da posição a esquerda da posição inicial até a extrema esquerda
            seek_time += 1
            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

    return order, seek_time


# noinspection PyShadowingNames
def CSCAN(nblocks, visit_requests: list[int], initial_head_position):
    order: list[int] = []
    seek_time = 0

    if initial_head_position < nblocks//2:  # Cabeça de leitura está mais a esquerda
        for head_position in range(initial_head_position, -1, -1):  # Leitura da posição inicial até a extrema esquerda
            seek_time += 1

            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

        for head_position in range(nblocks - 1, initial_head_position + 2, -1):  # Leitura da extrema direita até uma posição a direita da posição inicial
            seek_time += 1

            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

    else:  # Cabeça de leitura está mais a direita ou no meio
        for head_position in range(initial_head_position, nblocks):  # Leitura da posição inicial até a extrema direita.
            seek_time += 1

            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

        for head_position in range(0, initial_head_position - 2):  # Leitura da extrema esquerda até uma posição a esquerda da posição inicial.
            seek_time += 1

            if head_position in visit_requests:
                order.append(head_position)
                visit_requests.remove(head_position)

                if len(visit_requests) == 0:
                    return order, seek_time

    return order, seek_time


if __name__ == "__main__":
    print("Gerenciamento de E/S - WINTERMUTE XXIII \n")
    nblocks = InputHandler.int_input("Informe a quantidade de blocos em disco: ", (0, sys.maxsize))
    nvisits = InputHandler.int_input("Informe a quantidade de blocos a serem visitados: ", (0, nblocks))

    print()
    print(f'Os blocos em disco foram enumerados de 0 até {nblocks}.')
    time.sleep(3)

    visit_requests = random.sample(list(range(nblocks)), k=nvisits)
    print()
    print("Ordem randômica dos blocos a serem visitados: " + str(visit_requests))
    time.sleep(3)

    disk_head_position = random.choice(list(range(nblocks)))
    print()
    print(f'A cabeça de leitura do disco encontra-se na posição {disk_head_position}')
    time.sleep(3)

    print()
    print("1 - SCAN")
    print("2 - CSCAN")
    algorithm = DiskSchedulingAlgorithm(InputHandler.int_input("Escolha o algoritmo de escalonamento de disco: ", (1, 2)))

    actual_visit_order = []

    if algorithm.SCAN:
        actual_visit_order = SCAN(nblocks, visit_requests, disk_head_position)
    elif algorithm.CSCAN:
        actual_visit_order = CSCAN(nblocks, visit_requests, disk_head_position)

    print("Ordem real dos blocos visitados: " + str(actual_visit_order[0]))
    print("Seek time: " + str(actual_visit_order[1]))


if __name__ == "__test__":  # TESTES
    nblocks = 100
    nrequests = 10
    ntests = 10000

    seek_time: tuple[list[int], list[int]] = ([], [])

    for _ in range(0, ntests):
        visit_requests = random.sample(list(range(nblocks)), k=nrequests)
        disk_head_position = random.choice(list(range(nblocks)))

        print(f'visit_requests: {visit_requests}')
        print(f'disk_head_position: {disk_head_position}')

        scan = SCAN(nblocks, visit_requests.copy(), disk_head_position)
        print(f'SCAN: {scan}')
        seek_time[0].append(scan[1])

        cscan = CSCAN(nblocks, visit_requests.copy(), disk_head_position)
        print(f'CSCAN: {cscan}')
        seek_time[1].append(cscan[1])

        print()

    print("Considerando um seek time constante para cada bloco visitado, ")
    print(f'o seek time do CSCAN é em média {round(((sum(seek_time[1])/sum(seek_time[0])) * 100), 3)}% do seek time do SCAN.')
