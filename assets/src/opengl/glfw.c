
#include <GLFW/glfw3.h>

int main() {
   if (!glfwInit()) return -1;
   GLFWwindow* window = glfwCreateWindow(800, 400, "Window", NULL, NULL);
   if (!window) {
      glfwTerminate();
      return -2;
   }
   glfwMakeContextCurrent(window);
   while (!glfwWindowShouldClose(window)) {
      glfwSwapBuffers(window);
      glfwPollEvents();
   }
}