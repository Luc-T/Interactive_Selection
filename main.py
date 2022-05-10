import pygame
import random

from dna import Dna
  

# activate the pygame library .
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
  
pygame.font.init() # you have to call this at the start to use pygame 


#Defining some constants
my_font = pygame.font.SysFont('Arial', 30)
# define the RGB value
# for white, green,
# blue, black, red
# colour respectively.
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)
# light shade of the button
color_light = (170,170,170)
# dark shade of the button
color_dark = (100,100,100)

POPMAX = 10
HALFMAX = 10 // 2
MUTATIONRATE = 0.05
FPS = 60
EMPTY = []
# assigning values to determine screen size
X = 1600
Y = 900
  
#################################################

#create tshirt class here so it can drawn on the display surface
class Tshirt:
     def __init__ (self, dna):
        self.genes = dna
        self.fitness = 1

     def get_DNA(self):
         #return the dna object
         return self.genes
        
    #Displayt is the most important function of Tshirt:

    #recieve size and position of design and display
    #using its dna
     def display(self, surface, rect_y, rect_y2, rect_x, rect_x2):
        genes = self.genes.get_genes()
        tshirtC = [255*genes[0], 255*genes[1], 255*genes[2]]
        c = [255*genes[3], 255*genes[4], 255*genes[5]]
        halfW = rect_x2/2
        quarterW = halfW/2
        xCentre = rect_x + (halfW)
        halfH = (rect_y2/2)
        quarterH = halfH/2
        yCentre = rect_y + (halfH)
        #determine position of the circle
        if (genes[6] >= 0.5):
            c_x = xCentre + quarterW*genes[8]
        else:
            c_x = xCentre - quarterW*genes[8]
        if (genes[7] >= 0.5):
            c_y = yCentre + quarterH*genes[8]
        else:
            c_y = yCentre - quarterH*genes[8]

        r = (quarterW) * genes[9]
        
        #draw the rectange, then save it so it can be returned
        rects = (pygame.draw.rect(surface, tshirtC, (rect_x, rect_y, rect_x2, rect_y2)))
        pygame.draw.circle(surface, c, (c_x, c_y), r, 0)
        #calc genes for traingle, min 1, max 3 per tshirt
        if (genes[10] <= 0.3333):
            tri = 1
        elif (genes[10] > 0.3333) & (genes[10] <= 0.6666):
            tri = 2
        else:
            tri = 3
        #calculate the position of triangle base      
        if (genes[11] <= 0.5):
            tri_y = yCentre + halfH*genes[12]
        else:
            tri_y = yCentre - quarterH*genes[12]
        #triangleC = triangle colour
        triangeC = [255*genes[13], 255*genes[14], 255*genes[15]]
        j = 16

        #loop for however many triangles are on the design
        for i in range(tri):
            #clalculate heights of each triangle individually
            triHeight = tri_y - 30 - (80*genes[j])

            if (genes[j+1] <= 0.5):
                t_x = xCentre + quarterW*genes[j+2]
            else:
                t_x = xCentre - halfW*genes[j+2]
            t_x3 = t_x + 70*genes[j+3] + 20
            t_x2 = t_x + ((t_x3 - t_x)/2)
            pygame.draw.polygon(surface, triangeC, [(t_x,tri_y), (t_x2,triHeight), (t_x3,tri_y)])

            j = j + 4
        
        return rects

     def get_fitness(self):
        return self.fitness

    #increment fitness if mouse has rolled over tshirt
     def rollover(self):
         self.fitness = self.get_fitness() + 0.25

     def set_prob(self, prob):
         self.prob = prob

     def get_prob(self):
         return self.prob
         
   
def getMaxFitness ( popList ):
    sum = 0
    for i in (popList):
        sum += i.get_fitness()
    return sum


def draw_text_boxes( text_boxes ):
    x = 170    
    for i in range(HALFMAX):
        displaySurface.blit(text_boxes[i], (x,370))
        x += 300

    x = 170    
    for i in range(HALFMAX, POPMAX):
        displaySurface.blit(text_boxes[i], (x,770))
        x += 300
    return

def draw_pop( popList ):
    #update screen, hiding old tshirts
    displaySurface.fill(white)
    #display row 1
    x = 70
    y = 20
    rects = []
    for i in range(HALFMAX):
        rects.append(popList[i].display(displaySurface, y, THEIGHT, x, TWIDTH))
        x += 300
        textSurface = my_font.render(str(popList[i].get_fitness()), False, 
        (0, 0, 0), (255, 255, 255))
        textBoxes[i] = textSurface
    #display row 2
    x = 70
    y = 410
    for i in range(HALFMAX, POPMAX):
        rects.append(popList[i].display(displaySurface, y, THEIGHT, x, TWIDTH))
        x += 300
        textSurface = my_font.render(str(popList[i].get_fitness()), False, 
        (0, 0, 0), (255, 255, 255))
        textBoxes[i] = textSurface
    return rects
    

#Beginning of Main
#################################################
#function to pick a parent based on fitness
def pickOne( pA ):
    index = 0
    r = random.random()
    while (r > 0):
        r = r - pA[index].get_prob()
        index +=1

    index -= 1
    return pA[index]

def reproduction( popList ):
    #get a sum of all the fitnesses
    fitnessSum = getMaxFitness(popList)
    #set a normalised probabiliy score for each candidate 
    for i in popList:
        prob = (i.get_fitness() / fitnessSum)
        i.set_prob(prob)
        
    newPopList = []
    for i in range(POPMAX):
        #pick first parent
        parent1 = pickOne(popList)
        #pick second parent
        parent2 = pickOne(popList)
        #Create new child from genes of parents
        p1Genes = parent1.get_DNA()
        p2Genes = parent2.get_DNA()
        child = p1Genes.crossover(p2Genes)
        child.mutate(MUTATIONRATE)
        newPopList.append(Tshirt(child))
    
    return newPopList

#end of Mains functions

#################################################
# create the display surface object
# of specific dimension..e(X,Y).
displaySurface = pygame.display.set_mode((X, Y ))
  
# set the pygame window name
pygame.display.set_caption('Drawing')
  
# completely fill the surface object 
# with white colour 
displaySurface.fill(white)

width = displaySurface.get_width()
height = displaySurface.get_height()
  

#initialise population
x = 70
TWIDTH = 210
y = 20
THEIGHT = 338

popList = []
textBoxes = []
rects = []

#create pop to go on first row
for i in range(HALFMAX):
    dna = (Dna(EMPTY))
    mbr = Tshirt(dna)
    
    popList.append(mbr)
    #save list of rectangles to detect when mouse is over them
    rects.append(popList[i].display(displaySurface, y, THEIGHT, x, TWIDTH))
    x += 300
    textSurface = my_font.render(str(popList[i].get_fitness()), False, (0, 0, 0), (255, 255, 255))
    textBoxes.append(textSurface)

#create pop to go on second row
x = 70
y = 410
for i in range(HALFMAX, POPMAX):
    dna = (Dna(EMPTY))
    mbr = Tshirt(dna)
    
    popList.append(mbr)
    #save list of rectangles to detect when mouse is over them
    rects.append(popList[i].display(displaySurface, y, THEIGHT, x, TWIDTH))
    x += 300
    textSurface = my_font.render(str(popList[i].get_fitness()), False, (0, 0, 0), (255, 255, 255))
    textBoxes.append(textSurface)

draw_text_boxes(textBoxes)



clock = pygame.time.Clock()
# infinite loop
while True :
    clock.tick(FPS)
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get() :
  
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
        
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # if mouse is hovered on a button it
        # changes to lighter shade 

        if width/4 <= mouse[0] <= width/4+285 and (height - 90) <= mouse[1] <= (height - 90 + 40):
            pygame.draw.rect(displaySurface,color_light,[width/4,(height - 90),285,40])
            #if mouse1 was clicked on the button

            if click[0] == 1 != None:
                #initiate next pop!
                popList = reproduction(popList)
                rects = draw_pop(popList)
        else:
            #else draw button
            pygame.draw.rect(displaySurface,color_dark,[width/4,(height - 90),285,40])
        displaySurface.blit(my_font.render("Generate next population", False, (0, 0, 0)), (width/4,height - 90))


        #Check each tshirt, if the mouse is on it, increase the fitness
        for i in range(POPMAX):
            #check if user is interacting with tshirt
            #increase fitness with rollover function if so 
            if rects[i].collidepoint(mouse):
                popList[i].rollover()
                textBoxes[i] = my_font.render(str(popList[i].get_fitness()),
                 False, (0, 0, 0), (255, 255, 255))
                
        draw_text_boxes(textBoxes)
        # Draws the surface object to the screen. 
        pygame.display.update()