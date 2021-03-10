## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================
## Install OpenGL: pip3 install PyOpenGL PyOpenGL_accelerate
## =========================================================================

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

## -------------------------------------------------------------------------
## Some global variables: DON'T DO THIS IN REAL LIFE APPLICATIONS!!!!
## -------------------------------------------------------------------------
room_size = 6
viewer_height = 1.7
camera_eye = [ 0, viewer_height, room_size ]
camera_target = [ 0, viewer_height, 0 ]
camera_up = [ 0, 1, 0 ]
tetha = math.pi/2

room_geometry = [
    [ -room_size, 0,  room_size ],
    [  room_size, 0,  room_size ],
    [  room_size, 0, -room_size ],
    [ -room_size, 0, -room_size ],
    [ -room_size, room_size,  room_size ],
    [  room_size, room_size,  room_size ],
    [  room_size, room_size, -room_size ],
    [ -room_size, room_size, -room_size ]
    ]
room_topology = [
    [ 0, 1, 3 ],
    [ 1, 2, 3 ],
    [ 1, 5, 2 ],
    [ 5, 6, 2 ],
    [ 4, 7, 5 ],
    [ 7, 6, 5 ],
    [ 2, 6, 7 ],
    [ 7, 3, 2 ],
    [ 3, 7, 4 ],
    [ 0, 3, 4 ],
    [ 1, 0, 4 ],
    [ 1, 4, 5 ]
    ]

## -------------------------------------------------------------------------
def init( ):
  global room_size

  glClearColor( 0.0, 0.0, 0.0, 0.0 )

  # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glLight.xml

  glShadeModel( GL_SMOOTH )
  glLightfv( GL_LIGHT0, GL_POSITION, [ 0, 0, 0, 1.0 ] )
  glLightfv( GL_LIGHT0, GL_DIFFUSE, [1,0,0,1] )

  glLightfv( GL_LIGHT1, GL_POSITION, [ room_size, room_size, room_size, 1.0 ] )
  glLightfv( GL_LIGHT1, GL_DIFFUSE, [0,0,1,1] )

  glLightfv( GL_LIGHT2, GL_POSITION, [ room_size, 0, room_size, 1.0 ] )
  glLightfv( GL_LIGHT2, GL_DIFFUSE, [0,1,0,1] )

  #glMaterial()
  #Teclas D & A

  glEnable( GL_LIGHTING );
  glEnable( GL_LIGHT0 );
  glEnable( GL_LIGHT1 );
  glEnable( GL_LIGHT2 );
  
  glEnable( GL_DEPTH_TEST )
# end def

## -------------------------------------------------------------------------
def drawOrthoBase( ):
  glPushMatrix( )

  cur_color = glGetFloatv( GL_CURRENT_COLOR )
  lw = glGetFloatv( GL_LINE_WIDTH )

  glLineWidth( 2 )
  glBegin( GL_LINES )

  glColor3f( 1, 0, 0 )
  glVertex3f( 0, 0, 0 )
  glVertex3f( 1, 0, 0 )

  glColor3f( 0, 1, 0 )
  glVertex3f( 0, 0, 0 )
  glVertex3f( 0, 1, 0 )

  glColor3f( 0, 0, 1 )
  glVertex3f( 0, 0, 0 )
  glVertex3f( 0, 0, 1 )

  glEnd( )

  glColor3f( cur_color[ 0 ], cur_color[ 1 ], cur_color[ 2 ] )
  glLineWidth( lw )

  glPopMatrix( )
# end def

## -------------------------------------------------------------------------
def drawRoom( ):
  global room_geometry, room_topology

  glColor3f( 1, 1, 1 )
  for t in room_topology:
    glBegin( GL_LINE_LOOP )
    glVertex3fv( room_geometry[ t[ 0 ] ] )
    glVertex3fv( room_geometry[ t[ 1 ] ] )
    glVertex3fv( room_geometry[ t[ 2 ] ] )
    glEnd( )
  # end for
# end def

## -------------------------------------------------------------------------
def draw( ):
  global room_size, viewer_height

  # -- Clear framebuffer
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

  # -- Draw stuff
  glMatrixMode( GL_MODELVIEW )
  glLoadIdentity( )

  # -- Camera
  gluLookAt(
    camera_eye[ 0 ], camera_eye[ 1 ], camera_eye[ 2 ],
    camera_target[ 0 ], camera_target[ 1 ], camera_target[ 2 ],
    camera_up[ 0 ], camera_up[ 1 ], camera_up[ 2 ]
    )

  # -- Scene
  drawOrthoBase( )
  drawRoom( )

  glColor3f( 0.4, 0.7, 0.2 )
  glTranslatef( 0, 1, 0 )
  glutSolidTeapot( 0.5 )

  # -- Prepare next frame
  glFlush( )
  glutSwapBuffers( )
# end def

## -------------------------------------------------------------------------
def reshape( width, height ):
  global room_size

  # Compute aspect ratio of the new window
  aspect = width
  if height != 0:
    aspect /= height
  # end if

  # Set the viewport to cover the new window
  glViewport( 0, 0, width, height )

  # Compute projection
  glMatrixMode( GL_PROJECTION )
  glLoadIdentity( )
  gluPerspective( 45, aspect, 1e-2, 3 * room_size )
# end def

## -------------------------------------------------------------------------
def keyboard( key, x, y ):
  global camera_eye, camera_target, camera_up, tetha
  lx = camera_target[ 0 ] - camera_eye[ 0 ]
  ly = camera_target[ 1 ] - camera_eye[ 1 ]
  lz = camera_target[ 2 ] - camera_eye[ 2 ]
  n = ( lx * lx ) + ( ly * ly ) + ( lz * lz )
  print(lx)
  print(ly)
  print(lz)

  if key == b'w' or key == b'W':
    if n > 0:
      camera_eye[ 0 ] += ( lx / n )
      camera_eye[ 1 ] += ( ly / n )
      camera_eye[ 2 ] += (( lz / n ))
      print(camera_eye)
      glutPostRedisplay( )
    # end if
  elif key == b's' or key == b'S':
    if n > 0:
      camera_eye[ 0 ] -= ( lx / n )
      camera_eye[ 1 ] -= ( ly / n )
      camera_eye[ 2 ] -= (( lz / n )) 
      print(camera_eye)
      glutPostRedisplay( )
  if key == b'a' or key == b'A':
    if n > 0:
      tetha += 0.1
      camera_eye[ 0 ] = room_size * math.cos(tetha)
      camera_eye[ 2 ] = room_size * math.sin(tetha)
      glutPostRedisplay( )
    # end if
  elif key == b'd' or key == b'D':
    if n > 0:
      tetha -= 0.1
      camera_eye[ 0 ] = room_size * math.cos(tetha)
      camera_eye[ 2 ] = room_size * math.sin(tetha)
      glutPostRedisplay( )

  # end if
# end def

## -------------------------------------------------------------------------
## ---------------------------------- MAIN ---------------------------------
## -------------------------------------------------------------------------

# Prepare window
glutInit( )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH )
glutInitWindowSize( 700, 700 )
glutInitWindowPosition( 0, 0 )
wind = glutCreateWindow( "A simple room" )

# Prepare OpenGL
init( )

# Associate callbacks
glutDisplayFunc( draw )
glutReshapeFunc( reshape )
glutKeyboardFunc( keyboard )

# Main loop
glutMainLoop( )

## eof - light.py
