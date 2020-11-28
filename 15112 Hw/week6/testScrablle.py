def canMakeWord(word, hand):
  wordLetters = []
  word = word.lower()
  for c in word:
    wordLetters.append(c) 
  for letter in hand:
    if letter in wordLetters:
      wordLetters.remove(letter)
  if len(wordLetters) > 0:
    return False
  else:
    return True

def getScore(word, LetterScores):
  sum = 0
  index = 1
  for c in word:
    index = ord(c) - ord('a')
    print(LetterScores[index])
    sum += LetterScores[index]
  return sum


def bestScrabbleScore(dictionary, letterScores, hand):
  best_word = []
  best_score = 0
  for word in dictionary:
    if canMakeWord(word, hand):
      score = getScore(word, LetterScores)
      if score >= 0:
        best_score = score
        best_word.append(word)
        print(word)

def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
def letterScores2(): return [1+(i%5) for i in range(26)]

bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) 