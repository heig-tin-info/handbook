#version 330 core
out vec4 FragColor;

in vec2 TexCoord;
in vec3 FragPos;
in vec3 Normal;
in vec3 ViewDir;

uniform sampler2D albedo;
uniform sampler2D normal;
uniform sampler2D roughness;
uniform sampler2D heightMap;

uniform vec3 light_source_position;
uniform vec3 light_source_color;
uniform vec3 camera_position;

vec2 parallaxMapping(vec2 texCoords, vec3 viewDir) {
    float height = texture(heightMap, texCoords).r;
    float parallaxScale = 0.1;
    vec2 pOffset = viewDir.xy * (height * parallaxScale);
    return texCoords - pOffset;
}

void main() {
    vec2 newTexCoords = parallaxMapping(TexCoord, ViewDir);

    vec3 normFromMap = texture(normal, newTexCoords).rgb;
    normFromMap = normFromMap * 2.0 - 1.0;  // From [0,1] to [-1,1]
    vec3 norm = normalize(normFromMap);

    vec3 lightDir = normalize(light_source_position - FragPos);

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * light_source_color;

    float rough = texture(roughness, newTexCoords).r;
    vec3 viewDir = normalize(camera_position - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), (1.0 - rough) * 32.0);

    vec3 specular = spec * light_source_color;

    vec3 ambient = 0.2 * light_source_color;

    vec4 textureColor = texture(albedo, newTexCoords);
    FragColor = textureColor * vec4((ambient + diffuse + specular), 1.0);
}