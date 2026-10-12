#version 330 core
layout(location = 0) in vec3 aPos;  // Position des sommets
layout(location = 1) in vec3 aNormal;  // Normales
layout(location = 2) in vec2 aTexCoord;  // Coordonnées de texture

out vec2 TexCoord;  // Passer les coordonnées au fragment shader
out vec3 FragPos;   // Position du fragment dans l'espace monde
out vec3 Normal;    // Normale interpolée
out vec3 ViewDir;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 camera_position;

void main() {
    FragPos = vec3(model * vec4(aPos, 1.0));
    Normal = mat3(transpose(inverse(model))) * aNormal;  // Transformer la normale
    ViewDir = normalize(camera_position - FragPos); // De la position du fragment à la caméra

    gl_Position = projection * view * vec4(FragPos, 1.0);
    TexCoord = aTexCoord;
}
