
# Part A

def five_x_cubed_plus_2(x) :
    return 5 * x ** 3 + 2

def triple_up(lst):
    return [lst[x:x+3] for x in range(0, len(lst), 3)]

def mystery_code(str):
    mystery_dic = {"a":"v", "b":"w", "c":"x", "d":"y", "e":"z", "f":"a", "g":"b", "h":"c", "i":"d", "j":"e", "k":"f",
                   "l":"g", "m":"h", "n":"i", "o":"j", "p":"k", "q":"l", "r":"m", "s":"n", "t":"o", "u":"p", "v":"q",
                   "w":"r", "x":"s", "y":"t", "z":"u"}
    ans = []
    for i in str:
        if i.isalpha():
            if i.isupper():
                ans.append(mystery_dic.get(i.lower()))
            else:
                ans.append(mystery_dic.get(i).upper())
        else:
            ans.append(i)
    return "".join(ans)

def future_tense(lst):
    #tomorrow
    time1 = ['today', 'yesterday', 'now']
    time2 = ['Today', 'Yesterday', 'Now']
    #will be
    tobe = ['am', 'is', 'are', 'was', 'were']
    #will go
    togo = ['went', 'go', 'goes']
    #will eat
    toeat =['ate', 'eat', 'eats']
    #will have
    tohave =['had', 'have', 'has']
    #will do
    todo =['did', 'do', 'does']
    ans = []
    for str in lst:
        if str in time1:
            ans.append('tomorrow')
        elif str in time2:
            ans.append('Tomorrow')
        elif str in tobe:
            ans.append('will')
            ans.append('be')
        elif str in togo:
            ans.append('will')
            ans.append('go')
        elif str in toeat:
            ans.append('will')
            ans.append('eat')
        elif str in tohave:
            ans.append('will')
            ans.append('have')
        elif str in todo:
            ans.append('will')
            ans.append('do')
        else:
            ans.append(str)
    return ans

