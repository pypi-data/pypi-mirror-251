from time import perf_counter, time, sleep
from sys import exit, platform, argv
from os import system, remove, rename, path
from locale import getlocale
from subprocess import Popen
from math import gamma

inf = float('inf') # an infinitely large number
nan = float('nan') # "not a number" programming constant
pi = 3.141592653589793 # (π) ratio of the circumference of a circle to its diameter
tau = 6.283185307179586 # (τ) tau = 2pi
delta = 2.414213562373095 # (δ) silver ratio formula constant
phi = 1.618033988749894 # (φ) golden ratio formula constant
psi = 1.465571231876768 # (ψ) supergolden ratio formula constant
e = 2.718281828459045 # Euler's number
G = 6.67408e-11 # gravitational constant
g = { # standart acceleration of gravity
  'earth':   9.80665,
  'moon':    1.62,
  'venus':   8.88,
  'jupiter': 24.79,
  'uranus':  8.86,
  'eris':    0.81,
  'sun':     273.1,
  'mercury': 3.7,
  'mars':    3.86,
  'saturn':  10.44,
  'neptune': 11.09,
  'pluto':   0.617
}
lightspeed = 299792458 # m/s
volumespeed = 343.2 # m/s

def root(a, n=2): # mathimatic root
  root = a**(1/n)
  return ((-root, root), root)[n%2 or a==0]

def aroot(a, n=2): # arithmetic root (radical)
  return a**(1/n)

def neg(n): # make number negative
  return -abs(n)

def fib(n): # fibonacci series generator
  a, b = 0, 1
  for i in range(n):
    yield a
    a, b = b, a+b

def lfib(n): # last fibonacci series number
  a, b = 0, 1
  for i in range(n-1):
    a, b = b, a+b
  return a

def sfib(n): # sum fibonacci series
  a, b = 0, 1
  for i in range(n+1):
    a, b = b, a+b
  return a-1

def fact(n, i=1):
  fact = 1
  for c in range(n, 1, -i): fact *= c
  return fact

def gcd(*numbers):
  gcd = numbers[0]
  for i in numbers[1:]:
    while i: result, i = i, gcd%i
  return gcd

def lcm(*numbers):
  try:
    lcm = numbers[0]
    for i in range(1, len(numbers)): lcm = lcm*numbers[i]//gcd(lcm, numbers[i])
    return lcm
  except: return 0

def mean(*numbers):
  return sum(numbers) / len(numbers)

def islog(a):
  return type(a)==bool

def isstr(a):
  return type(a)==str

def isnum(a):
  return type(a) in (int, float) or isinstance(a, complex)

def isnan(a): # check if not a number (nan is a number (seriosly))
  return type(a) not in (int, float) or not isinstance(a, complex)

def isbig(n, big=10000000000): # first big number acording to me is 10¹⁰
  return n>=big

def isint(n):
  return type(n)==int

def isfloat(n):
  return type(n)==float

def isnatural(n):
  return type(n)==int and n>0

def iscomplex(n):
  return isinstance(n, complex)

def isreal(n):
  return isinstance(n, complex)==0

def iswhole(n):
  return n%1==0
  
def iseven(n):
  return n%2==0

def isprime(n):
  if n<=1: return False
  for i in range(2, int(n**.5)+1):
    if n%i==0: return False
  return True

def ispos(n):
  return n>0

def isneg(n):
  return n<0

def iszero(n):
  return n==0

def isinf(n):
  return n==float('inf')

def swapsign(number):
  return number * -1

def gamma(number):
  if number == float('inf'): return float('inf')
  elif number == 0: return 1
  if gamma(number) == int(gamma(number)): return int(gamma(number))
  return gamma(number)

def doublegamma(number):
  if number == float('inf'): return float('inf')
  return (gamma(((gamma(number))) - number * (number + 1) / 2 - log(6.283185307179586)  ** 2.718281828459045) / 2) ** 2.718281828459045

def triplegamma(number, step=1e-5):
  if number == float('inf'): return float('inf')
  return (gamma(number + 2 * step) - 2 * gamma(number + step) + gamma(number)) / (step ** 3)

def simplifyfraction(fraction):
  numerator, denominator = map(int, fraction.split('/'))
  div = gcd(numerator, denominator)
  numerator //= div
  denominator //= div
  whole_part = numerator // denominator
  remainder = numerator % denominator
  if whole_part > 0 and remainder > 0: return f'{whole_part} {remainder}/{denominator}'
  elif whole_part > 0: return whole_part
  return f'{numerator}/{denominator}'

def numberlen(number):
  return len(str(number))

def convert(number, to = 'roman'):
  if to.lower() == 'roman':
    result = ''
    for value, numeral in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]: result, number = result + number // value * numeral, number % value
    return result
  elif to.lower() == 'binary':
    if number < 0: return f'-{bin(number)[3:]}'
    return bin(number)[2:]
  elif to.lower() == 'octal':
    if number < 0: return f'-{oct(number)[3:]}'
    return oct(number)[2:]
  elif to.lower() == 'hexadecimal':
    if number < 0: return f'-{hex(number)[3:]}'
    return hex(number)[2:]

def sameelements(*lists):
  return set(lists[0]).intersection(*lists)

def ispalindrome(e):
  return str(e) == str(e)[::-1]

class cryptography():
  def encrypt(text, key = 38):
    result = ''
    for char in text: result += chr((ord(char) + key) % 0x110000)
    return result

  def decrypt(text, key = 38):
    result = ''
    for char in text: result += chr((ord(char) - key) % 0x110000)
    return result

class column():
  def addition(firstnumber, secondnumber):
    result = firstnumber + secondnumber
    firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
    firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
    secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
    return f'{firstnumberspace}{firstnumber}\nᐩ{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

  def subtraction(firstnumber, secondnumber):
    result = firstnumber - secondnumber
    firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
    firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
    secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
    return f'{firstnumberspace}{firstnumber}\n⁻{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

  def multiplication(firstnumber, secondnumber):
    result = firstnumber * secondnumber
    firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
    firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
    secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
    return f'{firstnumberspace}{firstnumber}\n*{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

  def division(firstnumber, secondnumber):
    try: result = firstnumber / secondnumber
    except: result = 'inf'
    firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
    firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
    secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
    return f'{firstnumberspace}{firstnumber}\n÷{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

class triangle():
  def t(a, b, c): # type
    return (a==c)+(b==c)+(a+b>c)
  
  def tn(a, b, c): # type name in english
    return ('invalid', 'versatile', 'isosceles', 'equilateral')[(a==c)+(b==c)+(a+b>c)]

  def p(a, b, c): # perimeter
    return a+b+c

  def s(a, b, c): # semi-perimeter
    return (a+b+c)*.5

  def a(a, b, c): # area
    s = (a+b+c)*.5
    return (s*(s-a)*(s-b)*(s-c))**.5

  def h(a, b, c): # height
    return 2*math.triangle.a(a, b, c)/a

class circle():
  def p(r): # perimeter
    return 6.283185307179586*r

  def s(r): # semi-perimeter
    return 3.141592653589793*r

  def a(r): # area
    return 3.141592653589793*r*r

class os():
  def os():
    if platform == 'linux':
       os = Popen(('lsb_release', '-a'), stdout=-1).communicate()[0].split(b'\n')[1][16:-5]
       return f'{os} GNU/Linux'[2:].replace("'", '')
    return platform

  def uptime(unit = 'm'): # return system uptime
    return perf_counter()*{
      'fs': 1000000000000000,       # femtoseconds
      'ps': 1000000000000,          # picoseconds
      'ns': 1000000000,             # nanoseconds
      'ms': 1000000,                # microseconds
      'Ms': 1000,                   # milliseconds
      's':  1,                      # seconds
      'm':  0.016666666666666666,   # minutes
      'h':  0.0002777777777777778,  # hours
      'd':  1.1574074074074073e-05, # days
      'w':  1.6534391534391535e-06, # weeks
      'f':  8.267195767195768e-07,  # fortnights
      'M':  5.432987360698204e-08,  # months
      'Y':  4.527489467248504e-09   # years
    }[unit]

  def time(unit = 's'): # return time
    return time()*{
      'fs': 1000000000000000,       # femtoseconds
      'ps': 1000000000000,          # picoseconds
      'ns': 1000000000,             # nanoseconds
      'ms': 1000000,                # microseconds
      'Ms': 1000,                   # milliseconds
      's':  1,                      # seconds
      'm':  0.016666666666666666,   # minutes
      'h':  0.0002777777777777778,  # hours
      'd':  1.1574074074074073e-05, # days
      'w':  1.6534391534391535e-06, # weeks
      'f':  8.267195767195768e-07,  # fortnights
      'M':  5.432987360698204e-08,  # months
      'Y':  4.527489467248504e-09   # years
    }[unit]

  def wait(t='1s'):
    fs, ps, ns, ms, Ms, s, m, h, d, w, f, M, Y = 1e-15, 1e-12, 1e-09, 1e-06, .001, 1, 60, 3600, 86400, 604800, 1209600, 18406080, 220872960
    sleep(eval(f"{''.join([char for char in t if char.isdigit() or char == '.'])}*{''.join([char for char in t if not char.isdigit() and char != '.'])}"))

  def do(do):
    system(do)

  def exit():
    exit()

class file():
  def currentfile(path = False):
    if path: return argv[0].replace('\\', '/')
    return argv[0][argv[0].rfind("\\") + 1:]

  def currentdirectory():
    return argv[0][:argv[0].rfind("\\")].replace('\\', '/')

  def exist(name, path = currentdirectory()):
    try: 
      with open(f'{path}/{name}') as afile: return True
    except FileNotFoundError: return False
    except: return True

  def pathexist(path):
    try:
      with open(path) as apath: return True
    except FileNotFoundError: return False
    except: return True

  def content(name, path = currentdirectory()):
    with open(f'{path}/{name}') as afile: return afile.read()

  def isempty(name, path = currentdirectory()):
    try:
      with open(f'{path}/{name}') as afile: return afile.read() == ''
    except UnicodeDecodeError: return False 

  def new(name = 'new', path = currentdirectory()):
    with open(f'{path}/{name}', 'w') as afile: pass

  def overwrite(name, path = currentdirectory(), content = ''):
    if file.exist(name, path):
      with open(f'{path}/{name}', 'w') as afile: afile.write(str(content))

  def rewrite(fromfile, tofile, frompath = currentdirectory(), topath = currentdirectory()):
    if file.exist(fromfile, frompath) and file.exist(tofile, topath):
      with open(f'{frompath}/{fromfile}') as copyfile: copy = copyfile.read()
      with open(f'{topath}/{tofile}', 'w') as afile: afile.write(copy)

  def delete(name, path = currentdirectory()):
    if file.exist(name, path): remove(f'{path}/{name}')

  def extension(name):
    return name[1 + name.rfind('.'):]

  def rename(name, to, path = currentdirectory()):
    if file.exist(name, path): rename(f'{path}/{name}', f'{path}/{to}')

  def hide(name, path = currentdirectory()): # ! WINDOWS ONLY
    if file.exist(name, path): system(f'attrib +h {path}/{name}')

  def show(name, path = currentdirectory()): # ! WINDOWS ONLY
    if file.exist(name, path): system(f'attrib -h {path}/{name}')

  def size(name, apath = currentdirectory()): # Return size in bytes
    return path.getsize(f'{apath}/{name}')

  def symbols(name, apath = currentdirectory()):
    return len(file.content(name, apath))

  def created(name, apath = currentdirectory()):
    return strftime('%d.%m.%Y %H:%M:%S', localtime(path.getctime(f'{apath}/{name}')))

  def motificated(name, apath = currentdirectory()):
    return strftime('%d.%m.%Y %H:%M:%S', localtime(path.getmtime(f'{apath}/{name}')))

class color():
  rainbow = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')    
  names = (
    'absolute zero', 'acid green', 'aero', 'african violet', 'air superiority blue', 'alice blue', 'alizarin', 'alloy orange', 'almond', 'amaranth deep purple', 'amaranth pink', 'amaranth purple', 'amazon', 'amber', 'amethyst', 'android green', 'antique brass', 'antique bronze', 'antique fuchsia', 'antique ruby', 'antique white', 'apricot', 'apple', 'apricot', 'aqua', 'aquamarine', 'arctic lime', 'artichoke green', 'arylide yellow', 'ash grey', 'atomic tangerine', 'aureolin', 'army green', 'azure',
    'baby blue', 'baby blue eyes', 'baby pink', 'baby powder', 'baker-miler pink', 'banana mania', 'barn red', 'battleship grey', 'beau blue', 'beaver', 'beige', "b'dazzled blue", "big dip o'ruby", 'bisque', 'bistre', 'bistre brown', 'bitter lemon', 'black', 'black bean', 'black coral', 'black olive', 'black shadows''blanched almond', 'blast-off bronze', 'bleu de France', 'blizzard blue', 'blood red', 'blue', 'blue (crayola)', 'blue (munsell)', 'blue (NCS)', 'blue (pantone)', 'blue (pigment)', 'blue bell', 'blue-gray (crayola)', 'blue jeans', 'blue sapphire', 'blue-violet', 'blue yonder', 'bluetiful', 'blush', 'bole', 'bone', 'brick red', 'bright lilac', 'bright yellow (crayola)', 'bronze', 'brown', 'brown suggar', 'bud green', 'buff', 'burgundy', 'burlywood', 'burnished brown', 'burnt orange', 'burnt sienna', 'burnt umber', 'byzantine', 'buzantium'
    'cadet blue', 'cadet grey', 'cadmium green', 'cadmium orange', 'café au lait', 'café noir', 'cambridge blue', 'camel', 'cameo pink', 'canary', 'canary yellow', 'candy pink', 'cardinal', 'caribbean green', 'carmine', 'carnation pink', 'carnelian', 'carolina blue', 'carrot orange', 'catawba', 'cedar chest', 'celadon', 'celeste', 'cerise', 'cerulean', 'cerulean blue', 'cerulean frost', 'cerulean (crayola)', 'champagne', 'champagne pink', 'charcoal', 'charm pink', 'chartreuse', 'chartreuse (web)', 'cherry blossom pink', 'chestnut', 'chili red', 'china pink', 'chinese red', 'chinese violet', 'chinese yellow', 'chocolate (traditional)', 'chocolate (web)', 'cinereous', 'cinnabar', 'cinnamon satin', 'citrine', 'citron', 'claret', 'coffee', 'columbia blue', 'congo pink', 'cool gray', 'copper', 'copper (crayola)', 'copper penny', 'copper red', 'copper rose', 'coquelicot', 'coral', 'coral pink', 'cordovian', 'corn', 'cornflower blue', 'cornsilk', 'cosmic cobalt', 'cosmic latte', 'coyote brown', 'cotton candy', 'cream', 'crimson', 'crimson (UA)', 'cultured pearl', 'cyan', 'cyan (process)', 'cyber grape', 'cyber yellow', 'cyclamen',
    'dark brown', 'dark byzantium', 'dark blue', 'dark cyan', 'dark electric blue', 'dark goldenrod', 'darkgreen (x11)', 'darkgreen', 'darkgrey', 'dark jungle green', 'dark khaki', 'dark lava', 'dark liver (horses)', 'dark magenta', 'dark olive green', 'dark orange', 'dark orchid', 'dark purple', 'dark red', 'dark salmon', 'dark sea green', 'dark sienna', 'dark sky blue', 'dark slate blue', 'dark slate gray', 'dark spring green', 'dark turquoise', 'dark violet', "davy's grey", 'deep cerise', 'deep champagne', 'deep chestnut', 'deep jungle green', 'deep pink', 'deep saffron', 'deep sky blue', 'deep space sparkle', 'deep taupe', 'denim', 'denim blue', 'desert', 'desert sand', 'dim gray', 'dodger blue', 'drab dark brown', 'duke blue', 'dutch white',
    'ebony', 'ecru', 'eerie black', 'eggplant', 'eggshell', 'electric lime', 'electric purple', 'electric violet', 'emerald', 'eminence', 'english lavender', 'english red', 'english vermilion', 'english violet', 'erin', 'eton blue',
    'fallow', 'falu red', 'fandango', 'fandango pink', 'fawn', 'fern green', 'field drab', 'fiery rose', 'finn', 'firebrick', 'fire engine red', 'flame', 'flax', 'flirt', 'floral white', 'forest green', 'french beige', 'french bistre', 'french blue', 'french fuchsia', 'french lilac', 'french lime', 'french mauve', 'french pink', 'french raspberry', 'french sky blue', 'french violet', 'frostbite', 'fuchsia', 'fuchsia (crayola)', 'fulvous', 'fuzzy wuzzy',
    'gainsboro', 'gamboge', 'generic viridan', 'ghost white', 'glaucous', 'glossy grape', 'go green', 'gold (metallic)', 'gold (crayola)', 'gold fusion', 'golden', 'golden brown', 'golden poppy', 'golden yellow', 'goldenrod', 'gotham green', 'granite gray', 'granny smith apple', 'grey (web)', 'grey (X11)', 'green', 'green (crayola)', 'green (web)', 'green (munsell)', 'green (NCS)', 'green (pantone)', 'green (pigment)', 'green-blue',  'green-yellow', 'green lizard', 'green sheen', 'gunmetal',
    'hansa yellow', 'harlequin', 'harvest gold', 'heat wave', 'heliotrope', 'heliotrope gray', 'hollywood cerise', 'honolulu blue', "hooker's green", 'hot magenta', 'hot pink', 'hunter green', 'honeydew',
    'iceberg', 'illuminating emerald', 'imperial red', 'inchworm', 'independence', 'india green', 'indian red', 'indian yellow', 'indigo', 'indigo dye', 'international klein blue', 'international orange (engineering)', 'international orange (golden gate bridge)', 'irresistible', 'isabelline', 'italian sky blue', 'indianred', 'indigo', 'ivory',
    'japanese carmine', 'japanese violet', 'jasmine', 'jazzberry jam', 'jet', 'jonquil', 'june bud', 'jungle green',
    'kelly green', 'keppel', 'key lime', 'khaki', 'kobe', 'kobi', 'kobicha', 'KSU purple'
    'languid lavender', 'lapis lazuli', 'laser lemon', 'laurel green', 'lava', 'lavender (floral)', 'lavender (web)', 'lavender blue', 'lavender blush', 'lavender gray', 'lawn green', 'lemon', 'lemon chiffon', 'lemon curry', 'lemon glacier', 'lemon meringue', 'lemon yellow', 'lemon yellow (crayola)', 'liberty', 'light blue', 'light coral', 'light cornflower blue', 'light cyan', 'light french beige', 'light goldenrod yellow', 'light gray', 'light green', 'light orange', 'light periwinkle', 'light khaki', 'light pink', 'light salmon', 'light sea green', 'light sky blue', 'light slate gray', 'light steel blue', 'light yellow', 'lilac', 'lilac luster', 'lime (color whell)', 'lime x11 (web)', 'lime green', 'lincoln green', 'linen', 'lion', 'liseran purple', 'little boy blue', 'liver', 'liver (dogs)', 'liver (organ)', 'liver chestnut', 'livid',
    'macaroni and cheese', 'madder lake', 'magenta', 'magenta (crayola)', 'magenta (dye)', 'magenta (pantone)', 'magenta (process)', 'magenta haze', 'magic mit', 'magnolia', 'mahogany', 'maize', 'maize (crayola)', 'majorelle blue', 'malachite', 'manatee', 'mandarin', 'mango', 'mango tango', 'mantis', 'mardi gras', 'marigold', 'maroon (crayola)', 'maroon (web)', 'maroon x11', 'mauve', 'mauve taupe', 'mauvelous', 'maximum blue', 'maximum blue green', 'maximum blue purple', 'maximum green', 'maximum green yellow', 'maximum purple', 'maximum red', 'maximum red purple', 'maximum yellow', 'maximum yelow red', 'may green', 'maya blue', 'medium aquamarine', 'medium blue', 'medium candy apple red', 'medium carmine', 'medium champagne', 'medium orchid', 'medium purple', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet-red', 'mellow apricot', 'mellow yellow', 'melon', 'metallic gold', 'metallic seaweed', 'metallic sunburst', 'mexican pink', 'middle blue', 'middle blue green', 'middle blue purple', 'middle grey', 'middle green', 'middle green yellow', 'middle purple', 'middle red', 'middle red purple', 'middle yellow', 'middle yellow red', 'midnight' 'midnight blue', 'midnight green (eagle green)', 'mikado yellow', 'mimi pink', 'mindaro', 'ming', 'minion yellow', 'mint', 'mint cream', 'mint green', 'mistry moss', 'misty rose', 'moccasin', 'mode beige', 'mona lisa', 'morning blue', 'moss green', 'mountain meadow', 'mountbatten pink', 'MSU green', 'mulberry', 'mulberry (crayola)', 'mustrad', 'myrtle green', 'mystic', 'mystic maroon',
    'nadeshiko pink',  'naples yellow',  'navajo white', 'navy blue', 'navy blue (Crayola)', 'neon blue', 'neon green', 'neon fuchisia', 'new york pink', 'nikel', 'non-photo blue', 'nyanza',
    'ochre', 'old burgundy', 'old gold', 'old lace', 'old lavender', 'old mauve', 'old rose', 'old silver', 'olive', 'olive drab #3', 'olive drab #7', 'olive green', 'olivine', 'onyx', 'opal', 'opera mauve', 'orange', 'orange (crayola)', 'orange (Pantone)', 'orange (web)', 'orange peel', 'orange-red', 'orange-red (Crayola)', 'orange soda', 'orange-yellow', 'orange-yellow (crayola)', 'orchid', 'orchid pink', 'orchid (crayola)', 'outer space (crayola)', 'outrageous orange', 'oxblood', 'oxford blue', 'ou crimson red',
    'pacific blue', 'pakistan green', 'palatinate purple', 'pale aqua', 'pale cerulean', 'pale dogwood', 'pale pink', 'pale purple (pantone)', 'pale spring bud', 'pansy purple', 'paolo veronese green', 'papaya whip', 'paradise pink', 'parchment', 'paris green', 'pastel pink', 'patriarch', 'paua', "payne's grey", 'peach', 'peach (crayola)', 'peach puff', 'pear', 'pearly purple', 'periwinkle', 'periwinkle (crayola)', 'permanent geranium lake', 'persian blue', 'persian green', 'persian indigo', 'persian orange', 'persian pink', 'persian plum', 'persian red', 'persian rose', 'persimmon', 'pewter blue', 'phlox', 'phthalo blue', 'phthalo green', 'picotee blue', 'pictorial carmine', 'piggy pink', 'pine green', 'pine tree', 'pink', 'pink (pantone)', 'pink lace', 'pink lavender', 'pink sherbet', 'pistachio', 'platinum', 'plum', 'plum (web)', 'plump purple', 'polished pine', 'pomp and power', 'popstar', 'portland orange', 'powder blue', 'princeton orange', 'process yellow', 'prune', 'prussian blue', 'psychedelic purple', 'puce', 'pullman brown', 'pumpkin', 'purple', 'purple (web)', 'purple (munsell)', 'purple x11', 'purple mountain majesty', 'purple navy', 'purple pizzazz', 'purple plum', 'purpureus',
    'queen blue', 'queen pink', 'quick silver', 'quinacridone magenta'
    'radical red', 'raisin black', 'rajan', 'raspberry', 'raspberry glacé', 'raspberry rose', 'raw sienna', 'raw umber', 'razzle dazzle rose', 'razzmatazz', 'razzmic berry', 'rebecca purple', 'red', 'red (crayola)', 'red (munsell)', 'red (ncs)', 'red pantone', 'red (pigment)', 'red (ryb)', 'red-orange', 'red-orange (crayola)', 'red-orange (color wheel)', 'red-purple', 'red salsa', 'red-violet', 'red-violet (crayola)', 'red-violet (color wheel)', 'redwood', 'redolution blue', 'rhythm', 'rich black', 'rhich black (fogra 29)', 'rich black (fogra 39)', 'rifle green', 'robin egg blue', 'rocket metallic', 'rojo spanish red', 'roman silver', 'rose', 'rose bondon', 'rose dust', 'rose ebony', 'rose madder', 'rose pink', 'rose pompadour', 'rose red', 'rose taupe', 'rose vale', 'rosewood', 'rosso corsa', 'rosy brown', 'royal blue (dark)', 'royal blue (light)', 'royal purple', 'royal yellow', 'ruber', 'rubine red', 'ruby', 'ruby red', 'rufous', 'russet', 'russian green', 'russian violet', 'rust', 'rustly red',
    'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue',
    'tan', 'teal', 'thistle', 'tomato', 'turquoise',
    'violet',
    'wheat', 'white', 'whitesmoke',
    'xanadu', 'xantihic', 'xanthous'
    'yellow', 'yellowgreen',
    'zaffre', 'zebra', 'zomp'
  )

  def rgbtohex(red, green, blue):
    return '#{:02X}{:02X}{:02X}'.format(red, green, blue)

  def hextorgb(hexadecimal, to = 'string'): # Returns a tuple with 3 numbers from 0 to 255
    hexadecimal = hexadecimal.lstrip('#')
    red, green, blue = int(hexadecimal[:2], 16), int(hexadecimal[2:4], 16), int(hexadecimal[4:], 16)
    if to == 'tuple': return red, green, blue
    elif to == 'list': return [red, green, blue]
    return f"{red}, {green}, {blue}"

class language():
  def group(text):
    cyrillic = ['Ё', 'Є', 'І', 'Ї', 'Ў', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', 'є', 'і', 'ї', 'ў', 'Ґ', 'ґ', 'Ђ', 'ђ', 'Љ', 'љ', 'Њ', 'њ', 'Ћ', 'ћ', 'Џ', 'џ', 'Đ', 'đ', 'Nj', 'nj', 'Ә', 'ә', 'Ғ', 'ғ', 'Қ', 'қ', 'Ң', 'ң', 'Ө', 'ө', 'Ұ', 'ұ', 'Ү', 'ү', 'Һ', 'һ', 'Ѓ', 'ѓ', 'S', 'ѕ', 'Ќ', 'ќ']
    latin = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    arabic = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']
    greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
    if operations.sameelements(cyrillic, list(text)) > operations.sameelements(latin, list(text)) and  operations.sameelements(cyrillic, list(text)) > operations.sameelements(arabic, list(text)): return 'Cyrillic'
    elif operations.sameelements(latin, list(text)) > operations.sameelements(cyrillic, list(text)) and operations.sameelements(latin, list(text)) > operations.sameelements(arabic, list(text)): return 'Latin'
    elif operations.sameelements(greek, list(text)) > operations.sameelements(cyrillic, list(text)) and operations.sameelements(latin, list(text)) > operations.sameelements(arabic, list(text)): return 'Greek'
    return 'Arabic'

  def detect(text):
    if language.group(text) == 'Cyrillic':
      ukrainianletters = ['є', 'і', 'ї', 'ґ', 'щ', "'"]
      ukrainianіnclusions = ['ти', 'це', 'чи', 'що', 'як', 'його', 'був', 'була', 'було', 'були', 'вони', 'вона', 'весь', 'все', 'де', 'дуже', 'коли', 'моя', 'себе', 'своє', 'себе', 'та', 'також', 'тебе', 'теж', 'тих', 'той', 'тою', 'тому', 'того', 'цей', 'цим', 'цього', 'цьому', 'чого', 'чому', 'яка', 'який', 'яке', "ти", "тись", "тисячи", "тисьсяч"]
      ukrainianendings = ['и','о', 'ю', 'я', 'ам', 'ям', 'ому', 'ою', 'ею', 'ем', 'ько']
      belorusianletters = ['ў']
      belorusianinclusions = ['жы', 'шы', 'щы']
      serbianletters = ['ђ', 'љ', 'њ', 'ћ', 'џ', 'j', 'đ']
      macedonianletters = ['ѓ', 'ѕ', 'ќ']
      kazahletters = ['ә', 'ғ', 'қ', 'ң', 'ө', 'ұ', 'ү', 'һ']
      if list(set(list(text.lower())) & set(belorusianletters)) or any(word in text.lower() for word in belorusianinclusions): return 'Belorusian'
      elif list(set(list(text.lower())) & set(serbianletters)): return 'Serbian'
      elif list(set(list(text.lower())) & set(macedonianletters)): return 'Macedonian'
      elif list(set(list(text.lower())) & set(kazahletters)): return 'Kazah'
      elif list(set(list(text.lower())) & set(ukrainianletters)) or any(word in text.lower() for word in ukrainianіnclusions) or any(text.endswith(end) for end in ukrainianendings): return 'Ukrainian'
      return 'Russian'
    elif language.group(text) == 'Latin':
      germanletters = ['ä', 'ö', 'ü', 'ẞ', 'ß']
      germanіnclusions = ['du', 'sie', 'bin', 'ist', 'hase', 'mit', 'der', 'die', 'das', 'ein', 'eine', 'auf', 'nein', 'gut', 'kein', 'da', 'sehr', 'zu', 'sch']
      francianletters = ['â', 'ç', 'é', 'è', 'î', 'ô', 'ù']
      espanianletters = ['ñ', 'ú']
      czechletters = ['č', 'ě', 'ř', 'ů', 'í', 'ý', 'š', 'ž']
      czechinclusions = ['ov']
      polishletters = ['ą', 'ę', 'ć', 'ś', 'ń', 'ł', 'ó', 'ź', 'ż']
      polishіnclusions = ['cz', 'dz', 'sz', 'rz', 'pan', 'tak', 'nie', 'co', 'ski', 'jest']
      if list(set(list(text.lower())) & set(germanletters)) or any(word in text.lower() for word in germanіnclusions): return 'German'
      elif list(set(list(text.lower())) & set(francianletters)): return 'Francian'
      elif list(set(list(text.lower())) & set(espanianletters)): return 'Espanian'
      elif list(set(list(text.lower())) & set(czechletters)) or any(word in text.lower() for word in czechinclusions): return 'Czech'
      elif list(set(list(text.lower())) & set(polishletters)) or any(word in text.lower() for word in polishіnclusions): return 'Polish'
      return 'English'
    elif language.group(text) == 'Greek': return 'Greek'
    return 'Arabian'

  def system():
    return getlocale()[0][:getlocale()[0].find('_')]
