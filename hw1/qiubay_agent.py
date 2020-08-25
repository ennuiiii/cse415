

from re import *   # Loads the regular expression module.
import random

def introduce():
    intro = "I don't have a name, I'm your boyfriend. \n\
            I'm not telling you that I was programmed by Qiubai Yu whose UWNETID is qiubay. \n\
            You should treat me as a real person. \n\
            Do you miss me?"
    return intro

def agentName():
    return "bf"

def Boyfriend_bot():
    'Boyfriend bot is the auto-response bot in case you did not see the message from your girlfriend'
    print(introduce())
    while True:
        the_input = input('TYPE HERE:>> ')
        if match('bye',the_input):
            print('Have a good rest of your day!')
            return
        if match('good', the_input):
            print('deal!')
            return
        print(respond(the_input))

def respond(the_input):
    wordlist = split(' ',remove_punctuation(the_input))
    # undo any initial capitalization:
    wordlist[0]=wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0]=mapped_wordlist[0].capitalize()
    # no topics. Find a topic that the girl likes
    if wordlist[0]=='':
        if not MEMORY:
            return ("I just wanna let you know that I miss you.")
        else:
            return ("I remember that you like " + random_MEMORY() + "? Do you wanna do that?")
    # keyword like: record what she likes
    if 'like' in wordlist:
        index = wordlist.index('like')
        event = stringify(mapped_wordlist[index:])
        MEMORY.append(event)
        return ("I'm glad to know that.")
    # keyword hungry: list out possible foods
    if 'hungry' in wordlist:
        return ("Hotpot? Sushi? Barbeque? Steak? What are you planning to eat?")
    # if some food is the respond
    if food(wordlist[0]):
        return ("I know a place that has very good " + wordlist[0] + "."
              + " Do you wanna try it tomorrow?")
    
    if wordlist[0:2] == ['good', 'morning']:
        return ("Good morning. Wanna do some sports?")
    if wpred(wordlist[0]):
        return (wordlist[0] + "?")
    if wordlist[0:3] == ['i','want','to']:
        return ("I agree with you to do so. ＜（＾－＾）＞")
    if wordlist[0:2] == ['i','feel']:
        return ("Drink some hot water. o(*￣▽￣*)ブ")
    if 'hate' in wordlist:
        return ("I'm sorry to hear that. b\(￣︶￣*\))")
    if 'yes' in wordlist:
        return ("Great!")
    if wordlist[0:2] == ['you','are']:
        return ("Someone did say that to me previously.")
    if wordlist[0:3] == ['do','you','think']:
        return ("Follow your heart.")
    if 'heavy' in wordlist:
        return ("Don't ever say you're heavy again."
        + " You know you are the best in my heart!")
    if 'dream' in wordlist:
        return ("Did you have a bad dream babe?")
    if 'love' in wordlist:
        return ("I love you three thousand.")
    if 'no' in wordlist:
        return ("Why?")
    if 'maybe' in wordlist:
        return ("You know I respect every choice you make.")
    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        return (stringify(mapped_wordlist) + '.')
    # I'm reluctant to do anything if one rush me
    if 'now' in wordlist:
        return ("Yes yes yes.")
    # I'm jealous
    if 'man' in wordlist:
        return ("Don't ever talk about other men in front of me!")
    return punt()

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when','why','where','how'])

# def dpred(w):
#     'Returns True if w is an auxiliary verb.'
#     return (w in ['do','can','should','would'])

PUNTS = ['Ummm...',
         'I am doing sport, call you later.',
         'Are you hungry?',
         'Let me figure out what do you mean.',
         'Love you.',
         'Good to know.',
         'You are right.']

punt_count = 0
def punt():
    'Returns one from a list of default responses.'
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 7]

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}
MEMORY = []

def random_MEMORY():
    return random.choice(MEMORY)

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def food(w):
    'Returns True if w is one of the food of the following.'
    return (w in ['hotpot', 'ice-cream', 'boba', 'sushi', 'ramen',
                  'steak', 'tofu', 'chicken'])


Boyfriend_bot()
