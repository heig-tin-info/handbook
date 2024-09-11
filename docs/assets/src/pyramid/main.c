#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>

const unsigned int WIDTH = 800, HEIGHT = 600;

float vertices[] = {-1.0f, 0.0f,  -1.0f, 1.0f, 0.0f, -1.0f, 1.0f, 0.0f,
                    1.0f,  -1.0f, 0.0f,  1.0f, 0.0f, 1.5f,  0.0f};

unsigned int indices[] = {
    // Base
    0, 1, 2, 2, 3, 0,

    // Faces
    0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 4};

const char* vert_src =
    "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "uniform mat4 model;\n"
    "uniform mat4 view;\n"
    "uniform mat4 projection;\n"
    "void main() {\n"
    "   gl_Position = projection * view * model * vec4(aPos, 1.0);\n"
    "}\n";

const char* frag_src =
    "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main() {\n"
    "   FragColor = vec4(0.8, 0.6, 0.4, 1.0);\n"
    "}\n";

void multiplyMatrix4x4(float result[16], const float a[16], const float b[16]) {
   for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++) {
         result[i * 4 + j] = 0;
         for (int k = 0; k < 4; k++) {
            result[i * 4 + j] += a[i * 4 + k] * b[k * 4 + j];
         }
      }
   }
}

void identityMatrix(float matrix[16]) {
   for (int i = 0; i < 16; i++) matrix[i] = (i % 5 == 0) ? 1.0f : 0.0f;
}

void translateMatrix(float matrix[16], float x, float y, float z) {
   identityMatrix(matrix);
   matrix[12] = x;
   matrix[13] = y;
   matrix[14] = z;
}

void rotateYMatrix(float matrix[16], float angle) {
   identityMatrix(matrix);
   matrix[0] = cos(angle);
   matrix[2] = sin(angle);
   matrix[8] = -sin(angle);
   matrix[10] = cos(angle);
}

void perspectiveMatrix(float matrix[16], float fov, float aspect, float near,
                       float far) {
   const float tanHalfFov = tan(fov / 2.0f);
   for (int i = 0; i < 16; i++) matrix[i] = 0.0f;
   matrix[0] = 1.0f / (aspect * tanHalfFov);
   matrix[5] = 1.0f / tanHalfFov;
   matrix[10] = -(far + near) / (far - near);
   matrix[11] = -1.0f;
   matrix[14] = -(2.0f * far * near) / (far - near);
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
   glViewport(0, 0, width, height);
}

void processInput(GLFWwindow* window) {
   if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
      glfwSetWindowShouldClose(window, true);
}

int compileShader(const char* source, GLenum type) {
   int success;
   char infoLog[512];

   unsigned int shader = glCreateShader(type);
   glShaderSource(shader, 1, &source, NULL);
   glCompileShader(shader);

   glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
   if (!success) {
      glGetShaderInfoLog(shader, 512, NULL, infoLog);
      printf("Erreur de compilation du shader : %s\n", infoLog);
      return -1;
   }
   return shader;
}

unsigned int createShaderProgram(const char* vert_src, const char* frag_src) {
   int success;
   char infoLog[512];

   unsigned int vertexShader = compileShader(vert_src, GL_VERTEX_SHADER);
   unsigned int fragmentShader = compileShader(frag_src, GL_FRAGMENT_SHADER);

   // Création du programme shader
   unsigned int shaderProgram = glCreateProgram();
   glAttachShader(shaderProgram, vertexShader);
   glAttachShader(shaderProgram, fragmentShader);
   glLinkProgram(shaderProgram);

   // Vérification du linking
   glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
   if (!success) {
      glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
      printf("Erreur de linking du programme shader : %s\n", infoLog);
   }

   glDeleteShader(vertexShader);
   glDeleteShader(fragmentShader);

   return shaderProgram;
}

int main() {
   // Init GLFW
   if (!glfwInit()) {
      printf("Erreur lors de l'initialisation de GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

   // Create window
   GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "Pyramide", NULL, NULL);
   if (window == NULL) {
      printf("Erreur lors de la création de la fenêtre GLFW\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

   // Init GLEW
   glewExperimental = GL_TRUE;
   if (glewInit() != GLEW_OK) {
      printf("Erreur lors de l'initialisation de GLEW\n");
      return -1;
   }

   glEnable(GL_DEPTH_TEST);

   unsigned int shaderProgram = createShaderProgram(vert_src, frag_src);

   unsigned int VBO, VAO, EBO;
   glGenVertexArrays(1, &VAO);
   glGenBuffers(1, &VBO);
   glGenBuffers(1, &EBO);

   // Lier et remplir les buffers
   glBindVertexArray(VAO);

   glBindBuffer(GL_ARRAY_BUFFER, VBO);
   glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

   glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
   glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices,
                GL_STATIC_DRAW);

   glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
   glEnableVertexAttribArray(0);

   // Boucle principale
   while (!glfwWindowShouldClose(window)) {
      processInput(window);
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glUseProgram(shaderProgram);
      float projection[16];
      perspectiveMatrix(projection, M_PI / 4.0f, (float)WIDTH / (float)HEIGHT,
                        0.1f, 100.0f);

      float view[16];
      identityMatrix(view);
      translateMatrix(view, 0.0f, 0.0f, -5.0f);  // Reculer de 5 unités

      // Matrice de modèle (rotation)
      float model[16];
      identityMatrix(model);
      rotateYMatrix(model, glfwGetTime());  // Rotation en fonction du temps

      // Charger la matrice model dans le shader
      int modelLoc = glGetUniformLocation(shaderProgram, "model");
      glUniformMatrix4fv(modelLoc, 1, GL_FALSE, model);

      // Charger les matrices dans les shaders
      int viewLoc = glGetUniformLocation(shaderProgram, "view");
      int projectionLoc = glGetUniformLocation(shaderProgram, "projection");
      glUniformMatrix4fv(viewLoc, 1, GL_FALSE, view);
      glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, projection);

      // Dessiner la pyramide
      glBindVertexArray(VAO);
      glDrawElements(GL_TRIANGLES, 18, GL_UNSIGNED_INT, 0);

      // Échanger les buffers et traiter les événements
      glfwSwapBuffers(window);
      glfwPollEvents();
   }

   // Libérer les ressources
   glDeleteVertexArrays(1, &VAO);
   glDeleteBuffers(1, &VBO);
   glDeleteBuffers(1, &EBO);

   glfwTerminate();
}
