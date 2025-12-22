from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Variables
W_WIDTH, W_HEIGHT = 1000, 900

GRID_LENGTH = 1200
GRID_CELL_SIZE = 50

fovY = 60
camera_angle_h = 0.0     
camera_angle_v = 0.5      
camera_zoom = 800         
is_first_person = False  

player_pos = [0, 0, 20] 
player_vel = [0, 0, 0]    
player_acc = 1.0         
friction = 0.97           
gravity = 1.5             
ball_radius = 20

# Game State
game_over = False
falling = False
time_count = 0

map_data = {}

def init_map():

    global map_data
    map_data = {} 
    
    for x in range(-GRID_LENGTH, GRID_LENGTH, GRID_CELL_SIZE):
        for y in range(-GRID_LENGTH, GRID_LENGTH, GRID_CELL_SIZE):
            
            
            if -150 < x < 150 and -150 < y < 150:#safe jone(starting)
                map_data[(x, y)] = 0 
            else:
                rng = random.random()
                if rng < 0.10:     #hole
                    map_data[(x, y)] = 1 
                elif rng < 0.15:     #  Obstacle
                    map_data[(x, y)] = 2
                else:
                    map_data[(x, y)] = 0 # Safe Floor

init_map()


# Drawing Functions
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, W_WIDTH, 0, W_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid_and_walls():
    
    # Draw Floor
    glBegin(GL_QUADS)
    for x in range(-GRID_LENGTH, GRID_LENGTH, GRID_CELL_SIZE):
        for y in range(-GRID_LENGTH, GRID_LENGTH, GRID_CELL_SIZE):
            
            tile_type = map_data.get((x, y), 0)
            
            if tile_type == 1: # Hole so Don't draw
                continue
            
            if ((x // GRID_CELL_SIZE) + (y // GRID_CELL_SIZE)) % 2 == 0: 
                glColor3f(1.0, 1.0, 1.0) # White
            else:
                glColor3f(0.0, 0.0, 0.5) # Blue
            
            glVertex3f(x, y, 0)
            glVertex3f(x + GRID_CELL_SIZE, y, 0)
            glVertex3f(x + GRID_CELL_SIZE, y + GRID_CELL_SIZE, 0)
            glVertex3f(x, y + GRID_CELL_SIZE, 0)
    glEnd()

    # Draw Obstacles
    for (x, y), type in map_data.items():
        if type == 2: 
            glPushMatrix()
            glColor3f(0.9, 0.1, 0.1)
            glTranslatef(x + GRID_CELL_SIZE/2, y + GRID_CELL_SIZE/2, 25)
            glutSolidCube(40)
            glPopMatrix()

    # Draw Walls
    wall_h = 50
    
    glColor3f(0, 0, 0.8) # Left
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0); glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_h); glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_h)
    glEnd()
    
    glColor3f(0, 0.8, 0.8) #Right
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0); glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_h); glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_h)
    glEnd()

    glColor3f(0, 0.8, 0) #Back
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0); glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_h); glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_h)
    glEnd()
    
    glColor3f(0, 0, 0.5) #Front
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0); glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_h); glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_h)
    glEnd()

def draw_player():
    global player_pos, time_count, falling
    
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    if falling:
        glColor3f(1, 0, 0)
    else:
        glColor3f(1.0, 0.84, 0.0) 
        
    gluSphere(gluNewQuadric(), ball_radius, 32, 30)
    glPopMatrix()


# Physics
def check_collisions():
    global player_pos, player_vel, falling, game_over
    
    if player_pos[0] > GRID_LENGTH - ball_radius:#hit with Boundaries
        player_pos[0] = GRID_LENGTH - ball_radius
        player_vel[0] *= -0.8#bounce back
    elif player_pos[0] < -GRID_LENGTH + ball_radius:
        player_pos[0] = -GRID_LENGTH + ball_radius
        player_vel[0] *= -0.8
        
    if player_pos[1] > GRID_LENGTH - ball_radius:
        player_pos[1] = GRID_LENGTH - ball_radius
        player_vel[1] *= -0.8
    elif player_pos[1] < -GRID_LENGTH + ball_radius:
        player_pos[1] = -GRID_LENGTH + ball_radius
        player_vel[1] *= -0.8

    # hit with holes or obstecal
    gx = int(GRID_CELL_SIZE * round(player_pos[0] / GRID_CELL_SIZE))
    gy = int(GRID_CELL_SIZE * round(player_pos[1] / GRID_CELL_SIZE))
    
    tile_type = map_data.get((gx, gy), 0)
    
    if tile_type == 1: # Hole
        falling = True
    elif tile_type == 2: # Obstacle
        player_vel[0] *= -1.2#bounce back
        player_vel[1] *= -1.2
        player_pos[0] += player_vel[0] * 2
        player_pos[1] += player_vel[1] * 2

def idle():
    global player_pos, player_vel, falling, game_over, time_count
    
    if game_over:
        return
    time_count += 1
    
    if falling:
        player_pos[2] -= gravity * 4
        player_vel[0] *= 0.99
        player_vel[1] *= 0.99
        if player_pos[2] < -700:
            game_over = True
    else:
        player_vel[0] *= friction
        player_vel[1] *= friction
        player_pos[0] += player_vel[0]
        player_pos[1] += player_vel[1]
        
        check_collisions()

    glutPostRedisplay()


#Controls
def keyboardListener(key, x, y):
    global player_vel, game_over, player_pos, falling, is_first_person

    if not game_over and not falling:
        if key == b'a': player_vel[1] += player_acc
        if key == b'd': player_vel[1] -= player_acc
        if key == b's': player_vel[0] -= player_acc
        if key == b'w': player_vel[0] += player_acc


    if key == b'r':#reset
        game_over = False
        falling = False
        player_pos = [0, 0, 20]
        player_vel = [0, 0, 0]
        
        init_map() 
        print("Game Restarted")
        
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global camera_angle_h, camera_angle_v
    if key == GLUT_KEY_UP:
        camera_angle_v = min(1.5, camera_angle_v + 0.05)
    if key == GLUT_KEY_DOWN:
        camera_angle_v = max(0.1, camera_angle_v - 0.05)
    if key == GLUT_KEY_RIGHT:
        camera_angle_h -= 0.05
    if key == GLUT_KEY_LEFT:
        camera_angle_h += 0.05
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global is_first_person
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        is_first_person = not is_first_person
    glutPostRedisplay()

def setupCamera():
    global camera_angle_h, camera_angle_v, camera_zoom, is_first_person, player_pos
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, W_WIDTH/W_HEIGHT, 0.1, 4500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if is_first_person:#first person
        eyeX = player_pos[0]
        eyeY = player_pos[1]
        eyeZ = player_pos[2] + ball_radius + 5#camera at top of the ball
        
        
        targetX = eyeX + math.cos(camera_angle_h) * 200
        targetY = eyeY + math.sin(camera_angle_h) * 200
        targetZ = eyeZ + (camera_angle_v - 0.5) * 200 
        
        gluLookAt(eyeX, eyeY, eyeZ, 
                  targetX, targetY, targetZ,
                  0, 0, 1)
    else:
        
        eyeX = player_pos[0] - math.cos(camera_angle_h) * camera_zoom#THIRD PERSON
        eyeY = player_pos[1] - math.sin(camera_angle_h) * camera_zoom
        eyeZ = camera_zoom * camera_angle_v
        
        gluLookAt(eyeX, eyeY, eyeZ,
                   player_pos[0], player_pos[1], 0, 
                   0, 0, 1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupCamera()

    draw_grid_and_walls()
    draw_player()
    
    draw_text(700, 860, "Controls: W,A,S,D Move/Camera control: Arrow keys ")
    draw_text(700, 880, "Right click: Toggle Camera (1st/3rd Person)")
    
    if game_over:
        draw_text(400, 800, "GAME OVER! PRESS 'R'")

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(W_WIDTH, W_HEIGHT)
    glutInitWindowPosition(100, 10)
    glutCreateWindow(b"Hazard Ball")

    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    print("Hazard Ball")
    print("Press 'R' to restart with a NEW random map.")
    glutMainLoop()

if __name__ == "__main__":
    main()