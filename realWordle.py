### WORDLE SOLVER ### 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

letter_frequencies = [ # obtained from https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html
    ('a', 0.08167),
    ('b', 0.01492),
    ('c', 0.02782),
    ('d', 0.04253),
    ('e', 0.12702),
    ('f', 0.02228),
    ('g', 0.02015),
    ('h', 0.06094),
    ('i', 0.06966),
    ('j', 0.00153),
    ('k', 0.00772),
    ('l', 0.04025),
    ('m', 0.02406),
    ('n', 0.06749),
    ('o', 0.07507),
    ('p', 0.01929),
    ('q', 0.00095),
    ('r', 0.05987),
    ('s', 0.06327),
    ('t', 0.09056),
    ('u', 0.02758),
    ('v', 0.00978),
    ('w', 0.02360),
    ('x', 0.00150),
    ('y', 0.01974),
    ('z', 0.00074)
]

# convert to dict for easy access
letter_frequencies_dict = dict(letter_frequencies) 

# find duplicate letters in the word
def dupPenalty(str):
  letter_penalty = 0.0
  count = 0
  hashset = set()

  for char in str:
      if char in hashset:
          count += 1
          letter_penalty += letter_frequencies_dict[char]
          # count the dups and the indv. freq. of the dup letter
      hashset.add(char)
  return (count, letter_penalty)

# score word based on the frequency of the letters minus penalties
def scoreWord(str):
  res = 0
  for char in str:
    res += letter_frequencies_dict[char]

  res -= dupPenalty(str)[0] * 0.1
  res -= dupPenalty(str)[1] * 1  # might have to tweak this value
  # subtract the count of dups 
  # and subtract the frequency of the individual duplicate letter
    # I thought that adding the indv. letter would be better, somehow
    # subtracting the indv. letter freq. yields higher success rate
  return res



# 5wordlist from --- https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
# wordle-La from --- https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d
word_list = [] 
#f = open("./5wordlist.txt", "r") # this one has 5000 words
f = open("./wordle-La.txt", "r")  # this one has 2000 words
for word in f:
  # list of (word, score)
  word_list.append((word.strip(), scoreWord(word.strip())))
# sort based on the score of the word
word_list.sort(key=lambda x: x[1], reverse=True)

# annoying Chrome stuff
def startChromeStuff():
  cService = webdriver.ChromeService(executable_path='./chromedriver-mac-arm64/chromedriver')
  driver = webdriver.Chrome(service = cService)

  url="https://www.nytimes.com/games/wordle/index.html"
  driver.get(url)

  time.sleep(1) # these sleeps account for the annoying animation delay of the site

  try: 
    # put tries everywhere because if it can't find the element
    # the program has a panic attack and just closes chrome
    # which personally I wouldn't freak out like that, I'd be more chill about it
    theButton = driver.find_element(By.XPATH, "//button[@class='Welcome-module_button__ZG0Zh']") # click play button
    theButton.click()
  except:
    print("cant find where to click")

  time.sleep(1) 

  try:
    # a million buttons to click before we can actually enter the game thanks NYT
    theXButton = driver.find_element(By.XPATH, "//button[@class='Modal-module_closeIcon__TcEKb']")
    theXButton.click()
  except:
    print("cant find where to click")

  time.sleep(1)
  return driver # return this for use outside the function



driver = startChromeStuff() # start the chrome stuff and get the driver from it
#first guess 
input_field = driver.find_element(By.XPATH, "//*[@class='Key-module_key__kchQI']")
firstGuess = word_list[0][0] # use highest ranked word 
input_field.send_keys(firstGuess)
print(f"Guessing: {firstGuess}")

try:
  # tried to send_keys(ENTER) but was having issues I just used on-screen keyboard 
  enter = driver.find_element(By.XPATH, "//*[@class='Key-module_key__kchQI Key-module_oneAndAHalf__bq8Tw']")
  enter.click()
except:
  print("cant find where to click")

time.sleep(2)

# revise the word list based on the colors we receive
def cropWordList(revised_word_list, guess): 
  letter_idx = 0 # this will track what letter we're at in the word
  yellow_green_map = {} # this keeps track of any Y or G spaces 

  for pair in guess: # pair is a letter remember, not a word
    letter = pair[0].lower() # lowercase to standardize to the word list
    
    if pair[1] == 'correct': # (green letter)
      if letter not in yellow_green_map:
        yellow_green_map[letter] = 0
      yellow_green_map[letter] += 1 
      # keep all words with that have letter in that index
      revised_word_list = [word for word in revised_word_list if word[0][letter_idx] == letter] 
    
    elif pair[1] == 'present in another position': # (yellow letter)
      if letter not in yellow_green_map:
        yellow_green_map[letter] = 0
      yellow_green_map[letter] += 1
      # keep all words with that letter not in that index
      revised_word_list = [word for word in revised_word_list if letter in word[0] and word[0][letter_idx] != letter] # keep words that have that letter
  
    elif pair[1] == 'absent': # (gray letter)
      # keep all words where the letter in this index is not the letter
      # more revisions to be made after the first pass (we need to fully populate the y_g_map)
      revised_word_list = [word for word in revised_word_list if word[0][letter_idx] != letter]
      
    # had to add the [0] after all the word references because the word_list is a list of tuples
    # such a headache
    letter_idx+=1
    
  # after the loop, we remove words without the specific number of letters that show up in the yog list
  for letter, count in yellow_green_map.items(): # revise based on the counts in the list
    # for all letters in the map, keep all words where the amount of those letters in the word are >= count (in map)
    revised_word_list = [word for word in revised_word_list if word[0].count(letter) >= count]   
  
  for pair in guess: 
    letter = pair[0].lower()
    if pair[1] == 'absent':
      if letter not in yellow_green_map:  
        # for all letters marked 'absent', if they don't show up at all in the word
        # then we keep all words with no instance of that letter
        # this is only possible after a full population of the YG map 
        revised_word_list = [word for word in revised_word_list if letter not in word[0]]

  return revised_word_list

                                                                  
# row start at 1 since we did first guess already
row = 1
while row <= 6:
    # another break because I think correct_guess is being set as false somehow
    try:
        if correct_guess == True:
            print(f"CONGRATS! CORRECT GUESS IS: {guess}")
            break
    except NameError:
        pass
    
    # parse from the row we're at
    parent_section = driver.find_element(By.XPATH, f"//div[@aria-label='Row {row}']")
    # Find child elements within the parent section, only returning the letters from specific row
    child_elements = parent_section.find_elements(By.XPATH, ".//div[@class='Tile-module_tile__UWEHN']")

    # Create a list to store tuples of (letter, status)
    label_list = []

    # start this out as true, then any incorrect answer will turn this off
    correct_guess = True 
    
    for child in child_elements:
      # Find the substring that contains the information
      child_html = str(child.get_attribute("outerHTML"))
      # HTML looks like: " aria-label="1st letter, S, present in another position" data... "
      # so we take the text from the aria-label
      start_index = child_html.find('letter,') + len('letter,') 
      end_index = child_html.find('" ', start_index) 
      label_substring = child_html[start_index:end_index]
      
      # Split the substring by commas and strip whitespace
      label_parts = label_substring.split(',')
      label_parts = [part.strip() for part in label_parts]
      
      letter = label_parts[0].strip()  # idx 1 contains the letter
      status = label_parts[1].strip()  # idx 2 contains the status

      # use this to break if we guess correct
      if status != 'correct': 
        correct_guess = False

      # use this label list to revise the word list
      label_list.append((letter, status))
    
    
    if row < 6 and correct_guess == False: # get congrats message above, only continue past that if we're not at last row
      word_list = cropWordList(word_list, label_list)
      
      try:
        # grab the best ranked word
        guess = word_list[0][0]
        input_field.send_keys(guess)
      except:
        print("Index Error")

      print(f"Guessing: {guess}")

      # click enter
      try:
        enter = driver.find_element(By.XPATH, "//*[@class='Key-module_key__kchQI Key-module_oneAndAHalf__bq8Tw']")
        enter.click()
      except:
        print("cant find where to click")

      time.sleep(2)

      row+=1

time.sleep(3)
if correct_guess == False:  
  print("We have lost :(")

# Just click the two X's after the game ends because why would playing the game be easy?
# I actually enjoying clicking 12 X's after I play to view my results  
try:
  anotherXButton = driver.find_element(By.XPATH, "//button[@class='Modal-module_closeIconButton__y9b6c']")
  anotherXButton.click()    
except:
  print("cant find where to click")

try:
  yetAnotherXButton = driver.find_element(By.XPATH, "//button[@class='Modal-module_closeIconButton__y9b6c']")
  yetAnotherXButton.click()    
except:
  print("cant find where to click")

# quit
input("Type Q to quit: ")






