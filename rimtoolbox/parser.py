import json
import re
from typing import Optional as opt, Union, Dict, List, Callable
from pathlib import Path
from collections import OrderedDict

import xmltodict

from . import log

__all__ = ['Workspace']

all_deftype = (
    'ThingDef',
    'TerrainDef',
    'TraitDef'
)


class Workspace(object):
    defs: Dict[str, Dict]
    _refs: Dict[str, Dict]
    langdata: Dict[str, str]

    def __init__(self):
        self.defs = {}
        self._refs = {}
        self.langdata = {}

    def digest(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)

        assert path.is_file(), 'Digest path %s not file' % path
        assert path.suffix == '.xml', 'Digest file must be xml file'

        data = xmltodict.parse(path.read_text('utf-8'), force_list=all_deftype+('li',))

        if data.get('Defs'):
            logger.trace('digest file as def file: %s' % path)
            for key in data['Defs']:
                if key in all_deftype:
                    deftype = key
                else:
                    continue

                defxmls = data['Defs'][deftype]
                for defxml in defxmls:
                    defxml['@DefType'] = deftype # record

                    ### 移除不需要的元素
                    for i in (
                        'comps', 'tools', 'verbs', 'inspectorTabs',
                        'apparel', 'devNote'
                    ):
                        defxml.pop(i, None)
                    ###

                    if '@Name' in defxml:
                        logger.trace('parent name load: [%s]' % defxml['@Name'])
                        self._refs[defxml['@Name']] = defxml
                    if not '@Abstract' in defxml:
                        self.defs[defxml['defName']] = defxml

        elif data.get('LanguageData'):
            logger.trace('digest file as langdata: %s' % path)
            self.langdata.update(data['LanguageData'])

        else:
            logger.warning('unknown file content, ignore: %s' % path)

    def digest_dir(self, path: Union[str, Path],
        depth: int = -1,
        filter: opt[Callable[[Path], bool]] = None
    ):
        if isinstance(path, str):
            path = Path(path)

        assert path.is_dir(), 'Digest path %s not dir' % path

        for path in path.iterdir():
            if path.is_file() and path.suffix == '.xml':
                if filter is None or filter(path):
                    self.digest(path)
            elif path.is_dir():
                if depth > 0:
                    self.digest_dir(path, depth-1)
                elif depth == -1:
                    self.digest_dir(path, -1)

    def solve_inherit(self):
        def merge_comp(li, base):
            # 合并两个 comp 列表：
            # 若两个元素有相同的 compClass 键，则使用 li 中的元素
            to_extend = []
            for item in li:
                if isinstance(item, dict) and 'compClass' in item:
                    for i in li:
                        if i.get('compClass') == item['compClass']:
                            logger.warning('collide')
                            break
                    else:
                        to_extend.append(item)
                else:
                    to_extend.append(item)
            li.extend(to_extend)

        def cut_inherit(child, parent):
            # 解耦两个 defxml 间的继承关系
            assert child['@ParentName'] == parent['@Name']
            assert not parent.get('@ParentName')
            child.pop('@ParentName')

            logger.trace('cut [%s] --> [%s]'
                % (child.get('defName') or child['@Name'], parent['@Name']))

            for k, v in parent.items():
                if k in ('@Abstract', '@Name', '@ParentName', '@DefType'):
                    # 特殊 key 不予覆盖
                    pass
                elif k not in child:
                    # 该 key 在子类未定义，遂覆盖之
                    child[k] = v
                elif isinstance(child[k], dict) \
                and child[k].get('@Inherit', '').lower() == 'false':
                        # 该 key 有不继承标注，移除该标注，若移除标注后 key 内无内容，则将该 key 也移除
                        # Note:
                        #   有时子类会给父类并没有的 key 打上不继承标注
                        #   这些仅子类拥有的 key 无法被遍历到
                        #   因此 dump 的结果依然会有非预期的 @Inherit 存在
                        child[k].pop('@Inherit')
                        if not child[k].keys():
                            child.pop(k)

                elif isinstance(child[k], dict) and isinstance(parent[k], dict):
                    if child[k].get('li') and parent[k].get('li'):
                        # 该 key 指向一个列表，尝试合并
                        if k == 'comp':
                            merge_comp(child[k]['li'], parent[k]['li'])
                        else:
                            child[k]['li'].extend(parent[k]['li'])

                    else:
                        for k1, v1 in parent[k].items():
                            if k1 not in child[k]:
                                child[k][k1] = v1

        for defxml in self.defs.values():
            if '@ParentName' not in defxml:
                continue

            mro = [defxml] # inherit link: child <---> parent
            while True:
                parent_name = mro[-1].get('@ParentName')
                if parent_name is None:
                    break

                try:
                    parent = self._refs[parent_name]
                except KeyError:
                    logger.warning('when solving inherit for [%s], parent [%s] is missing' % (name, parent_name))
                    break
                mro.append(parent)

            # 倒序覆盖
            for index in range(len(mro)-1):
                cut_inherit(mro[-index-2], mro[-index-1])

    def inject_langdata(self, *, mark='T', ignore_extra=False):
        for key, trans in self.langdata.items():
            defname, part = key.split('.', 1)
            if part not in ('label', 'description'):
                continue

            logger.trace('langdata %s' % key)
            try:
                defxml = self.defs[defname]
            except KeyError:
                if not ignore_extra:
                    logger.warning('dangling langdata for [%s]' % key)
                continue

            defxml[part + '-' + mark] = trans

    def clean(self):
        for defxml in self.defs.values():
            defxml.pop('@Name', None)
            defxml.pop('@ParentName', None)
            # 将 <li> 转换成正常的列表
            for k, v in defxml.items():
                if isinstance(v, dict) and v.get('li'):
                    defxml[k] = v['li']
                

    def dump(self, path, indent=0):
        if isinstance(path, str):
            path = Path(path)

        text = json.dumps(self.defs, indent=indent, ensure_ascii=False)
        path.write_text(text)
