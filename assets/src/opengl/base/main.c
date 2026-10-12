#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <cglm/cglm.h>
#include <stdio.h>

// Variables globales pour la position et la direction de la caméra
vec3 camera_pos = {0.0f, 1.70f, 3.0f};  // La caméra est à 1m70 du sol
vec3 camera_front = {0.0f, 0.0f, -1.0f};
vec3 camera_up = {0.0f, 1.0f, 0.0f};
vec3 camera_right;

float yaw = -90.0f, pitch = 0.0f;
float last_x = 800 / 2.0, last_y = 600 / 2.0;
float fov = 45.0f;
int first_mouse = 1;

// Variables pour le temps et la vitesse
float delta_time = 0.0f;
float last_frame = 0.0f;
float camera_speed = 2.5f;
float sprint_multiplier = 2.0f;  // Multiplicateur de vitesse pour courir

// Fonction de rappel pour la gestion de la souris
void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
   if (first_mouse) {
      last_x = xpos;
      last_y = ypos;
      first_mouse = 0;
   }

   float xoffset = xpos - last_x;
   float yoffset =
       last_y - ypos;  // inversé car y-coordonnées vont du bas vers le haut
   last_x = xpos;
   last_y = ypos;

   float sensitivity = 0.1f;
   xoffset *= sensitivity;
   yoffset *= sensitivity;

   yaw += xoffset;
   pitch += yoffset;

   // Limiter le pitch
   if (pitch > 89.0f) pitch = 89.0f;
   if (pitch < -89.0f) pitch = -89.0f;

   vec3 front;
   front[0] = cos(glm_rad(yaw)) * cos(glm_rad(pitch));
   front[1] = sin(glm_rad(pitch));
   front[2] = sin(glm_rad(yaw)) * cos(glm_rad(pitch));
   glm_vec3_normalize(front);
   glm_vec3_copy(front, camera_front);

   // Calcul du vecteur camera_right
   glm_vec3_cross(camera_front, camera_up, camera_right);
   glm_vec3_normalize(camera_right);
}

// Fonction de rappel pour les touches
void process_input(GLFWwindow* window) {
   float speed = camera_speed * delta_time;
   if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS) {
      speed *= sprint_multiplier;  // Courir avec SHIFT
   }

   vec3 temp;
   vec3 front_flat;  // Front projeté sur le plan horizontal (Y = 0)
   glm_vec3_copy(camera_front, front_flat);
   front_flat[1] = 0.0f;  // On force Y à 0 pour un mouvement horizontal
   glm_vec3_normalize(front_flat);

   if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
      glm_vec3_scale(front_flat, speed, temp);
      glm_vec3_add(camera_pos, temp,
                   camera_pos);  // Avancer sur le plan horizontal
   }
   if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
      glm_vec3_scale(front_flat, speed, temp);
      glm_vec3_sub(camera_pos, temp,
                   camera_pos);  // Reculer sur le plan horizontal
   }
   if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
      glm_vec3_scale(camera_right, speed, temp);
      glm_vec3_sub(camera_pos, temp, camera_pos);  // Gauche
   }
   if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
      glm_vec3_scale(camera_right, speed, temp);
      glm_vec3_add(camera_pos, temp, camera_pos);  // Droite
   }
   if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS) {
      camera_pos[1] += speed;  // S'élever comme un jetpack avec Q
   }
   if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS) {
      camera_pos[1] -= speed;  // Descendre comme un jetpack avec E
   }
}

// Fonction pour dessiner le quadrillage
void draw_grid(vec3 camera_pos) {
   glBegin(GL_LINES);

   // Paramètres du brouillard
   float fog_start = 10.0f;
   float fog_end = 50.0f;

   // Taille de la grille (50x50 unités)
   float grid_size = 100.0f;
   float half_grid_size = grid_size / 2.0f;
   float grid_spacing = 1.0f;  // Espacement des lignes de la grille

   // Calcul de la position de la caméra quantifiée pour aligner le quadrillage
   float start_x =
       floor(camera_pos[0] / grid_spacing) * grid_spacing - half_grid_size;
   float start_z =
       floor(camera_pos[2] / grid_spacing) * grid_spacing - half_grid_size;

   // Dessiner la grille ancrée
   for (float i = start_x; i <= start_x + grid_size; i += grid_spacing) {
      for (float j = start_z; j <= start_z + grid_size; j += grid_spacing) {
         // Calcul de la distance de la ligne à la caméra (on utilise la
         // distance au centre de chaque ligne)
         vec3 line_center = {i, 0.0f, j};
         float distance_to_camera = glm_vec3_distance(camera_pos, line_center);

         // Calcul de l'intensité du brouillard en fonction de la distance
         float fog_factor =
             (fog_end - distance_to_camera) / (fog_end - fog_start);
         fog_factor = glm_clamp(fog_factor, 0.0f,
                                1.0f);  // On contraint la valeur entre 0 et 1

         // Couleur des lignes avec un effet de brouillard (plus loin = plus
         // estompé)
         glColor3f(0.5f * fog_factor, 0.5f * fog_factor, 0.5f * fog_factor);

         // Lignes parallèles à l'axe Z
         glVertex3f(i, 0.0f, j);
         glVertex3f(i, 0.0f, j + grid_spacing);

         // Lignes parallèles à l'axe X
         glVertex3f(i, 0.0f, j);
         glVertex3f(i + grid_spacing, 0.0f, j);
      }
   }

   glEnd();
}

int main() {
   // Initialisation GLFW
   if (!glfwInit()) {
      printf("Failed to initialize GLFW\n");
      return -1;
   }

   GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGL Grid", NULL, NULL);
   if (!window) {
      printf("Failed to create GLFW window\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);

   // Initialisation GLEW
   if (glewInit() != GLEW_OK) {
      printf("Failed to initialize GLEW\n");
      return -1;
   }

   // Capture de la souris
   glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);
   glfwSetCursorPosCallback(window, mouse_callback);

   // Paramètres OpenGL de base
   glEnable(GL_DEPTH_TEST);

   // Boucle principale
   while (!glfwWindowShouldClose(window)) {
      // Temps écoulé
      float current_frame = glfwGetTime();
      delta_time = current_frame - last_frame;
      last_frame = current_frame;

      // Gestion des entrées
      process_input(window);

      // Rendu
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      // Projection et vue
      mat4 projection, view;
      glm_perspective(glm_rad(fov), 800.0f / 600.0f, 0.1f, 100.0f, projection);
      vec3 center;
      glm_vec3_add(camera_pos, camera_front, center);
      glm_lookat(camera_pos, center, camera_up, view);

      // Appliquer la projection et la vue
      glMatrixMode(GL_PROJECTION);
      glLoadMatrixf((float*)projection);

      glMatrixMode(GL_MODELVIEW);
      glLoadMatrixf((float*)view);

      // Dessiner le quadrillage
      draw_grid(camera_pos);

      // Swap des buffers
      glfwSwapBuffers(window);
      glfwPollEvents();
   }

   // Nettoyage
   glfwTerminate();
   return 0;
}
