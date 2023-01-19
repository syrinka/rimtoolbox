import sys
from rimtoolbox.parser import Workspace, Path

if __name__ == '__main__':
    w = Workspace()
    for i in sys.argv[1:-1]:
        w.digest_dir(i)
    w.solve_inherit()
    w.inject_langdata(mark='', ignore_extra=True)
    w.clean()
    w.dump('dump/thingdef.json', ('ThingDef',))
    w.dump('dump/stats.json', ('StatDef',))
    w.dump('dump/statcat.json', ('StatCategoryDef',))