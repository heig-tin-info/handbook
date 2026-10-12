#include <raylib.h>

#define BALL_SIZE 30

int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 450;

    SetConfigFlags(FLAG_MSAA_4X_HINT);

    InitWindow(screenWidth, screenHeight, "rBouncing ball with anti-aliasing");

    Image perlinNoise = GenImagePerlinNoise(screenWidth, screenHeight, 50, 50, 4.0f);
    Texture2D texture = LoadTextureFromImage(perlinNoise);
    UnloadImage(perlinNoise);

    Vector2 ballPosition = {(float)screenWidth / 2, (float)screenHeight / 2};
    Vector2 ballSpeed = {300.0f, 250.0f};

    SetConfigFlags(FLAG_VSYNC_HINT);
    SetTargetFPS(120);

    while (!WindowShouldClose())
    {
        float deltaTime = GetFrameTime();

        ballPosition.x += ballSpeed.x * deltaTime;
        ballPosition.y += ballSpeed.y * deltaTime;

        if ((ballPosition.x >= screenWidth - BALL_SIZE) || (ballPosition.x <= BALL_SIZE))
            ballSpeed.x *= -1;

        if ((ballPosition.y >= screenHeight - BALL_SIZE) || (ballPosition.y <= BALL_SIZE))
            ballSpeed.y *= -1;

        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawTexture(texture, 0, 0, RED);

        DrawText("Bouncing Ball", 10, 10, 20, RAYWHITE);
        DrawCircleV(ballPosition, BALL_SIZE, GREEN);

        EndDrawing();
    }

    CloseWindow();
}
