
import random, string

def randstr(count, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(count))
    
