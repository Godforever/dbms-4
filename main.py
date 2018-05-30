from utils import *
from select import *
from difference import *
from intersect import *
from join import *
from projection import *
from union import *

def printTips():
    print('====================Please Choose Options!====================')
    print('=                 1.Generating Data.                         =')
    print('=                 2.Linear Selecting.                        =')
    print('=                 3.Binary Selecting.                        =')
    print('=                 4.Projection.                              =')
    print('=                 5.nest_loop_join.                          =')
    print('=                 6.sort_merge_join.                         =')
    print('=                 7.hash_join.                               =')
    print('=                 8.Set Union.                               =')
    print('=                 9.Set Intersect.                           =')
    print('=                 10.Set Difference.                         =')
    print('=                 11.Index Selecting.                        =')
    print('==============================================================')


if __name__ == '__main__':
    while True:
        printTips()
        options = int(input())
        if options == 1:
            generate_R_S()
        elif options == 2:
            linear_select()
        elif options == 3:
            binary_select_R_S()
        elif options == 4:
            projection()
        elif options == 5:
            nest_loop_join()
        elif options == 6:
            sort_merge_join()
        elif options == 7:
            hash_join()
        elif options == 8:
            setUnion()
        elif options == 9:
            setIntersect()
        elif options == 10:
            setDifference()
        elif options == 11:
            index_select()



