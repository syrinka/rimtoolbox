import sys
import json


# 展平数据，k['a']['b'] -> k['a.b']
if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    exp = {}
    for k1, v1 in data.items():
        exp[k1] = {}
        for k2, v2 in v1.items():
            if isinstance(v2, dict):
                for k3, v3 in v2.items():
                    exp[k1][k2+'.'+k3] = v3
            else:
                exp[k1][k2] = v2
    json.dump(exp, open(sys.argv[2], 'w', encoding='utf-8'),
        indent=4,
        ensure_ascii=False
    )