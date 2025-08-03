#Controls:
#WASD + space + Lshift to move pen ball
#enter to place point
#4 points make a plane automatically
#backspace to delete last placed plane
#hold LMB+move cursor to move camera
#hold RMB+move cursor up/down to zoom in/out

import pygame
import math

#horisontal/vertical rotation of cam
hr=0
vr=0.5

#coords of pen ball
x=0
y=1
z=0

#lists of surfaces and points and whatnot
drawn=()
tuplelist=[]
drawntuplelist=[]
surfacelist=[]

#etc
bweh=0
pi=3.14
offset=0
mousedown=0
rightmd=0
zoom=500
timer=0

#pygame setup
pygame.init()
#this size can be changed :>
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Visual engine v0.1.0")
clock = pygame.time.Clock()
running = True

def drawpoint(points: tuple):
    #the camera positions are basically a vector function
    if points[1]<0:
        offset=pi
    else:
        offset=0
    camx=math.cos(vr)*math.sin(hr-0.5*pi)*-zoom
    camy=math.cos(vr)*math.cos(hr-0.5*pi)*zoom
    camz=math.sin(vr)*(-zoom)
    #pythagoras :>
    distance=math.sqrt((points[0]-camx)**2+(points[1]-camy)**2+(points[2]-camz)**2)+1
    #lots of trigonometry
    #the points are basically mounted on circles and go around the periphery when you turn the camera horisontally
    #for vertical rotation, the circles get flatter when rv is closer to 0, and their centers get further apart
    #the points are closer to the center of the screen the further away they are from the camera 
    return (500*math.sqrt(points[0]**2+points[1]**2)*math.cos(hr+offset+math.atan(points[0]/points[1]))/distance+500,500*math.sin(vr)*math.sqrt(points[0]**2+points[1]**2)*math.sin(hr+offset+math.atan(points[0]/points[1]))/distance+500*points[2]*math.cos(vr)/distance+500)

while running:
    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        if mousedown==0:
            oldx=pygame.mouse.get_pos()[0]
            oldy=pygame.mouse.get_pos()[1]
            mousedown=1
        hr+=(oldx-pygame.mouse.get_pos()[0])/300
        vr+=(pygame.mouse.get_pos()[1]-oldy)/300

        oldx=pygame.mouse.get_pos()[0]
        oldy=pygame.mouse.get_pos()[1]
    else:
        mousedown=0

    if pygame.mouse.get_pressed(num_buttons=3)[2]:
        if rightmd==0:
            oldzm=pygame.mouse.get_pos()[1]
            rightmd=1
        zoom+=(pygame.mouse.get_pos()[1]-oldzm)/10

        oldzm=pygame.mouse.get_pos()[1]
    else:
        rightmd=0

    #avoiding weird rotation stuff :3
    if hr>2*pi:
        hr=0
    elif hr<0:
        hr=2*pi

    if vr>0.5*pi:
        vr=0.5*pi
    elif vr<-0.5*pi:
        vr=-0.5*pi

    if zoom<0:
        zoom=0

    #find key presses to control
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_w]:
        x+=-5
    if keystate[pygame.K_s]:
        x+=5
    if keystate[pygame.K_a]:
        y+=-5
    if keystate[pygame.K_d]:
        y+=5
    if keystate[pygame.K_SPACE]:
        z+=-5
    if keystate[pygame.K_LSHIFT]:
        z+=5
    if keystate[pygame.K_RETURN] and bweh>30:
        tuplelist.append((x,y,z))
        drawntuplelist.append((x,y,z))
        if len(drawntuplelist)>3:
            surfacelist.append(drawntuplelist)
            drawntuplelist=[]
        bweh=0
    else:
        bweh+=1
    
    screen.fill((255,255,255))

    #colours to choose from :>
    colourlist=[(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]

    #finding the camera position
    camx=math.cos(vr)*math.sin(hr-0.5*pi)*-zoom
    camy=math.cos(vr)*math.cos(hr-0.5*pi)*zoom
    camz=math.sin(vr)*(-zoom)

    #finding the distance from the camera of the center of each plane and putting them in a dictionary
    dictionary={}
    for n in range(len(surfacelist)):
        templist=surfacelist[n]
        tt1=templist[0]
        tt2=templist[1]
        tt3=templist[2]
        tt4=templist[3]
        avgt=((tt1[0]+tt2[0]+tt3[0])/3,(tt1[1]+tt2[1]+tt3[1])/3,(tt1[2]+tt2[2]+tt3[2])/3)
        length=math.sqrt((avgt[0]-camx)**2+(avgt[1]-camy)**2+(avgt[2]-camz)**2)
        #using vector projection to check that the plane isn't behind the camera
        if (avgt[0]*camx+avgt[1]*camy+avgt[2]*camz)/(camx**2+camy**2+camz**2+0.01)<1:
            dictionary.update({n: length})

    #sorting the dictionary by distance from the camera and making a list of the keys 
    sorteddic=(sorted(dictionary.items(), key=lambda kv: (kv[1], kv[0])))
    planenolist=[i[0] for i in sorteddic]
    planenolist.reverse()

    #drawing surfaces
    for i in planenolist:
        templist=surfacelist[i]
        c=i-int(n/6)*6
        for i in range(4):
            pa=drawpoint(templist[0])
            pb=drawpoint(templist[1])
            pc=drawpoint(templist[2])
            pd=drawpoint(templist[3])
            pygame.draw.polygon(screen,colourlist[c],((pa,pb,pc,pd)))

    #drawing the points
    for n in range(len(drawntuplelist)):
        drawn=drawntuplelist[n]
        pygame.draw.circle(screen,(255,0,0),drawpoint((drawn[0],drawn[1],drawn[2])),10)

    #drawing the pen ball
    pygame.draw.circle(screen,(0,0,0),drawpoint((x,y,z)),10)

    #ability to remove last plane
    if keystate[pygame.K_BACKSPACE] and timer==10 and len(surfacelist)>0:
        surfacelist.pop()
        for n in range(4):
            tuplelist.pop()
        timer=0
    elif timer<10:
        timer+=1

    #pygame stuff
    pygame.display.update()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
