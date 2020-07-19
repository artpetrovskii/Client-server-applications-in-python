import yaml

DATA_IN = {'items': ['computer', 'printer', 'keyboard', 'mouse'],
           'items_quantity': 4,
           'items_ptice': {'computer': '200€-1000€',
                           'printer': '100€-300€',
                           'keyboard': '5€-50€',
                           'mouse': '4€-7€'}
           }

with open('file_1.yaml', 'w', encoding='utf-8') as f_in:
    yaml.dump(DATA_IN, f_in, default_flow_style=False, allow_unicode=True)

with open("file_1.yaml", 'r', encoding='utf-8') as f_out:
    DATA_OUT = yaml.load(f_out, Loader=yaml.SafeLoader)

print(DATA_IN == DATA_OUT)
