## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================
## Install OpenGL: pip3 install PyOpenGL PyOpenGL_accelerate
## =========================================================================

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, sys

## -------------------------------------------------------------------------
class ParametricFunction:
  Points = []
  Normals = []
  Triangles = []

  '''
  Initalization
  '''
  def __init__( self ):
    pass
  # end def

  '''
  Points on the surface
  '''
  def point( self, u, v ):
    cu = math.cos( u )
    su = math.sin( u )
    cv = math.cos( v )
    sv = math.sin( v )
    c2v = ( cv * cv ) - ( sv * sv )
    s3 = math.sqrt( 3.0 )

    return [
      cu / ( s3 + sv ),
      su / ( s3 + sv ),
      v / ( s3 + c2v ),
      ]
  # end def

  '''
  Normal to the surface
  '''
  def normal( self, u, v ):
    cu = math.cos( u )
    su = math.sin( u )
    cv = math.cos( v )
    sv = math.sin( v )
    c2v = ( cv * cv ) - ( sv * sv )
    s2v = 2.0 * cv * sv
    s3 = math.sqrt( 3.0 )

    f1 = -su / ( s3 + sv )
    f2 = cu / ( s3 + sv )
    f3 = -cu * cv / ( ( s3 + sv ) ** 2 )
    f4 = -cu * sv / ( ( s3 + sv ) ** 2 )
    f5 = ( 2.0 * v * s2v ) / ( ( s3 + c2v ) ** 2 )
    f5 = f5 + ( 1.0 / ( s3 + c2v ) )
    nx = f2 * f5
    ny = -f1 * f5
    nz = ( f1 * f4 ) - ( f2 * f3 )
    d = math.sqrt( ( nx * nx ) + ( ny * ny ) + ( nz * nz ) )
    if d == 0.0:
      d = 1.0
    # end if
    return [ nx / d, ny / d, nz / d ]
  # end def

  '''
  Sampling
  '''
  def sample( self, su, sv ):
    self.Points = []
    self.Normals = []
    self.Triangles = []
    k = 0
    for iu in range( su + 1 ):

      u = ( 2.0 * math.pi * float( iu ) / float( su ) ) - math.pi
      for iv in range( sv ):
        v = ( 2.0 * math.pi * float( iv ) / float( sv ) ) - math.pi

        # Geometry
        self.Points.append( self.point( u, v ) )
        self.Normals.append( self.normal( u, v ) )

        # Topology
        if iu < su - 1 and iv < sv - 1:
          self.Triangles.append( [ k, k + 1, k + su + 1 ] )
          self.Triangles.append( [ k + 1, k + su + 2, k + su + 1 ] )
        # end if
        k += 1

      # end for
    # end for
  # end def

# end class

## -------------------------------------------------------------------------
## Some global variables: DON'T DO THIS IN REAL LIFE APPLICATIONS!!!!
## -------------------------------------------------------------------------
room_size = 6
viewer_height = 1.7

camera_angle = 0
camera_pos = room_size
camera_height = 0
current_material = 1

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

myFunction = ParametricFunction( )

## -------------------------------------------------------------------------
def init( ):
  global room_size, myFunction

  myFunction.sample( 50, 50 )

  glClearColor( 0.0, 0.0, 0.0, 0.0 )

  # https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/glLight.xml

  #glShadeModel( GL_FLAT )
  #glLightfv( GL_LIGHT0, GL_POSITION, [ 1.0, 1.0, 1.0, 1.0 ] )

  #glEnable( GL_LIGHTING )
  #glEnable( GL_LIGHT0 )

  #glEnable( GL_DEPTH_TEST )

  glShadeModel( GL_SMOOTH )
  glLightfv( GL_LIGHT0, GL_POSITION, [ 0, 0, 0, 1.0 ] )
  glLightfv( GL_LIGHT0, GL_SPECULAR, [1,0,0,1] )

  glLightfv( GL_LIGHT1, GL_POSITION, [ room_size, room_size, room_size, 1.0 ] )
  glLightfv( GL_LIGHT1, GL_SPECULAR, [0,0,1,1] )

  glLightfv( GL_LIGHT2, GL_POSITION, [ room_size, 0, room_size, 1.0 ] )
  glLightfv( GL_LIGHT1, GL_SPECULAR, [0,1,0,1] )

  glLightfv( GL_LIGHT3, GL_POSITION, [ room_size, 0, room_size, 1.0 ] )
  glLightfv( GL_LIGHT3, GL_SPECULAR, [0,1,0,1] )

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
    glBegin( GL_LINES )
    glVertex3fv( room_geometry[ t[ 0 ] ] )
    glVertex3fv( room_geometry[ t[ 1 ] ] )
    glVertex3fv( room_geometry[ t[ 2 ] ] )
    glEnd( )
  # end for
# end def

## -------------------------------------------------------------------------
def drawObject( obj, mode = GL_LINE_LOOP, material = 1 ):
  glBegin( mode )

  if material == 1:
    plastic()
  elif material == 2:
    metal()
  else:
    wood()
  
  for t in obj.Triangles:
    glNormal3fv( obj.Normals[ t[ 0 ] ] )
    glVertex3fv( obj.Points[ t[ 0 ] ] )
    glNormal3fv( obj.Normals[ t[ 1 ] ] )
    glVertex3fv( obj.Points[ t[ 1 ] ] )
    glNormal3fv( obj.Normals[ t[ 2 ] ] )
    glVertex3fv( obj.Points[ t[ 2 ] ] )
  # end for
  glEnd( )
# end def

## ----------------------------------------------------------d---------------

def material(ar, ag, ab, dr, dg, db, sr, sg, sb, shin):
  glMaterialfv(GL_FRONT, GL_AMBIENT, [ar, ag, ab, 1])
  glMaterialfv(GL_FRONT, GL_DIFFUSE, [dr, dg, db])
  glMaterialfv(GL_FRONT, GL_SPECULAR, [sr, sg, sb])
  glMaterialf(GL_FRONT, GL_SHININESS, shin * 128)

def emerald():
  material(0.0215, 0.1745, 0.0215, 0.07568, 0.61424, 0.07568, 0.633, 0.727811, 0.633, 0.6)

def plastic():
  material(0.0, 0.0, 0.0,	0.55,	0.55,	0.55,	0.70,	0.70,	0.70,	0.25)

def metal():
  material(0.19125,	0.0735,	0.0225,	0.7038,	0.27048,	0.0828,	0.256777,	0.137622,	0.086014,	0.1)

def wood():
  material(0.25,	0.15,	0.06,	0.40,	0.24,	0.10,	0.77,	0.46,	0.20,	0.768)



def draw( ):
  global room_size, viewer_height, camera_angle, camera_pos, camera_height, current_material

  # -- Clear framebuffer
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

  # -- Draw stuff
  glMatrixMode( GL_MODELVIEW )
  glLoadIdentity( )

  # -- Camera
  camera_z = camera_pos * math.cos( camera_angle )
  camera_x = camera_pos * math.sin( camera_angle )
  gluLookAt( camera_x, camera_height, camera_z, 0, 0, 0, 0, 1, 0 )

  # -- Scenea
  drawOrthoBase( )
  drawRoom( )
  glColor3f( 0.4, 0.7, 0.2 )
  drawObject( myFunction, GL_TRIANGLES, current_material )

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
  gluPerspective( 45, aspect, 1e-2, 30 * room_size )
# end def

## -------------------------------------------------------------------------
def keyboard( key, x, y ):
  global camera_angle, camera_pos, camera_height, current_material
  speed = 5
  if key == b'q' or key == b'Q':
    sys.exit( 0 )
  elif key == b'a' or key == b'A':
    camera_angle -= 1e-2 * speed
    glutPostRedisplay( )
  elif key == b'd' or key == b'D':
    camera_angle += 1e-2 * speed
    glutPostRedisplay( )
  elif key == b'w' or key == b'W':
    camera_pos -= 1e-1 * speed
    glutPostRedisplay( )
  elif key == b's' or key == b'S':
    camera_pos += 1e-1 * speed
    glutPostRedisplay( )
  elif key == b'z' or key == b'Z':
    camera_height -= 1e-1 * speed
    glutPostRedisplay( )
  elif key == b'c' or key == b'C':
    camera_height += 1e-1 * speed
    glutPostRedisplay( )
  elif key == b'm' or key == b'M':
    current_material = 2
    glutPostRedisplay( )
  elif key == b'p' or key == b'P':
    current_material = 1
    glutPostRedisplay( )
  elif key == b'l' or key == b'L':
    current_material = 3
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
