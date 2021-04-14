import pygame
import time

class AStar():

    def __init__(self, startNode, endNode, cols, rows, grid, visualisation):
        self.grid = grid
        self.openSet = []
        self.closedSet = []
        self.cols = cols
        self.rows = rows
        self.startNode = startNode
        self.endNode = endNode
        self.openSet.append(self.startNode)
        self.visualisation = visualisation
        self.AStar_loop()


    def f_cost(self, node):  #calculate f_cost of node ## combined cost
        return node.g_cost + self.h_cost(node)                  #self.h_cost(node) + self.g_cost(node)

    def h_cost(self, node):  #calculate h_cost of node ## (heuristic cost) -> distance from end node
        vx = abs(node.x - self.endNode.x)
        vy = abs(node.y - self.endNode.y)
        if vx <= vy:
            return 14*vx + 10*(vy - vx) # 14 ≈ squareroot(2) * 10 --> diagonal distance  ## 10 = 1 * 10 --> straight distance
        else:
            return 14*vy + 10*(vx - vy)

    def g_cost(self, node, checknode):  #calculate g_Cost of Node ## distance from start node
        x = node.x - checknode.x
        y = node.y - checknode.y
        sum = x + y
        if sum == 1 or sum == -1:
            return node.g_cost + 10
        else:
            return node.g_cost + 14

    def getNeighbors(self, node):
        vars = [(-1,-1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        neighbors = []
        for i in range(8):
            pos1 = vars[i][0] + node.y
            pos2 = vars[i][1] + node.x
            if pos1 > -1 and pos1 < self.rows:
                if pos2 > -1 and pos2 < self.cols:
                    neighbors.append(self.grid[pos2][pos1])
        return neighbors

    def AStar_loop(self):
        while True:
            time.sleep(0.08)
            currf = 1000000000
            currh = 1000000000
            currN = None
            for i in self.openSet:
                if i.f_cost < currf or i.h_cost < currh and i.f_cost == currf:
                    currf = i.f_cost
                    currh = i.h_cost
                    currN = i
            self.currentNode = currN
            self.openSet.remove(self.currentNode)
            self.closedSet.append(self.currentNode)
            self.currentNode.inOpen = False
            self.currentNode.inClosed = True

            if self.currentNode == self.endNode: #Path has been found
                return True

            for neighbour in self.getNeighbors(self.currentNode):
                if not neighbour.traversable or neighbour in self.closedSet:
                    continue
                #need to calculate g_cost with new node to check if new g_cost is lower
                new_g_cost = self.g_cost(neighbour, self.currentNode)
                if new_g_cost < neighbour.g_cost or neighbour not in self.openSet:
                    neighbour.g_cost = new_g_cost
                    neighbour.f_cost = self.f_cost(neighbour)
                    neighbour.parent = self.currentNode
                    if neighbour not in self.openSet:
                        self.openSet.append(neighbour)
                        neighbour.inOpen = True
            #draw functions
            self.visualisation.drawGrid()
            pygame.display.update()


class Node():
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.f_cost = 0
            self.g_cost = 0
            self.h_cost = 0
            self.parent = None
            self.traversable = True
            self.startNode = False
            self.endNode = False
            self.inClosed = False
            self.inOpen = False
            self.inPath = False
            self.rect = None

        def getColor(self):
            if not self.traversable:
                return (0, 0, 0)
            elif self.startNode or self.endNode:
                return (0, 0, 255)
            elif self.inPath:
                return (64, 224, 208)
            elif self.inClosed:
                return (255, 0, 0)
            elif self.inOpen:
                return (0, 255, 0)
            else:
                return (255, 255, 255)


class Visualisation():
    def __init__(self, cols, width, height):
        self.cols = cols
        self.rows = cols
        self.width = width
        self.height = height
        self.colors = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255), "black": (0, 0, 0), "grey": (227, 230, 225), "lightgrey": (231, 231, 231), "darkgrey": (118,118,118)}
        self.menuwidth = width * 0.245
        self.gridwidth = self.width * 0.75
        self.createGrid()
        self.pygameloop()

    def createGrid(self):
        self.grid = [[] for _ in range(self.rows)]
        for i in range(len(self.grid)):
            self.grid[i] = [[] for _ in range(self.cols)]

        for i in range(self.cols):
            for j in range(self.rows):
                self.grid[i][j] = Node(i, j)

    def drawText(self, str, rect, px, color, bckcolor):
        font = pygame.font.SysFont("calibri", px)
        textsurface = font.render(str, True, color, bckcolor)
        rect_width = rect.width
        rect_height = rect.height
        textsurface_rect = textsurface.get_rect(center =(rect_width/2 + rect.left, rect_height/2 + rect.top))
        self.screen1.blit(textsurface, textsurface_rect)

    def drawGrid(self):
        squarewidth = self.gridwidth / (self.cols * 1.1)
        for i in range(self.cols):
            for j in range(self.rows):
                node = self.grid[i][j]
                cordx = node.x
                cordy = node.y
                color = node.getColor()
                sq = pygame.Rect(self.width * 0.25 + squarewidth * cordx + squarewidth * 0.1 * cordx, squarewidth * cordy + squarewidth * 0.1 * cordy, squarewidth, squarewidth)
                self.grid[i][j].rect = sq
                pygame.draw.rect(self.screen1, color, sq, 0)


    def drawMenu(self):
        menu_bg = pygame.Rect(0, 0 , self.menuwidth, self.height)
        pygame.draw.rect(self.screen1, self.colors.get("grey"), menu_bg, 0)

        #start_end_Node Button
        self.button1rect = pygame.Rect(self.menuwidth*0.1, self.height*0.5, self.menuwidth*0.8, self.height*0.06)
        pygame.draw.rect(self.screen1, self.colors.get("black"), self.button1rect, 2)
        self.drawText("Set Start & End Node", self.button1rect, 18, "black", None)

        #drawWalls Button
        self.button2rect = pygame.Rect(self.menuwidth*0.1, self.height*0.5 + self.height*0.09, self.menuwidth*0.8, self.height*0.06)
        pygame.draw.rect(self.screen1, self.colors.get("black"), self.button2rect, 2)
        self.drawText("draw Walls", self.button2rect, 18, "black", None)

        #reset Button
        self.button3rect = pygame.Rect(self.menuwidth*0.1, self.height*0.5 + self.height*0.18, self.menuwidth*0.8, self.height*0.06)
        pygame.draw.rect(self.screen1, self.colors.get("black"), self.button3rect, 2)
        self.drawText("reset Grid", self.button3rect, 18, "black", None)

        #start Button
        self.button4rect = pygame.Rect(self.menuwidth*0.1, self.height*0.5 + self.height*0.27, self.menuwidth*0.8, self.height*0.06)
        pygame.draw.rect(self.screen1, self.colors.get("black"), self.button4rect, 2)
        self.drawText("Start Pathfinding", self.button4rect, 18, "black", None)

    def setStartEnd(self, pygame_events):
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(self.cols):
                        for j in range(self.rows):
                            node = self.grid[i][j]
                            if node.rect.collidepoint(event.pos):
                                if self.StartEndCounter == 0:
                                    node.startNode = True
                                    self.startNode = node
                                    self.StartEndCounter += 1
                                elif self.StartEndCounter == 1 and node.startNode == False:
                                    node.endNode = True
                                    self.endNode = node
                                    self.StartEndCounter += 1
        if self.StartEndCounter == 2:
            self.startend = False


    def drawWalls(self, pygame_events):
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(self.cols):
                        for j in range(self.rows):
                            node = self.grid[i][j]
                            if node.rect.collidepoint(event.pos):
                                node.traversable = not node.traversable
    def drawPath(self, node):
        node.inPath = True
        if node.parent != None:
            self.drawPath(node.parent)
        return

    def pygameloop(self):
        pygame.init()
        self.pyactive = True
        self.screen1 = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("A*-Algorithmn")
        self.startend = False
        self.drawWall = False
        while self.pyactive:
            pygame_events = pygame.event.get()
            for event in pygame_events:
                if event.type == pygame.QUIT:
                    self.pyactive = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button1rect.collidepoint(event.pos):  #Stat&End-Node Button
                            self.StartEndCounter = 0
                            self.startend = True
                            self.drawWall = False
                        elif self.button2rect.collidepoint(event.pos):  #drawWalls Button
                            self.startend = False
                            self.drawWall = True
                        elif self.button3rect.collidepoint(event.pos): #Reset Button
                            self.startend = False
                            self.drawWall = False
                            self.createGrid()
                        elif self.button4rect.collidepoint(event.pos): #Start Pathfinding Button
                            self.startend = False
                            self.drawWall = False
                            AStar(self.startNode, self.endNode, self.cols, self.rows, self.grid, self)
                            self.drawPath(self.endNode)
            if self.startend:
                self.setStartEnd(pygame_events)
            if self.drawWall:
                self.drawWalls(pygame_events)
            self.screen1.fill(self.colors.get("darkgrey"))
            self.drawMenu()
            self.drawGrid()
            pygame.display.update()

x = Visualisation(20, 800, 600)