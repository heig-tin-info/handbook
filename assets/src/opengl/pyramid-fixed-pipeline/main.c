/** Pyramid with texture, lighting, fog, transparency
 * for OpenGL 1 with the obsolete fixed pipeline
 */
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <SOIL/SOIL.h>
#include <stdbool.h>
#include <stdio.h>

double rotate_y = 0;
double rotate_x = 0;
double rotate_z = 0;
GLuint texture, bumpMap;

bool showTexture = true;
bool showFog = true;
bool showLighting = true;
bool enableTransparency = true;
bool enableBumpMapping = true;

void key_callback(GLFWwindow* window, int key, int code, int action, int mods) {
   if (action == GLFW_PRESS || action == GLFW_REPEAT) {
      if (key == GLFW_KEY_RIGHT)
         rotate_y -= 5;
      else if (key == GLFW_KEY_LEFT)
         rotate_y += 5;
      else if (key == GLFW_KEY_UP)
         rotate_x += 5;
      else if (key == GLFW_KEY_DOWN)
         rotate_x -= 5;
      else if (key == GLFW_KEY_PAGE_UP)
         rotate_z += 5;
      else if (key == GLFW_KEY_PAGE_DOWN)
         rotate_z -= 5;

      else if (key == GLFW_KEY_T)
         showTexture = !showTexture;
      else if (key == GLFW_KEY_F)
         showFog = !showFog;
      else if (key == GLFW_KEY_L)
         showLighting = !showLighting;
      else if (key == GLFW_KEY_A)
         enableTransparency = !enableTransparency;
   }
}

void loadTexture() {
   glEnable(GL_TEXTURE_2D);
   texture = SOIL_load_OGL_texture("normal.jpg", SOIL_LOAD_AUTO,
                                   SOIL_CREATE_NEW_ID, SOIL_FLAG_INVERT_Y);

   if (!texture)
      printf("Erreur lors du chargement de la texture ou bump map\n");

   glBindTexture(GL_TEXTURE_2D, texture);
   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
}

void display() {
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
   glLoadIdentity();

   glRotatef(rotate_x, 1.0, 0.0, 0.0);
   glRotatef(rotate_y, 0.0, 1.0, 0.0);
   glRotatef(rotate_z, 0.0, 0.0, 1.0);

   glTranslatef(0.0, -0.3, 0.0);

   if (showTexture) {
      glEnable(GL_TEXTURE_2D);
      glBindTexture(GL_TEXTURE_2D, texture);
   } else {
      glDisable(GL_TEXTURE_2D);
   }

   if (enableTransparency) {
      glEnable(GL_BLEND);
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
   } else {
      glDisable(GL_BLEND);
   }

   if (showLighting) {
      glEnable(GL_LIGHTING);
   } else {
      glDisable(GL_LIGHTING);
   }

   GLfloat alpha = 0.8;

   glBegin(GL_TRIANGLES);
   glNormal3f(0.0, 0.5, 1.0);
   glColor4f(1.0, 0.0, 0.0, alpha);
   glTexCoord2f(0.5, 1.0);
   glVertex3f(0.0, 1.0, 0.0);

   glColor4f(0.0, 1.0, 0.0, alpha);
   glTexCoord2f(0.0, 0.0);
   glVertex3f(-0.5, 0.0, 0.5);

   glColor4f(0.0, 0.0, 1.0, alpha);
   glTexCoord2f(1.0, 0.0);
   glVertex3f(0.5, 0.0, 0.5);

   // Face droite
   glNormal3f(1.0, 0.5, 0.0);
   glColor4f(1.0, 0.0, 0.0, alpha);
   glTexCoord2f(0.5, 1.0);
   glVertex3f(0.0, 1.0, 0.0);

   glColor4f(0.0, 0.0, 1.0, alpha);
   glTexCoord2f(1.0, 0.0);
   glVertex3f(0.5, 0.0, 0.5);

   glColor4f(1.0, 1.0, 0.0, alpha);
   glTexCoord2f(0.0, 0.0);
   glVertex3f(0.5, 0.0, -0.5);

   // Face arrière
   glNormal3f(0.0, 0.5, -1.0);
   glColor4f(1.0, 0.0, 0.0, alpha);
   glTexCoord2f(0.5, 1.0);
   glVertex3f(0.0, 1.0, 0.0);

   glColor4f(1.0, 1.0, 0.0, alpha);
   glTexCoord2f(1.0, 0.0);
   glVertex3f(0.5, 0.0, -0.5);

   glColor4f(0.0, 1.0, 1.0, alpha);
   glTexCoord2f(0.0, 0.0);
   glVertex3f(-0.5, 0.0, -0.5);

   // Face gauche
   glNormal3f(-1.0, 0.5, 0.0);
   glColor4f(1.0, 0.0, 0.0, alpha);
   glTexCoord2f(0.5, 1.0);
   glVertex3f(0.0, 1.0, 0.0);

   glColor4f(0.0, 1.0, 1.0, alpha);
   glTexCoord2f(0.0, 0.0);
   glVertex3f(-0.5, 0.0, -0.5);

   glColor4f(0.0, 1.0, 0.0, alpha);
   glTexCoord2f(1.0, 0.0);
   glVertex3f(-0.5, 0.0, 0.5);

   glEnd();

   // Base (quadrilatère)
   glBegin(GL_QUADS);
   glNormal3f(0.0, -1.0, 0.0);
   glColor4f(0.0, 1.0, 0.0, alpha);
   glTexCoord2f(0.0, 1.0);
   glVertex3f(-0.5, 0.0, 0.5);

   glColor4f(0.0, 0.0, 1.0, alpha);
   glTexCoord2f(1.0, 1.0);
   glVertex3f(0.5, 0.0, 0.5);

   glColor4f(1.0, 1.0, 0.0, alpha);
   glTexCoord2f(1.0, 0.0);
   glVertex3f(0.5, 0.0, -0.5);

   glColor4f(0.0, 1.0, 1.0, alpha);
   glTexCoord2f(0.0, 0.0);
   glVertex3f(-0.5, 0.0, -0.5);
   glEnd();

   glfwSwapBuffers(glfwGetCurrentContext());
}

void setupLighting() {
   glEnable(GL_LIGHTING);

   GLfloat ambientLight[] = {0.3f, 0.3f, 0.3f, 1.0f};
   glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientLight);

   GLfloat lightPos[] = {-1.0f, 0.0f, -1.0f, 1.0f};
   GLfloat lightDiffuse[] = {1.0f, 1.0f, 1.0f, 1.0f};
   GLfloat lightSpecular[] = {1.0f, 1.0f, 1.0f, 1.0f};

   glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
   glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse);
   glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular);
   glEnable(GL_LIGHT0);

   GLfloat lightPos2[] = {1.0f, 1.0f, 1.0f, 1.0f};
   GLfloat lightDiffuse2[] = {0.5f, 0.5f, 0.5f, 1.0f};
   glLightfv(GL_LIGHT1, GL_POSITION, lightPos2);
   glLightfv(GL_LIGHT1, GL_DIFFUSE, lightDiffuse2);
   glEnable(GL_LIGHT1);

   GLfloat mat_specular[] = {1.0, 1.0, 1.0, 1.0};
   GLfloat mat_shininess[] = {50.0};
   glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
   glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);

   glEnable(GL_COLOR_MATERIAL);
   glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE);

   glEnable(GL_DEPTH_TEST);

   if (showFog) {
      glEnable(GL_FOG);
      GLfloat fogColor[] = {0.5, 0.5, 0.5, 1.0};
      glFogfv(GL_FOG_COLOR, fogColor);
      glFogf(GL_FOG_MODE, GL_LINEAR);
      glFogf(GL_FOG_START, 1.0);
      glFogf(GL_FOG_END, 5.0);
   }
}

int main() {
   if (!glfwInit()) {
      printf("Échec de l'initialisation de GLFW\n");
      return -1;
   }

   GLFWwindow* window = glfwCreateWindow(800, 800, "Pyramid", NULL, NULL);
   if (!window) {
      printf("Échec de la création de la fenêtre GLFW\n");
      glfwTerminate();
      return -1;
   }

   glfwMakeContextCurrent(window);
   if (glewInit() != GLEW_OK) {
      printf("Échec de l'initialisation de GLEW\n");
      return -1;
   }

   glfwSetKeyCallback(window, key_callback);
   glClearColor(0.0, 0.0, 0.0, 1.0);

   setupLighting();
   loadTexture();

   while (!glfwWindowShouldClose(window)) {
      display();
      glfwPollEvents();
   }

   glfwDestroyWindow(window);
   glfwTerminate();
}
