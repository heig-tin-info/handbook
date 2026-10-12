#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <SOIL/SOIL.h>
#include <cglm/cglm.h>
#include <stdio.h>

// Variables globales pour la position et la direction de la caméra
vec3 camera_pos = {0.0f, 1.70f, 3.0f};
vec3 camera_front = {0.0f, 0.0f, -1.0f};
vec3 camera_up = {0.0f, 1.0f, 0.0f};
vec3 camera_right;

float yaw = -90.0f, pitch = 0.0f;
float last_x = 800 / 2.0, last_y = 600 / 2.0;
float fov = 45.0f;
int first_mouse = 1;

float delta_time = 0.0f;
float last_frame = 0.0f;
float camera_speed = 2.5f;
float sprint_multiplier = 2.0f;

// Fonction de rappel pour la gestion de la souris
void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
   if (first_mouse) {
      last_x = xpos;
      last_y = ypos;
      first_mouse = 0;
   }

   float xoffset = xpos - last_x;
   float yoffset = last_y - ypos;
   last_x = xpos;
   last_y = ypos;

   float sensitivity = 0.5f;
   xoffset *= sensitivity;
   yoffset *= sensitivity;

   yaw += xoffset;
   pitch += yoffset;

   if (pitch > 89.0f) pitch = 89.0f;
   if (pitch < -89.0f) pitch = -89.0f;

   vec3 front;
   front[0] = cos(glm_rad(yaw)) * cos(glm_rad(pitch));
   front[1] = sin(glm_rad(pitch));
   front[2] = sin(glm_rad(yaw)) * cos(glm_rad(pitch));
   glm_vec3_normalize(front);
   glm_vec3_copy(front, camera_front);

   glm_vec3_cross(camera_front, camera_up, camera_right);
   glm_vec3_normalize(camera_right);

   //  printf("Orientation de la caméra : yaw=%.2f, pitch=%.2f\n", yaw, pitch);
}

// Fonction de rappel pour les touches
void process_input(GLFWwindow* window) {
   float speed = camera_speed * delta_time;
   if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS) {
      speed *= sprint_multiplier;
   }

   vec3 temp;
   vec3 front_flat;
   glm_vec3_copy(camera_front, front_flat);
   front_flat[1] = 0.0f;
   glm_vec3_normalize(front_flat);

   if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
      glm_vec3_scale(front_flat, speed, temp);
      glm_vec3_add(camera_pos, temp, camera_pos);
   }
   if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
      glm_vec3_scale(front_flat, speed, temp);
      glm_vec3_sub(camera_pos, temp, camera_pos);
   }
   if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
      glm_vec3_scale(camera_right, speed, temp);
      glm_vec3_sub(camera_pos, temp, camera_pos);
   }
   if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
      glm_vec3_scale(camera_right, speed, temp);
      glm_vec3_add(camera_pos, temp, camera_pos);
   }
   if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS) {
      camera_pos[1] += speed;
   }
   if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS) {
      camera_pos[1] -= speed;
   }

   // printf("Position de la caméra : (%.2f, %.2f, %.2f)\n", camera_pos[0],
   //        camera_pos[1], camera_pos[2]);
}

// Fonction pour dessiner un sol avec une texture
void draw_floor() {
   float floor_vertices[][8] = {
       // Positions         // Normales         // Coordonnées de texture
       {-10.0f, 0.0f, -10.0f, 0.0f, 1.0f, 0.0f, 0.0f, 0.0f},
       {10.0f, 0.0f, -10.0f, 0.0f, 1.0f, 0.0f, 1.0f, 0.0f},
       {10.0f, 0.0f, 10.0f, 0.0f, 1.0f, 0.0f, 1.0f, 1.0f},
       {-10.0f, 0.0f, 10.0f, 0.0f, 1.0f, 0.0f, 0.0f, 1.0f}};

   unsigned int floor_indices[] = {0, 1, 2, 0, 2, 3};

   GLuint floor_vao, floor_vbo, floor_ebo;
   glGenVertexArrays(1, &floor_vao);
   glGenBuffers(1, &floor_vbo);
   glGenBuffers(1, &floor_ebo);

   glBindVertexArray(floor_vao);
   glBindBuffer(GL_ARRAY_BUFFER, floor_vbo);
   glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, floor_ebo);

   glBufferData(GL_ARRAY_BUFFER, sizeof(floor_vertices), floor_vertices,
                GL_STATIC_DRAW);

   glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(floor_indices), floor_indices,
                GL_STATIC_DRAW);

   glEnableVertexAttribArray(0);
   glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);

   glEnableVertexAttribArray(1);
   glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float),
                         (void*)(3 * sizeof(float)));

   glEnableVertexAttribArray(2);
   glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float),
                         (void*)(6 * sizeof(float)));

   glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, (void*)0);

   // glBindVertexArray(0);
   // glDeleteBuffers(1, &floor_vbo);
   // glDeleteBuffers(1, &floor_ebo);
   // glDeleteVertexArrays(1, &floor_vao);
}

char* readShaderFile(const char* filePath) {
   FILE* file = fopen(filePath, "r");
   if (!file) {
      printf("Erreur lors de l'ouverture du fichier shader : %s\n", filePath);
      return NULL;
   }

   fseek(file, 0, SEEK_END);
   long length = ftell(file);
   rewind(file);

   char* content = (char*)malloc(length + 1);
   if (!content) {
      printf("Erreur lors de l'allocation de mémoire pour le fichier shader\n");
      fclose(file);
      return NULL;
   }

   fread(content, 1, length, file);
   content[length] = '\0';
   fclose(file);

   return content;
}

GLuint compile_shader(const char* source, GLenum type) {
   GLuint shader = glCreateShader(type);
   glShaderSource(shader, 1, &source, NULL);
   glCompileShader(shader);

   int success;
   glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
   if (!success) {
      char infoLog[512];
      glGetShaderInfoLog(shader, sizeof(infoLog), NULL, infoLog);
      printf("Erreur de compilation du shader : %s\n", infoLog);
      return 0;
   }
   return shader;
}

GLuint loadShader(const char* vertexPath, const char* fragmentPath) {
   char* vertexSource = readShaderFile(vertexPath);
   char* fragmentSource = readShaderFile(fragmentPath);
   if (!vertexSource || !fragmentSource) {
      return 0;
   }

   GLuint vertexShader = compile_shader(vertexSource, GL_VERTEX_SHADER);
   GLuint fragmentShader = compile_shader(fragmentSource, GL_FRAGMENT_SHADER);

   glShaderSource(vertexShader, 1, (const GLchar* const*)&vertexSource, NULL);
   glShaderSource(fragmentShader, 1, (const GLchar* const*)&fragmentSource,
                  NULL);

   GLuint shaderProgram = glCreateProgram();
   glAttachShader(shaderProgram, vertexShader);
   glAttachShader(shaderProgram, fragmentShader);
   glLinkProgram(shaderProgram);

   int success;
   glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
   if (!success) {
      char infoLog[512];
      glGetProgramInfoLog(shaderProgram, sizeof(infoLog), NULL, infoLog);
      printf("Erreur de liaison du programme shader : %s\n", infoLog);
   }

   glDeleteShader(vertexShader);
   glDeleteShader(fragmentShader);

   free(vertexSource);
   free(fragmentSource);

   return shaderProgram;
}

GLuint loadTexture(char* path) {
   GLuint texture;
   glGenTextures(1, &texture);
   glBindTexture(GL_TEXTURE_2D, texture);

   int width, height;
   unsigned char* image =
       SOIL_load_image(path, &width, &height, 0, SOIL_LOAD_RGB);
   if (image) {
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB,
                   GL_UNSIGNED_BYTE, image);
      glGenerateMipmap(GL_TEXTURE_2D);
   } else {
      printf("Erreur lors du chargement de la texture\n");
      return 0;
   }
   SOIL_free_image_data(image);

   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
   glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

   return texture;
}

int main() {
   if (!glfwInit()) {
      printf("Failed to initialize GLFW\n");
      return -1;
   }

   GLFWwindow* window =
       glfwCreateWindow(800, 600, "OpenGL Tiling Floor", NULL, NULL);
   if (!window) {
      printf("Failed to create GLFW window\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);

   if (glewInit() != GLEW_OK) {
      printf("Failed to initialize GLEW\n");
      return -1;
   }

   glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);
   glfwSetCursorPosCallback(window, mouse_callback);
   glEnable(GL_MULTISAMPLE);
   glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
   // glEnable(GL_DEPTH_TEST);

   GLuint shader_program = loadShader("shader.vert", "shader.frag");
   GLuint albedo_texture = loadTexture("albedo.jpg");
   GLuint normal_texture = loadTexture("normal.jpg");
   GLuint height_texture = loadTexture("height.jpg");
   GLuint roughness_texture = loadTexture("roughness.jpg");

   while (!glfwWindowShouldClose(window)) {
      float current_frame = glfwGetTime();
      delta_time = current_frame - last_frame;
      last_frame = current_frame;

      process_input(window);

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      mat4 projection, view, model;
      glm_perspective(glm_rad(fov), 800.0f / 600.0f, 0.1f, 100.0f, projection);
      vec3 center;
      glm_vec3_add(camera_pos, camera_front, center);
      glm_lookat(camera_pos, center, camera_up, view);
      glm_mat4_identity(model);  // Utilisation de la matrice modèle identité

      glUseProgram(shader_program);
      glUniform3f(glGetUniformLocation(shader_program, "light_source_position"),
                  0.0f, 2.0f, 2.0f);
      glUniform3f(glGetUniformLocation(shader_program, "light_source_color"),
                  1.0f, 1.0f, 1.0f);
      glUniform3f(glGetUniformLocation(shader_program, "camera_position"), 0.0f,
                  0.0f, 3.0f);
      // Envoi des matrices au shader
      glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1,
                         GL_FALSE, (float*)projection);
      glUniformMatrix4fv(glGetUniformLocation(shader_program, "view"), 1,
                         GL_FALSE, (float*)view);
      glUniformMatrix4fv(glGetUniformLocation(shader_program, "model"), 1,
                         GL_FALSE, (float*)model);

      draw_floor();  // Dessin du sol

      glActiveTexture(GL_TEXTURE0);
      glBindTexture(GL_TEXTURE_2D, albedo_texture);
      glUniform1i(glGetUniformLocation(shader_program, "albedo"), 0);

      glActiveTexture(GL_TEXTURE1);
      glBindTexture(GL_TEXTURE_2D, normal_texture);
      glUniform1i(glGetUniformLocation(shader_program, "normal"), 1);

      glActiveTexture(GL_TEXTURE2);
      glBindTexture(GL_TEXTURE_2D, roughness_texture);
      glUniform1i(glGetUniformLocation(shader_program, "roughness"), 2);

      glActiveTexture(GL_TEXTURE3);
      glBindTexture(GL_TEXTURE_2D, height_texture);
      glUniform1i(glGetUniformLocation(shader_program, "heightMap"), 3);

      glfwSwapBuffers(window);
      glfwPollEvents();
   }

   glfwTerminate();
}
