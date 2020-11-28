#################################################
# hw6b.py
#
# Name:
# Andrew Id: 
#################################################

import cs112_f20_week6_linter
import basic_graphics
import string, copy, random, math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

#################################################
# hw6b-standard
#################################################

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

def getScore(word, letterScores):
  sum = 0
  index = 1
  for c in word:
    index = ord(c) - ord('a')
    sum += letterScores[index]
  return sum


def bestScrabbleScore(dictionary, letterScores, hand):
  best_word = []
  best_score = 0
  for word in dictionary:
    if canMakeWord(word, hand):
      score = getScore(word, letterScores)
      if score >= best_score:
        best_score = score
        best_word.append(word)
  return (best_word, best_score)


def getConsonantCount(text):
  sum = 0
  for c in text:
    consonants = "qwrtyplkjhgfdszxcvbnm"
    if c in consonants:
      sum += 1
  return sum

def getVowelCount(text):
  sum = 0
  for c in text:
    if c in "aeiou":
      sum += 1
  return sum

def getOtherCount(text): 
  sum = 0
  for c in text:
    if c in string.punctuation or c.isdigit():
      sum += 1
  return sum

def getTotalCount(text):
  sum = 0
  for c in text:
    if c.isspace():
      continue
    sum += 1
  return sum

def stringProcessing(text):
  text = text.lower()
  vowelCount = getVowelCount(text)
  otherCount = getOtherCount(text)
  consonantCount = getConsonantCount(text)
  totalCount = getTotalCount(text)
  return vowelCount, otherCount, consonantCount, totalCount

def drawLetterTypePieChart(canvas, text, cx, cy, r):
  titleText = repr(text)
  title = f'Text = \'{titleText}\''
  canvas.create_text(cx, cy - r - 20, text = title, font="arial 18 bold")
  vowelCount, otherCount, consonantCount, totalCount = stringProcessing(text)
  preCount = 0
  if vowelCount == otherCount == consonantCount == 0:
    canvas.create_text(200, 100, text="No data to display")
  if vowelCount != 0:
    drawWedges(canvas, "vowels", vowelCount, totalCount, cx, cy, r,
        preCount, "pink") 
    preCount += vowelCount
  if consonantCount != 0:
    drawWedges(canvas, "consonants", consonantCount, totalCount, cx, 
        cy, r, preCount, "cyan") 
    preCount += consonantCount
  if otherCount != 0:
    drawWedges(canvas, "others", otherCount, totalCount, cx, cy, r, 
        preCount, "lightGreen") 

def drawWedges(canvas, letterType, lttrCount, totalCount, cx, cy, r,
        preCount, color): 
  beginAngle = 90 + (preCount / totalCount * 360)
  endAngle = (lttrCount / totalCount * 360)
  if endAngle == 360:
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = color)
  else:
    canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start = beginAngle, 
        extent = endAngle,  fill = color)

  #textAngle = (beginAngle + ((endAngle - beginAngle) / 2)) * math.pi / 180
  textAngle = (lttrCount + preCount) / 2 * (math.pi) 
  print(letterType)
  print("beginAngle " + str(beginAngle)) 
  print("endAngle " + str(endAngle)) 
  print("middleAngle " + str((beginAngle + endAngle)/2)) 
  textCx = cx + (r * math.cos(textAngle)) / 2
  textCy = cy - (r * math.sin(textAngle)) /2
  percentCount = int(roundHalfUp((lttrCount / totalCount)) * 100)
  textDisplay = f'{letterType}  ({lttrCount} of {totalCount}, {percentCount}%)'
  canvas.create_text(textCx, textCy, text=textDisplay)
    #case where all the counts are zero, edge case


  #angle = the count of that letter type and the total count
  #voewls first,at 90 degrees
  #counterclockwise, consonants , others

#################################################
# hw6b-bonus
#################################################

def solvesCryptarithm(puzzle, solution):
    return 42

def allSublists(L):
    yield 42

def solveSubsetSum(L):
    return 42

def heapsAlgorithmForPermutations(L):
    # from https://en.wikipedia.org/wiki/Heap%27s_algorithm
    yield 42

def solveCryptarithmWithMaxDigit(puzzle, maxDigit):
    return 42

def getAllSingletonCryptarithmsWithMaxDigit(words, maxDigit):
    return 42

#################################################
# Test Functions
#################################################

def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) ==
                                        (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) ==
                                        None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) ==
                                         (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) ==
                                        (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) ==
                                        ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) ==
                                        ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) ==
                                        None)
    print("Passed!")

def drawLetterTypePieCharts1(canvas, width, height):
    r = min(width,height)*0.2
    canvas.create_line(width/2, 0, width/2, height)
    canvas.create_line(0, height/2, width, height/2)
    drawLetterTypePieChart(canvas, "AB, c de!?!", width/4, height/4, r)
    drawLetterTypePieChart(canvas, "AB e", width/4, height*3/4, r)
    drawLetterTypePieChart(canvas, "A", width*3/4, height/4, r)
    drawLetterTypePieChart(canvas, "               ", width*3/4, height*3/4, r)

def drawLetterTypePieCharts2(canvas, width, height):
    rA = min(width,height)*0.15
    rB = min(width,height)*0.2
    drawLetterTypePieChart(canvas, "aLpHaBeT!", width*0.175, height*0.575, rA)
    drawLetterTypePieChart(canvas, "I ordered 2 eggs & 1 waffle for breakfast!",
                           width/2, height*0.375, rB)
    drawLetterTypePieChart(canvas, "A_E_I_O_U", width*0.825, height*0.575, rA)
    drawLetterTypePieChart(canvas, "#fbrkyz", width*0.5, height*0.8, rA)

def testDrawLetterTypePieChart():
    print('Testing drawLetterTypePieChart()...')
    basic_graphics.run(drawFn=drawLetterTypePieCharts1, width=800, height=800)
    basic_graphics.run(drawFn=drawLetterTypePieCharts2, width=800, height=800)
    print('Do a visual inspection to verify this passed!')

def testSolvesCryptarithm():
    print("Testing solvesCryptarithm()...", end="")
    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY--ENDRS") == 
                                  True)
    # from http://www.cryptarithms.com/default.asp?pg=1
    assert(solvesCryptarithm("NUMBER + NUMBER = PUZZLE", "UMNZP-BLER") ==
                                  True)
    assert(solvesCryptarithm("TILES + PUZZLES = PICTURE", "UISPELCZRT") ==
                                  True)
    assert(solvesCryptarithm("COCA + COLA = OASIS", "LOS---A-CI") ==
                                  True)
    assert(solvesCryptarithm("CROSS + ROADS = DANGER", "-DOSEARGNC") ==
                                  True)

    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY--ENDR-") == False)
    assert(solvesCryptarithm("SEND + MORE = MONEY","OMY-ENDRS") == False)
    assert(solvesCryptarithm("SEND + MORE = MONY","OMY--ENDRS") == False)
    assert(solvesCryptarithm("SEND + MORE = MONEY","MOY--ENDRS") == False)
    print("Passed!")

def testAllSublists():
    print('  Testing allSublists()...', end='')
    def f(): yield 42
    assert(type(allSublists([1,2,3])) == type(f())) # generator
    assert(sorted(allSublists([1])) == [ [], [1] ])
    assert(sorted(allSublists([3, 5])) == [ [], [3], [3, 5], [5] ])
    assert(sorted(allSublists([6,7,8])) == [ [], [6], [6, 7], [6, 7, 8],
                                             [6, 8], [7], [7, 8], [8] ])
    print('Passed!')

def testSolveSubsetSum():
    def checkSubsetSum(L):
        solution = solveSubsetSum(L)
        for v in solution:
            assert(solution.count(v) <= L.count(v))
        assert(sum(solution) == 0)
    print('  Testing solveSubsetSum()...', end='')
    assert(solveSubsetSum([5,2,3,-4]) == None)
    checkSubsetSum([-1,5,2,3,-4])
    checkSubsetSum([8,19,31,27,52,-70,4])
    print('Passed!')

def testHeapsAlgorithmForPermutations():
    print('  Testing heapsAlgorithmForPermutations()...', end='')
    def f(): yield 42
    assert(type(heapsAlgorithmForPermutations([1])) == type(f())) # generator
    assert(sorted(heapsAlgorithmForPermutations([1])) == [[1]])
    assert(sorted(heapsAlgorithmForPermutations([1,2])) == [
            [1,2], [2,1]
        ])
    assert(sorted(heapsAlgorithmForPermutations([3,1,2])) == [
            [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]
        ])
    print('Passed!')

def testSolveCryptarithmWithMaxDigit():
    print('  Testing solveCryptarithmWithMaxDigit()...', end='')
    assert(solveCryptarithmWithMaxDigit('RAM + RAT = ANT', 4) == '''\
RAM + RAT = ANT
120 + 123 = 243''')
    assert(solveCryptarithmWithMaxDigit('ANT + CAT = EEL', 4) == None)
    assert(solveCryptarithmWithMaxDigit('ANT + CAT = EEL', 5) == '''\
ANT + CAT = EEL
125 + 315 = 440''')
    print('Passed!')

def testGetAllSingletonCryptarithmsWithMaxDigit():
    print('  Testing getAllSingletonCryptarithmsWithMaxDigit()...', end='')
    words = ['EEL', 'RAM', 'CAT', 'BEE', 'FLY',
             'HEN', 'RAT', 'DOG', 'ANT']
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 3) == '')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 4) == '''\
RAM + RAT = ANT
120 + 123 = 243''')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 5) == '''\
ANT + CAT = EEL
125 + 315 = 440
ANT + CAT = HEN
105 + 315 = 420
ANT + RAT = EEL
125 + 315 = 440
ANT + RAT = HEN
105 + 315 = 420
BEE + EEL = FLY
411 + 112 = 523''')

    words = ['DEER', 'BEAR', 'GOAT', 'MULE', 'PUMA',
             'COLT', 'ORCA', 'IBEX', 'LION', 'WOLF']
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 5) == '')
    assert(getAllSingletonCryptarithmsWithMaxDigit(words, 6) == '''\
BEAR + DEER = IBEX
4203 + 1223 = 5426
COLT + GOAT = ORCA
4635 + 1605 = 6240''')
    print('Passed!')

def testBonusCombinatoricsProblems():
    print('Testing spicy combinatorics problems...')
    testAllSublists()
    testSolveSubsetSum()
    testHeapsAlgorithmForPermutations()
    testSolveCryptarithmWithMaxDigit()
    testGetAllSingletonCryptarithmsWithMaxDigit()
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    # hw6b-standard
    #testBestScrabbleScore()
    testDrawLetterTypePieChart()
    # hw6b-bonus
    testSolvesCryptarithm()
    testBonusCombinatoricsProblems()

def main():
    cs112_f20_week6_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
