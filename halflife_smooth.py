import time
import random
import math
import matplotlib
import matplotlib.pyplot as plt
import pygame

class molecule(object):
    """
    molecules have a given half-life, which have
    a 1/hl chance of decaying every second
    """
    def __init__(self, pos, hl):
        self.state = 1
        self.x, self.y = pos
        self.hl = hl
        
    def iterate(self, elapsed):
        if random.random() < 1-.5**(elapsed/self.hl):
            self.state = 0
        return self.state

    

class model(object):
    """
    model is a 2D array of molecules
    """

    
    def __init__(self, halflife, size):
        self.container = []
        self.x, self.y = size
        self.tot = self.x*self.y
        self.hl = halflife
        for y in range(0,self.y):
            temp = []
            for x in range(0,self.x):
                temp.append(molecule((x,y), self.hl))
            self.container.append(temp)
        self.WHITE = (255, 255, 255)
        self.green = (  0, 255,   0)
        self.grey =  (  10, 10,  10)
        self.clock = pygame.time.Clock()
        pygame.init()    
        pygame.display.set_caption('HalfLife Simulation')
        self.screen = pygame.display.set_mode((1200,700))
        self.pxarray = pygame.PixelArray(self.screen)

    def update(self, elapsed):
        

        
        livingTot = 0
        
        for y in range(0,self.y):
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    done=True
                    
            for x in range(0,self.x):
                if self.container[y][x].iterate(elapsed) == 1:
                    self.pxarray[x, y] = self.green
                    livingTot += 1
                else:
                    if self.screen.get_at((x, y)) != (10, 10, 10, 255):
                        self.pxarray[x, y] = self.grey
                        pygame.display.flip()
                        self.clock.tick(60)
        
            
                
        
        #print("\nLiving Pixels:", livingTot, "/", self.tot,
              #"(", round(100 * (livingTot/(self.tot)), 3), "% )\n")
        
        return livingTot

    def run(self):
        living = self.tot
        print("half-life set to", self.hl, "seconds.")
        print("beginning simulation...")
        clock = pygame.time.Clock()
        tick = -1
        elapsed = 0
        graph = []
        begin = time.time()
        while living > self.tot * 2**-4 :
            #time.sleep(1 - elapsed)
            start = time.time()
            

            living = self.update(elapsed)
            graph.append(living)
            tick+=elapsed
            
            finish = time.time()
            elapsed = finish - start
        end = time.time()
        runtime = end - begin
        print(self.tot, "decayed in", tick, "seconds ( reality:", runtime, ")")
        print(tick/self.hl, "half-lives occured")
        return graph

def hl(N, t, y):
    return N*math.e**(-y * t)
    

#oxygen-22: 2.25


        
o22 = model(300, (1200,700))
plt.plot(o22.run(), linewidth=.5)
plt.ylabel('Living')
plt.xlabel('Seconds')
plt.show()
pygame.quit()



