from collections import OrderedDict

def parsel(expr, parse_table, terminals, non_terminals):
    try:
        msg = []
        stack = ['$']
        stack.insert(0, non_terminals[0])
        msg.append('Matched\t\tStack\t\tInput\t\tAction\n')
        x = "-\t\t"
        for i in stack:
            x += i
        x += "\t\t"
        x += expr+"\t\t"
        x += '-'
        msg.append(x)
        matched ='-'
        while(True):
            action = "-"
            if(stack[0] == expr[0] and stack[0] == "$"):
                break
            elif(stack[0] == expr[0]):
                if(matched == "-"):
                    matched = expr[0]
                else:    
                    matched = matched + expr[0]
                action = "Matched "+expr[0]
                expr = expr[1:]
                stack.pop(0)
            else:
                action = parse_table[non_terminals.index(stack[0])][terminals.index(expr[0])]
                stack.pop(0)
                i = 0
                for item in action[2:]:
                    if(item != "`"):
                        stack.insert(i,item)
                    i+=1
            x = ""+matched+"\t\t"
            for i in stack:
                x += i
            x += "\t\t"
            x += expr+"\t\t"
            x += action
            msg.append(x)
        return msg
    except:
        return -1
    
def parse(expr, parse_table, terminals, non_terminals):
    stack = ["$"]
    stack.insert(0, non_terminals[0])

    print("\t\t\tMatched\t\t\tStack\t\t\tInput\t\t\tAction\n")
    print("\t\t\t-\t\t\t", end = "")
    for i in stack:
        print(i,  end = "")
    print("\t\t\t", end = "")
    print(expr+"\t\t\t", end = "")
    print("-")

    matched = "-"
    while(True):
        action = "-"

        if(stack[0] == expr[0] and stack[0] == "$"):
            break

        elif(stack[0] == expr[0]):
            if(matched == "-"):
                matched = expr[0]
            else:    
                matched = matched + expr[0]
            action = "Matched "+expr[0]
            expr = expr[1:]
            stack.pop(0)

        else:
            action = parse_table[non_terminals.index(stack[0])][terminals.index(expr[0])]
            stack.pop(0)
            i = 0
            for item in action[2:]:
                if(item != "`"):
                    stack.insert(i,item)
                i+=1

        print("\t\t\t"+matched+"\t\t\t", end = "")
        for i in stack:
            print(i,  end = "")
        print("\t\t\t", end = "")
        print(expr+"\t\t\t", end = "")
        print(action)

def get_rule(non_terminal, terminal, grammar, grammar_first):
    for rhs in grammar[non_terminal]:
        for rule in rhs:
            if(rule == terminal):
                string = non_terminal+"~"+rhs
                return string
            
            elif(rule.isupper() and terminal in grammar_first[rule]):
                string = non_terminal+"~"+rhs
                return string

def isterminal(char):
    if(char.isupper() or char == "`"):
        return False
    else:
        return True

def insert(grammar, lhs, rhs):
    if(lhs in grammar and rhs not in grammar[lhs] and grammar[lhs] != "null"):
        grammar[lhs].append(rhs)
    elif(lhs not in grammar or grammar[lhs] == "null"):
        grammar[lhs] = [rhs]
    return grammar

def first(lhs, grammar, grammar_first):
    rhs = grammar[lhs]
    for i in rhs:
        k = 0
        flag = 0
        current = []
        confirm = 0
        flog = 0
        if(lhs in grammar and "`" in grammar_first[lhs]):
            flog = 1
        while(1):	
            check = []
            if(k>=len(i)):
                if(len(current)==0 or flag == 1 or confirm == k or flog == 1):
                    grammar_first = insert(grammar_first, lhs, "`")
                break				
            if(i[k].isupper()):
                if(grammar_first[i[k]] == "null"):
                    grammar_first = first(i[k], grammar, grammar_first)
                   # print("state ", lhs, "i ", i, "k, ", k, grammar_first[i[k]])
                for j in grammar_first[i[k]]:
                    grammar_first = insert(grammar_first, lhs, j)
                    check.append(j)
            else:
                grammar_first = insert(grammar_first, lhs, i[k])
                check.append(i[k])
            if(i[k]=="`"):
                flag = 1
            current.extend(check)
            if("`" not in check):
                if(flog == 1):
                    grammar_first = insert(grammar_first, lhs, "`")
                break
            else:
                confirm += 1
                k+=1
                grammar_first[lhs].remove("`")
    return(grammar_first)

def rec_follow(k, next_i, grammar_follow, i, grammar, start, grammar_first, lhs):
    if(len(k)==next_i):
        if(grammar_follow[i] == "null"):
            grammar_follow = follow(i, grammar, grammar_follow, start)
        for q in grammar_follow[i]:
            grammar_follow = insert(grammar_follow, lhs, q)
    else:
        if(k[next_i].isupper()):
            for q in grammar_first[k[next_i]]:
                if(q=="`"):
                    grammar_follow = rec_follow(k, next_i+1, grammar_follow, i, grammar, start, grammar_first, lhs)		
                else:
                    grammar_follow = insert(grammar_follow, lhs, q)
        else:
            grammar_follow = insert(grammar_follow, lhs, k[next_i])

    return(grammar_follow)

def follow(lhs, grammar, grammar_follow, start,grammar_first):
    for i in grammar:
        j = grammar[i]
        for k in j:
            if(lhs in k):
                next_i = k.index(lhs)+1
                grammar_follow = rec_follow(k, next_i, grammar_follow, i, grammar, start, grammar_first, lhs)
    if(lhs==start):
        grammar_follow = insert(grammar_follow, lhs, "$")
    return(grammar_follow)

class Grammar:
    def __init__(self, path):
        self.grammar = OrderedDict()
        self.grammar_first = OrderedDict()
        self.grammar_follow = OrderedDict()
        f = open(path)
        for i in f:
            i = i.replace("\n", "")
            lhs = ""
            rhs = ""
            flag = 1
            for j in i:
                if(j=="~"):
                    flag = (flag+1)%2
                    continue
                if(flag==1):
                    lhs += j
                else:
                    rhs += j
            self.grammar = insert(self.grammar, lhs, rhs)
            self.grammar_first[lhs] = "null"
            self.grammar_follow[lhs] = "null"

        for lhs in self.grammar:
            if(self.grammar_first[lhs] == "null"):
                self.grammar_first = first(lhs, self.grammar, self.grammar_first)
        
        start = list(self.grammar.keys())[0]
        for lhs in self.grammar:
            if(self.grammar_follow[lhs] == "null"):
                self.grammar_follow = follow(lhs, self.grammar, self.grammar_follow, start, self.grammar_first)

        self.non_terminals = list(self.grammar.keys())
        self.terminals = []

        for i in self.grammar:
            for rule in self.grammar[i]:
                for char in rule:
                    if(isterminal(char) and char not in self.terminals):
                        self.terminals.append(char)
        self.terminals.append("$")

    def get_parse_table(self):
        parse_table = [[""]*len(self.terminals) for i in range(len(self.non_terminals))]
        for non_terminal in self.non_terminals:
            for terminal in self.terminals:
                if terminal in self.grammar_first[non_terminal]:
                    rule = get_rule(non_terminal, terminal, self.grammar, self.grammar_first)

                elif("`" in self.grammar_first[non_terminal] and terminal in self.grammar_follow[non_terminal]):
                    rule = non_terminal+"~`"

                elif(terminal in self.grammar_follow[non_terminal]):
                    rule = "Sync"

                else:
                    rule = ""
                parse_table[self.non_terminals.index(non_terminal)][self.terminals.index(terminal)] = rule
        
        return parse_table
    

def display_parse_table(obj, parse_table, terminal, non_terminal):
    print("\t\t\t\t",end = "")
    for terminal in obj.terminals:
        print(terminal+"\t\t", end = "")
    print("\n\n")
    
    for non_terminal in obj.non_terminals:
        print("\t\t"+non_terminal+"\t\t", end = "")
        for terminal in obj.terminals:
            print(parse_table[obj.non_terminals.index(non_terminal)][obj.terminals.index(terminal)]+"\t\t", end = "")
        print("\n")

if __name__ == "__main__":
    grmr = Grammar()
    display_parse_table(grmr, grmr.get_parse_table(), grmr.terminals, grmr.non_terminals)
    parse("i+i*i$", grmr.get_parse_table(), grmr.terminals, grmr.non_terminals)