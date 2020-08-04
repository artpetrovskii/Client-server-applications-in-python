import subprocess


processes = []

while True:
    actions = input('Выберите действие: e - выход, '
                    's - запустить сервер и клиенты, '
                    'c - закрыть все окна: ')

    if actions == 'e':
        break
    elif actions == 's':
        processes.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            processes.append(subprocess.Popen('python client.py -m send',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            processes.append(subprocess.Popen('python client.py -m listen',
                                              creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif actions == 'c':
        while processes:
            victim = processes.pop()
            victim.kill()
