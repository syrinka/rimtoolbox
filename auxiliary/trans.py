import sys
import json


# 抽取中英对照，csv形式输出
if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    csv = open(sys.argv[2], 'w', encoding='utf-8')
    csv.write('en,zh\n')
    for k, v in data.items():
        csv.write(f'{k},{v["label"]}\n')
