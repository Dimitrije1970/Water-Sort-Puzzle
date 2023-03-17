from math import trunc
from copy import deepcopy
from time import time
from random import randrange

#generisanje slucajnog pocetnog stanja igre
def generate_random_game(n, k):
    colors = []
    colors_added = 0
    while len(colors) < (n - k) * 4:
        rand = randrange(n-k) + 1
        if (rand == 0):
            continue
        if (rand not in colors and colors_added < (n - k)):
            colors.append(rand)
            colors_added += 1
        elif (0 < colors.count(rand) < 4):
            colors.append(rand)

    init_state = [[0 for x in range(4)] for y in range(n)]
    t = 0
    for i in range(n - k):
        for j in range(4):
            init_state[i][j] = colors[t]
            t += 1

    return init_state
#presipanje i vracanje vrednosti da li je presipanje moguce
def move(state, one, two):
    one -= 1
    two -= 1

    if(one == two):return 0

    top_two = 0; top_pos_two = -1
    for i in range(3, -1, -1):
        if state[two][i] != 0 :
            top_two = state[two][i]
            top_pos_two = i
            break
    receive = 3 - top_pos_two

    top_one = 0; top_pos_one = -1; bot_pos_one = 0
    for i in range(3, -1, -1):
        if state[one][i] != 0:
            top_one = state[one][i]
            top_pos_one = i
            for j in range(top_pos_one, -1, -1):
                if state[one][j] != top_one:
                    bot_pos_one = j+1
                    break
            break
    give = 0
    if top_pos_one >= 0:
        give = top_pos_one - bot_pos_one + 1

    if give == 0 or receive == 0:return 0
    if top_one == top_two or top_two == 0:
        if give <= receive:
            for i in range(give, 0, -1):
                top_pos_two += 1
                state[two][top_pos_two] = top_one
                state[one][top_pos_one] = 0
                top_pos_one -= 1
        else:
            for j in range(receive-1, -1, -1):
                top_pos_two += 1
                state[two][top_pos_two] = top_one
                state[one][top_pos_one] = 0
                top_pos_one -= 1

        return 1
    else:
        return 0

id = 0
states = []
#struktura cvora
class Node:
    def __init__(self, id, state, father):
        self.id = id
        self.state = state
        self.next = []
        self.father = father
        self.hints = 0

    def print_node(self):
        for i in range(3, -1, -1):
            for j in range(n):
                if(j == n-1):
                    print("%3d" % self.state[j][i])
                else:
                    print("%3d" % self.state[j][i], end="")

    def print_id(self):
        if self.father is not None:
            print(" |(" + str(self.id)+ ")" + " Sin od ({}) {}| ".format(str(self.father.id), str(self.hints)), end="   ")
        else:
            print(" |(" + str(self.id) + ")" + " Sin od (None) {}| ".format(str(self.hints)), end="   ")

    def generate_next(self, n):
        new_state = deepcopy(self.state)
        for i in range(n):
            for j in range(n):
                if move(new_state, i, j):
                    global states
                    if new_state == self.state or new_state in states:
                        new_state = deepcopy(self.state)
                        continue
                    else:
                        global id
                        id += 1
                        new_node = Node(id, new_state, self)
                        new_node.hints = is_winning_state(new_node)
                        self.next.append(new_node)
                        states.append(new_state)
                        new_state = deepcopy(self.state)

#strukture reda i steka
class Queue:
    def __init__(self):
        self.queue = []

    def insert(self, node):
        if node not in self.queue:
            self.queue.insert(0, node)
            return 1
        return 0

    def delete(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return 0
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, node):
        if node not in self.stack:
            self.stack.append(node)
            return 1
        return 0

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        return 0

#generise stablo
def generate_tree(root, n, p):
    queue = Queue()
    queue.insert(root)
    before_next_level = [0]*(p+1)
    before_next_level[0] = 1
    depth = 0
    while depth < p:
        if(before_next_level[depth] == 0):depth += 1;
        if(depth >= p):break
        current_node_in_gen = queue.delete()
        before_next_level[depth] -= 1
        if(type(current_node_in_gen) == int):
            continue
        current_node_in_gen.generate_next(n)
        sons = current_node_in_gen.next
        for son in sons:
            queue.insert(son)
        before_next_level[depth+1] += len(sons)
#ispisuje stablo pomocu level-order obilaska
def print_level_order(root, p):
    queue = Queue()
    queue.insert(root)
    before_next_level = [0]*(p+1)
    before_next_level[0] = 1
    depth = 0
    while depth < p:
        if(before_next_level[depth] == 0):
            depth += 1
            if (depth >= p):
                break
            else:
                print("\nNivo {}:".format(depth), end="")
            print()
        current_node_in_prnt = queue.delete()
        current_node_in_prnt.print_id()
        before_next_level[depth] -= 1
        sons = current_node_in_prnt.next
        for son in sons:
            queue.insert(son)
        before_next_level[depth+1] += len(sons)
#za zadati cvor ispituje da li je njegovo stanje pobednicko
def is_winning_state(node):
    current_state_in_state = node.state
    for i in range(len(current_state_in_state)):
        color = current_state_in_state[i][0]
        for j in range(4):
            if current_state_in_state[i][j] != color:
                return 0
    return 1
#za zadati cvor ispituje da li se ispod njega u stablu nalazi pobednicko stanje
def is_winning_node(node, p):
    queue = Queue()
    queue.insert(node)
    before_next_level = [0]*(p+1)
    before_next_level[0] = 1
    depth = 0
    while depth < p:
        if(before_next_level[depth] == 0):
            depth += 1
            if (depth >= p):
                break
        current_node_in_win = queue.delete()
        if (is_winning_state(current_node_in_win)):
            return 1
        before_next_level[depth] -= 1
        sons = current_node_in_win.next
        for son in sons:
            queue.insert(son)
        before_next_level[depth+1] += len(sons)
    return 0
#vraca bilo koje pobednicko stanje
def return_winning_state(node, p):
    queue = Queue()
    queue.insert(node)
    before_next_level = [0]*(p+1)
    before_next_level[0] = 1
    depth = 0
    while depth < p:
        if(before_next_level[depth] == 0):
            depth += 1
            if (depth >= p):
                break
        current_node_in_win = queue.delete()
        if(is_winning_state(current_node_in_win)):
            return current_node_in_win
        before_next_level[depth] -= 1
        sons = current_node_in_win.next
        for son in sons:
            queue.insert(son)
        before_next_level[depth+1] += len(sons)
    return None
#sabira broj mogucih pobeda iz svakog cvora
def sum_hints(root, p):
    queue = Queue()
    stack = Stack()
    queue.insert(root)
    before_next_level = [0]*(p+1)
    before_next_level[0] = 1
    depth = 0
    while depth < p:
        if(before_next_level[depth] == 0):depth += 1;
        if(depth >= p):break
        current_node_in_hints = queue.delete()
        stack.push(current_node_in_hints)
        before_next_level[depth] -= 1
        sons = current_node_in_hints.next
        for son in sons:
            queue.insert(son)
        before_next_level[depth+1] += len(sons)

    while True:
        temp = stack.pop()
        if(temp.father == None):
            break
        temp.father.hints += temp.hints

n, k, p = [int(num) for num in input("Unesi ukupan broj posuda, broj praznih posuda i maksimalan broj poteza (n k p):").split()]

if n < k or (n-k) > 9:
    print("Lose uneti brojevi.")
    exit()

init_state = generate_random_game(n, k)
root = Node("0", init_state, None)
states.append(init_state)
root.print_node()
if(is_winning_state(root)):
    print("Igra je zavrsena.")
    exit()
generate_tree(root, n, p+1)
sum_hints(root, p+1)

current_node = root

print("1. Ispisi stablo (level-order).")
print("2. Odigraj potez.")
print("3. Hint.")
print("4. Ispisi jedno resenje igre.")
print("5. Ispisi sadrzaj cvora.")
print("0. Prekini program.")
choice = int(input("Unesi broj opcije:"))

turns_played = 0

while choice != 0:
    if choice == 1:
        print_level_order(root, p+1)
    elif choice == 2:
        if(turns_played > p):
            print("Maksimalan broj poteza ispunjen.")
            exit()
        first, second = [int(col) for col in input("Unesi brojeve posuda za presipanje (indeksiranje krece od 1):").split()]
        current_state = current_node.state
        if not move(current_state, first, second):
            current_node.print_node()
            print("Presipanje nije moguce.")
        else:
            turns_played += 1
            for item in current_node.next:
                if item.state == current_state:
                    current_node = item
                    break

            if is_winning_state(current_node):
                print("Igra je zavrsena.")
                exit()

            if not is_winning_node(current_node, p-turns_played+1):
                current_node.print_node()
                print("Igra ne moze biti zavrsena u zadatom broju poteza.")
                exit()
            else:
                current_node.print_node()
    elif choice == 3:
        hint_flag = 0
        for item in current_node.next:
            if item.hints > 0:
                current_node = item
                hint_flag = 1
                break
        if(hint_flag == 0):
            print("Ne postoji hint koji vodi do resenja.")

        current_node.print_node()

        if is_winning_state(current_node):
            print("Igra je zavrsena.")
            exit()

    elif choice == 4:
        print("Jedno validno resenje igre je:")
        winning_node = return_winning_state(current_node, p-turns_played+1)
        if(winning_node is not None):
            winning_node.print_node()
        else:
            print("Od ovog stanja, igra nema validno resenje u zadatom broju poteza.")

    elif choice == 5:
        id = input("Unesi kod cvora koji zelis da ispises:")
        state_by_id = states[int(id)]
        for i in range(3, -1, -1):
            for j in range(n):
                if(j == n-1):
                    print("%3d" % state_by_id[j][i])
                else:
                    print("%3d" % state_by_id[j][i], end="")


    choice = int(input("\nUnesi broj opcije:"))

