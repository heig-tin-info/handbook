
#include <queue>
#include <climits>
#include <cstring>
using namespace std;

// `M × N` matrix
#define M 10
#define N 10

// A Queue Node
struct Node
{
    // `(x, y)` represents matrix cell coordinates, and
    // `dist` represents their minimum distance from the source
    int x, y, dist;
};

// Below arrays detail all four possible movements from a cell
int row[] = { -1, 0, 0, 1 };
int col[] = { 0, -1, 1, 0 };

// Function to check if it is possible to go to position `(row, col)`
// from the current position. The function returns false if `(row, col)`
// is not a valid position or has a value 0 or already visited.
bool isValid(int mat[][N], bool visited[][N], int row, int col)
{
    return (row >= 0) && (row < M) && (col >= 0) && (col < N)
        && mat[row][col] && !visited[row][col];
}

// Find the shortest possible route in a matrix `mat` from source
// cell `(i, j)` to destination cell `(x, y)`
void BFS(int mat[][N], int i, int j, int x, int y)
{
    // construct a matrix to keep track of visited cells
    bool visited[M][N];

    // initially, all cells are unvisited
    memset(visited, false, sizeof visited);

    // create an empty queue
    queue<Node> q;

    // mark the source cell as visited and enqueue the source node
    visited[i][j] = true;
    q.push({i, j, 0});

    // stores length of the longest path from source to destination
    int min_dist = INT_MAX;

    // loop till queue is empty
    while (!q.empty())
    {
        // dequeue front node and process it
        Node node = q.front();
        q.pop();

        // `(i, j)` represents a current cell, and `dist` stores its
        // minimum distance from the source
        int i = node.x, j = node.y, dist = node.dist;

        // if the destination is found, update `min_dist` and stop
        if (i == x && j == y)
        {
            min_dist = dist;
            break;
        }

        // check for all four possible movements from the current cell
        // and enqueue each valid movement
        for (int k = 0; k < 4; k++)
        {
            // check if it is possible to go to position
            // `(i + row[k], `j` + col[k])` from current position
            if (isValid(mat, visited, i + row[k], j + col[k]))
            {
                // mark next cell as visited and enqueue it
                visited[i + row[k]][j + col[k]] = true;
                q.push({ i + row[k], j + col[k], dist + 1 });
            }
        }
    }

    if (min_dist != INT_MAX)
    {
        cout << "The shortest path from source to destination "
                "has length " << min_dist;
    }
    else {
        cout << "Destination can't be reached from a given source";
    }
}

int main()
{
    // input maze
    int mat[M][N] =
    {
        { 1, 1, 1, 1, 1, 0, 0, 1, 1, 1 },
        { 0, 1, 1, 1, 1, 1, 0, 1, 0, 1 },
        { 0, 0, 1, 0, 1, 1, 1, 0, 0, 1 },
        { 1, 0, 1, 1, 1, 0, 1, 1, 0, 1 },
        { 0, 0, 0, 1, 0, 0, 0, 1, 0, 1 },
        { 1, 0, 1, 1, 1, 0, 0, 1, 1, 0 },
        { 0, 0, 0, 0, 1, 0, 0, 1, 0, 1 },
        { 0, 1, 1, 1, 1, 1, 1, 1, 0, 0 },
        { 1, 1, 1, 1, 1, 0, 0, 1, 1, 1 },
        { 0, 0, 1, 0, 0, 1, 1, 0, 0, 1 },
    };

    // Find the shortest path from source `(0, 0)` to destination `(7, 5)`
    BFS(mat, 0, 0, 7, 5);

    return 0;
}
