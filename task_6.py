with open('test_file.txt', 'w', encoding='utf-8') as t_f:
    t_f.write('сетевое программирование\n')
    t_f.write('сокет\n')

with open('test_file.txt', encoding='utf-8') as t_f:
    for each_line in t_f:
        print(each_line, end="")
