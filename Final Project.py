from itertools import permutations, product, combinations
from copy import deepcopy
import random

def get_rand(leng, num):
    """
    Generate random place for water tower
    : return: list of tuple containing all possible positions for water tower
    """
    if num>1:
        comb = list(combinations(range(leng), 2))
        comb.extend(comb)
        cc = list(combinations(comb,2))
        ret = set()
        for c in cc:
            if c[0][0]!= c[1][1] or c[1][0]!= c[0][1]:
                ret.add(((c[0][0], c[1][0]), (c[0][1], c[1][1])))
        return list(ret) #list of tuple of tuple [((x,x), (x,x)), ]
    else:
        ret = list(product(range(leng), repeat = 2))
        return ret #list of tuple [(x,x), ]

def generate_perm(leng):
    """
    Generate all possible layouts for buildings
    : return: list of list all possible layouts for buildings
    """
    perm = list(permutations([i+1 for i in range(leng)]))
    comb = list(product(perm, repeat = leng))
    ret = []
    flag = True
    for c in comb:
        flag = True
        for i in range(leng):
            visited = []
            for j in range(leng):
                if c[j][i] not in visited:
                    visited.append(c[j][i])
                else:
                    flag = False
                    break
            if flag== False: 
                break
        if flag: 
            ret.append(c)
    return ret

def generate_map(leng, num):
    """
    Generate all possible layouts with buildings and water towers
    : return: all possible layouts and the number of possible layouts
    """
    ret = []
    all_map = generate_perm(leng)
    rand = get_rand(leng, num)
    r_len = len(rand)
    i = 0
    if num<= 1:
        while i < len(all_map):
            j= 0
            while j< r_len:
                mp = [list(elem) for elem in deepcopy(all_map[i])]
                mp[rand[j][0]][rand[j][1]] = str(mp[rand[j][0]][rand[j][1]])
                ret.append(mp)
                j+= 1
            i+= 1
        return ret, len(ret) #list of list of list
    else:
        while i < len(all_map):
            j= 0
            while j< r_len:
                mp = [list(elem) for elem in deepcopy(all_map[i])]
                mp[rand[j][0][0]][rand[j][0][1]] = str(mp[rand[j][0][0]][rand[j][0][1]])
                mp[rand[j][1][0]][rand[j][1][1]] = str(mp[rand[j][1][0]][rand[j][1][1]])
                ret.append(mp)
                j+= 1
            i+= 1
        return ret, len(ret)

def print_layout(hint, layout, num, summ):
    """
    Orgainze the check layout and hint
    : return: null, print the layout and hint
    """
    print('# water tower = '+ str(num)+ ' tower height sum = '+ str(summ))
    print('   '+ ' '.join([str(m) for m in hint[0]]))
    for i in range(4):
        layer = ' '.join([str(m) for m in layout[i]])
        for j in range(4):
            if isinstance(layout[i][j], str) and layout[i][j]!='-':
                if j>=1:
                    layer = layer[:2*j-1] + '['+ layer[2*j:]
                if j<3:
                    layer = layer[:2*j+1] + ']' + layer[2*j+2:]
        print(str(hint[1][i])+ ' |'+ layer+ '| '+ str(hint[3][i]))
    print('   '+ ' '.join([str(m) for m in hint[2]]))

#print(generate_map(4, 2))
plain_layout = [['-' for i in range(4)] for j in range(4)]
hint = [[5 for i in range(4)] for j in range(4)]
def user_input(hint, layout, num, summ):
    """
    Allow user input and check game status
    : return: null, print hints, current layour and user guidance
    """
    layout = plain_layout
    print_layout(hint, layout, num, summ)
    leng = len(layout)
    count= 0
    while True:
        inp = input('Input coordinate and num:')
        if inp== 'q' or inp== 'Q' or inp == 'quit':
            print('End Game')
            break
        try:
            cord = inp.split(' ')[0].split(',')
            if len(inp.split(' ')[1])==1:
                fill = int(inp.split(' ')[1])
            else:
                fill = inp.split(' ')[1][1]
        except:
            print('Please fill in the form: "x,y number"')
            continue
        if isinstance(fill, int):
            if fill>leng:
                print('Please fill in a valid number')
                continue
        if int(cord[0])<0 or int(cord[0])>=leng or int(cord[1])<0 or int(cord[1])>=leng:
            print('Please input a valid coordinate')
            continue
        if layout[int(cord[0])][int(cord[1])]== '-':
            count+= 1
        layout[int(cord[0])][int(cord[1])] = fill
        print_layout(hint, layout, num, summ)
        if count == leng**2:
            str_sum = 0
            for i in range(leng):
                for j in range(leng):
                    if isinstance(layout[i][j], str):
                        str_sum+= int(layout[i][j])
            flag,_ = check_all(layout, hint, num, summ)
            if flag:
                print('YOU WIN!')
                break
            else:
                print('YOU LOSE')
                print('Press q to end game, or change your input to resume')

def check(board):
    """
    Calculate hint from the layout
    :return: list of hint calculated from layout
    """
    flag = True
    count_hint = []
    up_count,down_count,left_count,right_count=[],[],[],[]

    for j in range(len(board)):
        left, right, max_l, max_r=0,0,0,0
        for i in range(len(board[j])):
            if int(board[j][i])>max_l:
                left+=1
                if isinstance(board[j][i],str) == False:
                    max_l = board[j][i]
            if int(board[j][len(board)-1-i])>max_r:
                right+=1
                if isinstance(board[j][len(board)-1-i], str) == False:
                    max_r = board[j][len(board)-1-i]
        left_count.append(left)
        right_count.append(right)

    for i in range(len(board[0])):
        up,down, max_u, max_d = 0, 0, 0, 0
        for j in range(len(board)):
            if int(board[j][i])>max_u:
                up+=1
                if isinstance(board[j][i], str) == False:
                    max_u = board[j][i]
            if int(board[len(board)-1-j][i])>max_d:
                down+=1
                if isinstance(board[len(board)-1-j][i], str) == False:
                    max_d = board[len(board)-1-j][i]
        up_count.append(up)
        down_count.append(down)

        count_hint = [up_count,left_count,down_count,right_count]
    return count_hint

def check_all(board,hint,str_count,str_sum):
    """
    Check if input layout satisfies all the hints
    : return: if the input is correct (flag) and hints calculated from input layout
    """
    flag = True
    count_hint = []
    up_count,down_count,left_count,right_count=[],[],[],[]
    count_str = 0
    sum_str = 0

    for j in range(len(board)):
        left, right, max_l, max_r=0,0,0,0
        for i in range(len(board[j])):
            if isinstance(board[j][i],str):
                count_str+=1
                sum_str+=int(board[j][i])
            if int(board[j][i])>max_l:
                left+=1
                if isinstance(board[j][i],str) == False:
                    max_l = board[j][i]
            if int(board[j][len(board)-1-i])>max_r:
                right+=1
                if isinstance(board[j][len(board)-1-i], str) == False:
                    max_r = board[j][len(board)-1-i]
        left_count.append(left)
        right_count.append(right)

    for i in range(len(board[0])):
        up,down, max_u, max_d = 0, 0, 0, 0
        for j in range(len(board)):
            if int(board[j][i])>max_u:
                up+=1
                if isinstance(board[j][i], str) == False:
                    max_u = board[j][i]
            if int(board[len(board)-1-j][i])>max_d:
                down+=1
                if isinstance(board[len(board)-1-j][i], str) == False:
                    max_d = board[len(board)-1-j][i]
        up_count.append(up)
        down_count.append(down)

        if up != hint[0][i] or down!= hint[2][i] or left!= hint[1][j] or right!= hint[3][j] or count_str != str_count or sum_str != str_sum:
            flag = False
            break
        count_hint = [up_count,left_count,down_count,right_count]
    return flag, count_hint

def solver():
    """
    Generate puzzle, and find the puzzle with unique solution
    : return: the puzzle hint in list, layout in list of list, 
              # of towers in int, tower total height
    """
    while True:
        print('Generating Puzzle...')
        num = random.randint(1, 2)
        all_maps, all_len = generate_map(4, num)
        layout = all_maps[random.randint(1, all_len-1)]
        hint = check(layout)
        str_sum = 0
        for i in range(4):
            for j in range(4):
                if isinstance(layout[i][j], str):
                    str_sum+= int(layout[i][j])
        mp, _ = generate_map(4, num)
        fin_m = ''
        valid_sol_count = 0
        for m in mp:
            #pdb.set_trace()
            flag, __ = check_all(m, hint, num, str_sum)
            if flag:
                fin_m = m
                fin_sum = str_sum
                fin_num = num
                valid_sol_count+= 1
                if valid_sol_count>1:
                    break
        if valid_sol_count==1:
            print_layout(hint, fin_m, fin_num, fin_sum)
            return hint, fin_m, fin_num, fin_sum

def game_generator():
    """
    Generate an interactive playable game
    : return: null
    """
    hint, layout, num, str_sum = solver()
    user_input(hint, layout, num, str_sum)

# game_generator()
solver()

