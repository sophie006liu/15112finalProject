import basic_graphics, math, string

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

def drawText(canvas, letterType, letterCount, totalCount, cx, cy, r, preCount):
  textAngle = ((letterCount + preCount) / (2 * totalCount)) * (math.pi * 2)
  textCx = cx + (r * math.cos(textAngle)) / 2
  textCy = cy #- (r * math.sin(textAngle)) /2
  print(letterType)
  print((letterCount + preCount) / (2 * totalCount))
  print(textAngle)
  percentCount = int(round((letterCount / totalCount), 2) * 100)
  textDisplay = f'{letterType}  ({letterCount} of {totalCount}, {percentCount}%)'
  canvas.create_text(textCx, textCy, text=textDisplay)

def drawWedges(canvas, letterType, letterCount, totalCount, cx, cy, r, preCount, color): 
  beginAngle = 90 + (preCount / totalCount * 360)
  endAngle = (letterCount / totalCount * 360)
  if endAngle == 360:
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = color)
  else:
    canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start = beginAngle, extent = endAngle,  fill = color)
  drawText(canvas, letterType, letterCount, totalCount, cx, cy, r, preCount)
  #textAngle = (beginAngle + ((endAngle - beginAngle) / 2)) * math.pi / 180
  
    #case where all the counts are zero, edge case


  #angle = the count of that letter type and the total count
  #voewls first,at 90 degrees
  #counterclockwise, consonants , others
def drawLetterTypePieChart(canvas, text, cx, cy, r):
  titleText = repr(text)
  title = f'Text = \'{titleText}\''
  canvas.create_text(cx, cy - r - 20, text = title, font="arial 18 bold")
  vowelCount, otherCount, consonantCount, totalCount = stringProcessing(text)
  preCount = 0
  if vowelCount == otherCount == consonantCount == 0:
    canvas.create_text(200, 100, text="No data to display")
  if vowelCount != 0:
    drawWedges(canvas, "vowels", vowelCount, totalCount, cx, cy, r, preCount, "pink") 
    preCount += vowelCount
  if consonantCount != 0:
    drawWedges(canvas, "consonants", consonantCount, totalCount, cx, cy, r, preCount, "cyan") 
    preCount += consonantCount
  if otherCount != 0:
    drawWedges(canvas, "others", otherCount, totalCount, cx, cy, r, preCount, "lightGreen") 

def drawLetterTypePieCharts2(canvas, width, height):
    rA = min(width,height)*0.15
    rB = min(width,height)*0.2
    drawLetterTypePieChart(canvas, "aLpHaBeT!", width*0.175, height*0.575, rA)
    #drawLetterTypePieChart(canvas, "I ordered 2 eggs & 1 waffle for breakfast!",
                           #width/2, height*0.375, rB)
    #drawLetterTypePieChart(canvas, "A_E_I_O_U", width*0.825, height*0.575, rA)
    #drawLetterTypePieChart(canvas, "#fbrkyz", width*0.5, height*0.8, rA)

basic_graphics.run(drawFn=drawLetterTypePieCharts2, width=800, height=800)

