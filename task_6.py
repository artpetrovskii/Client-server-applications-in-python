with open('test_file.txt', 'w', encoding='cp866') as t_f:
    t_f.write('сетевое программирование\n')
    t_f.write('сокет\n')

with open('test_file.txt', encoding='cp866') as t_f:
    for each_line in t_f:
        print(each_line, end="")
