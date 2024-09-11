#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdbool.h>
#include <stdio.h>

// Dimensions de la fenêtre
const unsigned int WIDTH = 800, HEIGHT = 600;

// Sommets de la pyramide (base carrée)
float vertices[] = {
    // Base
    -1.0f, 0.0f, -1.0f,  // Sommet 0
    1.0f, 0.0f, -1.0f,   // Sommet 1
    1.0f, 0.0f, 1.0f,    // Sommet 2
    -1.0f, 0.0f, 1.0f,   // Sommet 3

    // Pointe
    0.0f, 1.5f, 0.0f  // Sommet 4 (pointe)
};

// Indexes pour les triangles formant la pyramide
unsigned int indices[] = {
    // Base
    0, 1, 2, 2, 3, 0,

    // Faces
    0, 1, 4, 1, 2, 4, 2, 3, 4, 3, 0, 4};

// Vertex Shader GLSL source (pas besoin de matrices ici)
const char* vertexShaderSource =
    "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(aPos, 1.0);\n"
    "}\n";

// Fragment Shader GLSL source
const char* fragmentShaderSource =
    "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main()\n"
    "{\n"
    "   FragColor = vec4(0.8, 0.6, 0.4, 1.0);  // Couleur beige pour la "
    "pyramide\n"
    "}\n";

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

unsigned int createShaderProgram(const char* vertexShaderSource,
                                 const char* fragmentShaderSource) {
   int success;
   char infoLog[512];

   // Compilation des shaders
   unsigned int vertexShader =
       compileShader(vertexShaderSource, GL_VERTEX_SHADER);
   unsigned int fragmentShader =
       compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER);

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
   // Initialisation GLFW
   if (!glfwInit()) {
      printf("Erreur lors de l'initialisation de GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

   // Création de la fenêtre
   GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "Pyramide", NULL, NULL);
   if (window == NULL) {
      printf("Erreur lors de la création de la fenêtre GLFW\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

   // Initialisation de GLEW
   glewExperimental = GL_TRUE;
   if (glewInit() != GLEW_OK) {
      printf("Erreur lors de l'initialisation de GLEW\n");
      return -1;
   }

   // Activer le test de profondeur
   glEnable(GL_DEPTH_TEST);

   // Compilation et création du programme shader
   unsigned int shaderProgram =
       createShaderProgram(vertexShaderSource, fragmentShaderSource);

   // Création des buffers pour les sommets et les indices
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
      // Traitement des entrées
      processInput(window);

      // Effacer l'écran et le tampon de profondeur
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      // Activer le programme shader
      glUseProgram(shaderProgram);

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
   return 0;
}
