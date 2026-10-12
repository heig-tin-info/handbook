#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <SOIL/SOIL.h>
#include <cglm/cglm.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

GLuint vao, vbo, ebo;
GLuint albedo, normal, height, roughness;
double rotate_y = 0;
double rotate_x = 0;
double rotate_z = 0;

bool showTexture = true;
bool enableBumpMapping = true;

void key_callback(GLFWwindow* window, int key, int code, int action, int mods) {
   if (action == GLFW_PRESS || action == GLFW_REPEAT) {
      if (key == GLFW_KEY_RIGHT)
         rotate_y -= 5;
      else if (key == GLFW_KEY_LEFT)
         rotate_y += 5;
      else if (key == GLFW_KEY_UP)
         rotate_x -= 5;
      else if (key == GLFW_KEY_DOWN)
         rotate_x += 5;
      else if (key == GLFW_KEY_PAGE_UP)
         rotate_z += 5;
      else if (key == GLFW_KEY_PAGE_DOWN)
         rotate_z -= 5;
   }
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

void setupVAO() {
   // Définition des vertices : position (x, y, z), normales (nx, ny, nz),
   // coordonnées texture (u, v)
   float vertices[][8] = {
       // Face arrière droite
       {0.0f, 1.0f, 0.0f, 0.0f, 0.707f, 0.707f, 0.5f, 1.0f},
       {-0.5f, 0.0f, 0.5f, 0.0f, 0.707f, 0.707f, 0.0f, 0.0f},
       {0.5f, 0.0f, 0.5f, 0.0f, 0.707f, 0.707f, 1.0f, 0.0f},

       // Face avant droite
       {0.0f, 1.0f, 0.0f, 0.707f, 0.707f, 0.0f, 0.5f, 1.0f},
       {0.5f, 0.0f, 0.5f, 0.707f, 0.707f, 0.0f, 0.0f, 0.0f},
       {0.5f, 0.0f, -0.5f, 0.707f, 0.707f, 0.0f, 1.0f, 0.0f},

       // Face avant gauche
       {0.0f, 1.0f, 0.0f, 0.0f, 0.707f, -0.707f, 0.5f, 1.0f},
       {0.5f, 0.0f, -0.5f, 0.0f, 0.707f, -0.707f, 0.0f, 0.0f},
       {-0.5f, 0.0f, -0.5f, 0.0f, 0.707f, -0.707f, 1.0f, 0.0f},

       // Face arrière gauche
       {0.0f, 1.0f, 0.0f, -0.707f, 0.707f, 0.0f, 0.5f, 1.0f},
       {-0.5f, 0.0f, -0.5f, -0.707f, 0.707f, 0.0f, 0.0f, 0.0f},
       {-0.5f, 0.0f, 0.5f, -0.707f, 0.707f, 0.0f, 1.0f, 0.0f},

       // Base (avec normales pointant vers le bas)
       {-0.5f, 0.0f, 0.5f, 0.0f, -1.0f, 0.0f, 0.0f, 0.0f},
       {0.5f, 0.0f, 0.5f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f},
       {0.5f, 0.0f, -0.5f, 0.0f, -1.0f, 0.0f, 1.0f, 1.0f},

       {-0.5f, 0.0f, 0.5f, 0.0f, -1.0f, 0.0f, 0.0f, 0.0f},
       {0.5f, 0.0f, -0.5f, 0.0f, -1.0f, 0.0f, 1.0f, 1.0f},
       {-0.5f, 0.0f, -0.5f, 0.0f, -1.0f, 0.0f, 0.0f, 1.0f}};

   glGenVertexArrays(1, &vao);
   glGenBuffers(1, &vbo);

   glBindVertexArray(vao);

   glBindBuffer(GL_ARRAY_BUFFER, vbo);
   glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

   glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
   glEnableVertexAttribArray(0);

   glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float),
                         (void*)(3 * sizeof(float)));
   glEnableVertexAttribArray(1);

   glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float),
                         (void*)(6 * sizeof(float)));
   glEnableVertexAttribArray(2);

   glBindBuffer(GL_ARRAY_BUFFER, 0);
   glBindVertexArray(0);
}

void setMat4(GLuint program, const char* name, mat4 matrix) {
   GLint location = glGetUniformLocation(program, name);
   glUniformMatrix4fv(location, 1, GL_FALSE, (const GLfloat*)matrix);
}

void display(GLuint shaderProgram) {
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

   glUseProgram(shaderProgram);

   mat4 model = GLM_MAT4_IDENTITY_INIT;
   glm_rotate(model, glm_rad((float)rotate_x), (vec3){1.0f, 0.0f, 0.0f});
   glm_rotate(model, glm_rad((float)rotate_y), (vec3){0.0f, 1.0f, 0.0f});
   glm_rotate(model, glm_rad((float)rotate_z), (vec3){0.0f, 0.0f, 1.0f});
   setMat4(shaderProgram, "model", model);

   mat4 view = GLM_MAT4_IDENTITY_INIT;
   glm_translate(view, (vec3){0.0f, 0.0f, -3.0f});
   setMat4(shaderProgram, "view", view);

   mat4 projection;
   glm_perspective(glm_rad(45.0f), 800.0f / 800.0f, 0.01f, 100.0f, projection);
   setMat4(shaderProgram, "projection", projection);

   glBindVertexArray(vao);

   glUniform3f(glGetUniformLocation(shaderProgram, "light_source_position"),
               0.0f, 2.0f, 2.0f);
   glUniform3f(glGetUniformLocation(shaderProgram, "light_source_color"), 1.0f,
               1.0f, 1.0f);
   glUniform3f(glGetUniformLocation(shaderProgram, "camera_position"), 0.0f,
               0.0f, 3.0f);

   glActiveTexture(GL_TEXTURE0);
   glBindTexture(GL_TEXTURE_2D, albedo);
   glUniform1i(glGetUniformLocation(shaderProgram, "albedo"), 0);

   glActiveTexture(GL_TEXTURE1);
   glBindTexture(GL_TEXTURE_2D, normal);
   glUniform1i(glGetUniformLocation(shaderProgram, "normal"), 1);
   glActiveTexture(GL_TEXTURE2);
   glBindTexture(GL_TEXTURE_2D, roughness);
   glUniform1i(glGetUniformLocation(shaderProgram, "roughness"), 2);
   glActiveTexture(GL_TEXTURE3);
   glBindTexture(GL_TEXTURE_2D, height);
   glUniform1i(glGetUniformLocation(shaderProgram, "heightMap"), 3);

   glDrawArrays(GL_TRIANGLES, 0, 18);
   glBindVertexArray(0);

   glfwSwapBuffers(glfwGetCurrentContext());
}

int main() {
   if (!glfwInit()) {
      printf("Échec de l'initialisation de GLFW\n");
      return -1;
   }

   GLFWwindow* window =
       glfwCreateWindow(800, 800, "Pyramid with OpenGL 3.3", NULL, NULL);
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

   // Enable anti-aliasing 8x
   glEnable(GL_MULTISAMPLE);
   glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);

   GLuint shaderProgram = loadShader("shader.vert", "shader.frag");

   setupVAO();
   albedo = loadTexture("albedo.jpg");
   normal = loadTexture("normal.jpg");
   height = loadTexture("height.jpg");
   roughness = loadTexture("roughness.jpg");

   glEnable(GL_DEPTH_TEST);
   glfwSetKeyCallback(window, key_callback);
   while (!glfwWindowShouldClose(window)) {
      display(shaderProgram);
      glfwPollEvents();
   }

   glfwDestroyWindow(window);
   glfwTerminate();
}
