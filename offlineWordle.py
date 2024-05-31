### OFFLINE WORDLE SOLVER ### 
import copy

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

def dupPenalty(str):
  dups = 0.0
  count = 0
  hashset = set()

  for char in str:
      if char in hashset:
          count += 1
          dups += letter_frequencies_dict[char]
      hashset.add(char)
  return (count, dups)


def scoreWord(str):
  res = 0
  for char in str:
    res += letter_frequencies_dict[char]

  res -= dupPenalty(str)[0] * 0.1
  res -= dupPenalty(str)[1] * 1  
  return res


# word list from --- https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
# wordle La from --- https://gist.github.com/scholtes/94f3c0303ba6a7768b47583aff36654d
# wordle La is the official words that wordle would use, so I think it makes more sense to test it
word_list = [] 
total_words = 0
f = open("./wordle-La.txt", "r")  # this ones 2000 words
#f = open("./5wordlist.txt", "r") # this ones 5000 words
for word in f:
  total_words += 1
  word_list.append((word.strip(), scoreWord(word.strip()))) # list of (word, score)

word_list.sort(key=lambda x: x[1], reverse=True)


# this was a tricky function
def getResult(answer, guess):
    # start the result as Nones
    result = [None] * 5
    yog_map = {} # same idea as from the cropwordlist function

    for i in range(5):
        # if letter at that index is same for guess and answer, append correct
        if guess[i] == answer[i]:
            if guess[i] not in yog_map:
                yog_map[guess[i]] = 0
            # add to map
            yog_map[guess[i]] += 1
            result[i] = ((guess[i], "correct")) # (green letter)
        
        elif guess[i] not in answer: 
            # can only count as absent if there's no instance of it in answer FOR NOW
            # you'll get why
            result[i] = ((guess[i], "absent")) # (gray letter)
    
    for i in range(5):
        # if the letter is filled already, we skip it
        if(result[i] != None):
           continue 
        
        # if at this index, guess letter != answer letter AND 
        # guess letter is in answer AND
        # YG map value for that letter is less than the total count of that letter in answer
        # then we can say it's present in another position (yellow)
        if guess[i] != answer[i] and guess[i] in answer and yog_map.get(guess[i], 0) < answer.count(guess[i]):
            # cant be in the right spot, and must be contained, and must be less than the amount of those letters in the answer
            if yog_map.get(guess[i], 0) < answer.count(guess[i]): 
                result[i] = ((guess[i], "present in another position")) # (yellow letter)
                if guess[i] not in yog_map:
                    yog_map[guess[i]] = 0
                # add to map
                yog_map[guess[i]] += 1
                # yellows are tricky -- I know, past Justin, yes they are. But you did it. High five.
        else:
           # last case I believe is if answer already has enough of the letter 
           # meaning that: yog_map.get(guess[i], 0) == answer.count(guess[i])
           result[i] = ((guess[i], "absent")) 
    return result 

# same as main.py
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

# use this to run wordle simulation and get success rate
def solve(word_list, answer):
    row = 0
    revised_word_list = copy.deepcopy(word_list) # this gets revised in the while loop
    # don't need deep copy but it looks cool so I'm keeping it
    while row <= 5:
        # Create a list to store tuples of (letter, status)
        label_list = []
        
        guess = revised_word_list[0] # highest ranked word

        print(f"MOVE {row+1} --- Guessing: {guess[0]}")
        label_list = getResult(answer, guess[0]) # guess[0] gives you the word
        print(label_list)
        
        
        if(answer == guess[0]): # really shouldve renamed guess[0] cuz its getting hard to keep track of
        # grab guess var from last loop
        # uninit. var only happens if you guess first try, so you're just cheating if so
            print(f"CONGRATS! CORRECT GUESS IS: {guess[0]}\n\n")
            return True # this works like break yes?
        
        else:
            revised_word_list = cropWordList(revised_word_list, label_list)
            

            #print(revised_word_list), used this for debugging, uncomment if you wanna see the revised list
        row+=1
    print("We have lost\n\n")
    return False # should be false if we never break inside the loop


attempts = 0
success = 0.0
while attempts < total_words: # total_words is set at the top
    set_word = word_list[attempts][0]
    print(f"Set the guess as {set_word}")
    solution = solve(word_list, set_word)
    if solution:
        success+=1
    attempts+=1
    print(f"Attempt: {int(success)}")

success_rate = success / attempts * 100
success_rate = round(success_rate, 4)
print(f"{success_rate}% success rate!")


