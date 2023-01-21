import json

if __name__ == '__main__':
    stats = json.load(open('dump/stats.json', encoding='utf-8'))
    cat = json.load(open('dump/statcat.json', encoding='utf-8'))
    for k, v in stats.items():
        try:
            cat[v['category']].setdefault('children', []).append({
                x: v[x] for x in ('defName', 'label')
            })
        except KeyError:
            pass

    cat = [v for v in cat.values() if 'children' in v]
    cat.sort(key=lambda x: x['displayOrder'])
    for v in cat:
        v.pop('@DefType', None)
        v.pop('displayAllByDefault', None)
        v.pop('displayOrder', None)
    json.dump({'order': cat}, open('dump/stat_order.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

