# Wordle Solver <img src="https://github.com/jjhassy/wordle_solver/assets/66802155/1be7a89e-3356-46ce-94a1-f0b5ff9fe2e2" height = "20" width="200"/>
## Description




  This is a script that solves the Wordle. It opens Chrome and everything. Fully hands off. Sit back, relax, and let my script solve it for you. You can also test it offline to see that the logic I use has a 98% success rate (~91% if you use the bigger word list). The logic is elementary. If a letter is green, only words with that letter in that spot are considered. Yellow, keep words that have that letter, just not in that spot. Etc. etc. 
  


  **How did I pick words?** I scored the words based on the sum of the frequencies of the individual letters then choose the highest ranked word. I also penalized the score slightly if there were duplicate letters. I could have done strategies that knock out a bunch of common letters first or some other logic that is cooler, but I didn't. 91-98% rate isn't terrible though. 
  I guess you could say that it plays the game in Wordle Hard Mode (all revealed letters must be used in subsequent guesses).
  
  The Chrome interactions I followed mostly from this typings.gg solver script: https://github.com/woosalexe/typingsgg-hack/blob/master/typingsgg.py, working with HTML is extremely annoying. Other sources like where I got the word list and the frequencies of letters are commented in the code. 
  
  Overall, I enjoyed this project. Cool stuff I'm proud of using in this project: *dictionaries, sets, maps, file reading, lambda function, selenium webdriver stuff, and a lot of swag (used a bunch of that).*  
  
  
  
## How to run
- Clone the repo.
- The chromedriver is for Mac, so if that's not you, find you appropriate chromedriver download at https://googlechromelabs.github.io/chrome-for-testing/#stable and put it in the directory of the repo.
- Run the **realWordle.py** to automatically open up Chrome and solve the wordle.
- Run the **offlineWordle.py** to test with thousands of random 5 letter words to see the success rate of the script logic.
- You could fiddle with **offlineWordle.py** to test with your specific input instead of 2000+ random guesses to see how well it guesses specific words.

## realWordle.py Demo
https://github.com/jjhassy/wordle_solver/assets/66802155/04f23430-305a-4509-8839-29177ff890a6

## offlineWordle.py Output
<img src="https://github.com/jjhassy/wordle_solver/blob/387cf5d2d67ae120873ebd4afffe4f7d39e31a64/screenshot.png" width="900" height="300" />




