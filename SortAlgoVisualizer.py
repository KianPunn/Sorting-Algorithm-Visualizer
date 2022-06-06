import sys, pygame
import random
pygame.init()  # Initializes all the pygame modules

class DisplayInfos:
    # Constant Variables
    LIME_GREEN = 50, 205, 50
    SCARLET = 255, 36, 0
    RAVEN = 20, 26, 22
    CROW = 21, 35, 36
    COLOR1 = 124, 202, 213
    COLOR2 = 160, 166, 190
    COLOR3 = 196, 129, 167
    BACKGROUND_COLOR = 255, 250, 250  # RGB Code of color snow

    COLOR_OF_BARS = [COLOR1, COLOR2, COLOR3]

    SIDE_PADDING = 200
    TOP_PADDING = 100

    LARGE_FONT = pygame.font.SysFont('Bahnschrift', 23)
    SMALL_FONT = pygame.font.SysFont('Candara', 15)
    
    # The 'lst' parameter is the list that we're going to sort
    def __init__(self, width, height, lst) -> None:
        self.size = self.width, self.height = width, height  # size of the screen

        self.screen = pygame.display.set_mode(self.size)  # creates the screen/window
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_lst(lst)
    
    def set_lst(self, lst):
        self.lst = lst
        self.smallestVal = min(lst)
        self.largestVal = max(lst)

        # Computes the height and width of the bars depending on their number and with respect to their padding
        self.barHeight = round((self.height - self.TOP_PADDING) / (self.largestVal - self.smallestVal))
        self.barWidth = round((self.width - self.SIDE_PADDING) / len(lst))
        # The bars will start at (100, 0)
        self.startingPointX = self.SIDE_PADDING // 2  

def display(displayInfos, sortingAlgoName, timeComp, ascending):
    # Set the background color of the window
    displayInfos.screen.fill(displayInfos.BACKGROUND_COLOR)

    # The texts 
    titleText = displayInfos.LARGE_FONT.render(f"{sortingAlgoName} | Status: {'Ascending' if ascending else 'Descending' } | Time Complexity: {timeComp}", True, displayInfos.RAVEN)
    text = displayInfos.SMALL_FONT.render("Press [C] to Change | Press [1] to Start Sorting | Press [->] for Ascending | Press [<-] for Descending", True, displayInfos.CROW)
    sortingAlgos = displayInfos.SMALL_FONT.render("Press [B] for Bubble Sort | Press [I] for Insertion Sort | Press [S] for Selection Sort ", True, displayInfos.CROW)

    displayInfos.screen.blit(titleText, (displayInfos.width // 2 - titleText.get_width() // 2, 5))
    displayInfos.screen.blit(text, (displayInfos.width // 2 - text.get_width() // 2, 45))
    displayInfos.screen.blit(sortingAlgos, (displayInfos.width // 2 - sortingAlgos.get_width() // 2, 65))

    displayBars(displayInfos)
    pygame.display.update()

def displayBars(displayInfos, color={}, clearBg=False):
    lst = displayInfos.lst

    if clearBg == True:
        clearRect = (displayInfos.SIDE_PADDING // 2, displayInfos.TOP_PADDING, 
                    displayInfos.width - displayInfos.SIDE_PADDING, displayInfos.height - displayInfos.TOP_PADDING)
        pygame.draw.rect(displayInfos.screen, displayInfos.BACKGROUND_COLOR, clearRect)

    # A loop that gets the index and the value of elements inside the lst
    for i, v in enumerate(lst):
        x = displayInfos.startingPointX + i * displayInfos.barWidth  # If the index is 0, then the bar will display at the starting point (100, 0)
        y = displayInfos.height - (v - displayInfos.smallestVal) * displayInfos.barHeight  # Computes the height of the bar to determine where is the starting point of drawing (draw downwards)

        barColors = displayInfos.COLOR_OF_BARS[i % 3]  # Gives different colors for every 3 consecutive bars

        if i in color:
            barColors = color[i]

        pygame.draw.rect(displayInfos.screen, barColors, (x, y, displayInfos.barWidth, displayInfos.height))  # Draw the bars to the window
    
    if clearBg == True:
        pygame.display.update()

# Sorting Algorithms
def bubbleSort(displayInfos, ascending=True):
    lst = displayInfos.lst
    n = len(lst)

    for i in range(n-1):
        # The most recent i elements are already sorted, that's why n-i
        for j in range (0, n-i-1):
            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                displayBars(displayInfos, {j:displayInfos.LIME_GREEN, j+1:displayInfos.SCARLET}, True)
            
                yield True
    return lst

def insertionSort(displayInfos, ascending=True):
    lst = displayInfos.lst
    n = len(lst)
    
    for i in range(1, n):
        current = lst[i]
        predecessor = i-1
        while True:
            ascendingOrder = predecessor >= 0 and current < lst[predecessor] and ascending
            descendingOrder = predecessor >= 0 and current > lst[predecessor] and not ascending

            if not ascendingOrder and not descendingOrder:
                break

            lst[predecessor + 1] = lst[predecessor]
            predecessor -= 1
            displayBars(displayInfos, {i:displayInfos.LIME_GREEN, predecessor:displayInfos.SCARLET}, True)
            
            yield True

        lst[predecessor + 1] = current

def selectionSort(displayInfos, ascending=True):
    lst = displayInfos.lst
    n = len(lst)

    for i in range(n):
        idxOfSmallestNum = i
        if ascending:
            for j in range(i+1, n):
                if (lst[idxOfSmallestNum] > lst[j]):
                    idxOfSmallestNum = j      
                displayBars(displayInfos, {i:displayInfos.LIME_GREEN, j:displayInfos.SCARLET}, True)

                yield True
            lst[i], lst[idxOfSmallestNum] = lst[idxOfSmallestNum], lst[i]
        elif not ascending:
            for j in range(i+1, n):
                if (lst[idxOfSmallestNum] < lst[j]):
                    idxOfSmallestNum = j      
                displayBars(displayInfos, {i:displayInfos.LIME_GREEN, j:displayInfos.SCARLET}, True)

                yield True
            lst[i], lst[idxOfSmallestNum] = lst[idxOfSmallestNum], lst[i]
    return lst

# List generator
def listGenerator(n, minVal, maxVal):
    randomList = []
    for i in range(n):
        randomList.append(random.randint(minVal, maxVal))
    return randomList

# Contains an infinite loop that will keep the program running til the user press the X button
def main():
    fps = pygame.time.Clock()

    n = 100
    minVal = 1
    maxVal = 100

    lst = listGenerator(n, minVal, maxVal)
    displayInfos = DisplayInfos(1000, 500, lst)

    # Flag variable that says if the program is sorting or not
    sorting = False
    ascending = True

    sortingAlgorithm = None
    sortingAlgorithmName = "Sorting Algorithm Visualizer"
    sortingAlgorithmTimeComp = None
    sortingAlgorithmGenerator = None

    while True:
        fps.tick(160)

        if sorting == True:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                sorting = False
        else:
            display(displayInfos, sortingAlgorithmName, sortingAlgorithmTimeComp, ascending)

        # If the user click the X button in the window, the program will close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            
            if event.type != pygame.KEYDOWN:
                continue

            # Gives a new list when the user press [C]
            if event.key == pygame.K_c:
                lst = listGenerator(n, minVal, maxVal)
                displayInfos.set_lst(lst)
                sorting = False

            # Sorting Options
            elif event.key == pygame.K_b:
                sortingAlgorithm = bubbleSort
                sortingAlgorithmTimeComp = "O(N^2)"
                sortingAlgorithmName = "Bubble Sort"
                sorting = False

            elif event.key == pygame.K_i:
                sortingAlgorithm = insertionSort
                sortingAlgorithmTimeComp = "O(N^2)"
                sortingAlgorithmName = "Insertion Sort"
                sorting = False
            
            elif event.key == pygame.K_s:
                sortingAlgorithm = selectionSort
                sortingAlgorithmTimeComp = "O(N^2)"
                sortingAlgorithmName = "Selection Sort"
                sorting = False

            # Start Sorting
            elif event.key == pygame.K_1 and not sorting:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithm(displayInfos, ascending)

            # Ascending
            elif event.key == pygame.K_RIGHT and not sorting:
                ascending = True
            
            # Descending
            elif event.key == pygame.K_LEFT and not sorting:
                ascending = False
            
# Prevent main() from being run when the module is imported
if __name__ == "__main__":
    main()