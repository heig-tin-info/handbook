#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdbool.h>
#include <stdio.h>

static const GLfloat vertices[] = {
    -1.0f, -1.0f, 0.0f,  // Bottom left
    1.0f,  -1.0f, 0.0f,  // Bottom right
    0.0f,  1.0f,  0.0f,  // Top
};

const char* vertexShaderSource =
    "#version 330 core\n"
    "layout (location = 0) in vec3 position;\n"
    "void main() {\n"
    "    gl_Position = vec4(position / 2.0, 1.0);\n"
    "}\n";

const char* fragmentShaderSource =
    "#version 330 core\n"
    "out vec4 FragColor;\n"
    "void main() { FragColor = vec4(1.0, 1.0, 1.0, 1.0); }\n";

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
   glViewport(0, 0, width, height);
}

int main() {
   // Initialise GLFW
   if (!glfwInit()) {
      fprintf(stderr, "Failed to initialize GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_SAMPLES, 4);                // 4x antialiasing
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);  // We want OpenGL 3.3
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE,
                  GLFW_OPENGL_CORE_PROFILE);  // We don't want the old OpenGL

   // Open a window and create its OpenGL context
   GLFWwindow* window =
       glfwCreateWindow(800, 400, "White Triangle", NULL, NULL);
   if (window == NULL) {
      fprintf(stderr, "Error: Failed to open GLFW window.\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   if (glewInit() != GLEW_OK) {
      fprintf(stderr, "Error: Failed to initialize GLEW\n");
      return -1;
   }
   glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

   // Compile and link shaders
   unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
   glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
   glCompileShader(vertexShader);

   unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
   glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
   glCompileShader(fragmentShader);

   unsigned int shaderProgram = glCreateProgram();
   glAttachShader(shaderProgram, vertexShader);
   glAttachShader(shaderProgram, fragmentShader);
   glLinkProgram(shaderProgram);
   glUseProgram(shaderProgram);

   glDeleteShader(vertexShader);
   glDeleteShader(fragmentShader);

   // Viewport
   glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

   // Setup VAO/VBO
   unsigned int VBO = 0, VAO = 0;
   glGenVertexArrays(1, &VAO);
   glGenBuffers(1, &VBO);
   glBindVertexArray(VAO);

   glBindBuffer(GL_ARRAY_BUFFER, VBO);
   glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

   glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
   glEnableVertexAttribArray(0);

   //  Main loop
   do {
      glClear(GL_COLOR_BUFFER_BIT);
      glDrawArrays(GL_TRIANGLES, 0, 3);
      glfwSwapBuffers(window);
      glfwPollEvents();
   } while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
            glfwWindowShouldClose(window) == 0);
}