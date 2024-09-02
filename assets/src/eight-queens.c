#include <stdbool.h>
#include <stdio.h>

#define N 8

#define EMPTY false
#define QUEEN (!EMPTY)

void printSolution(bool board[N][N]) {
   static int k = 0;
   printf("Solution %d:\n", ++k);
   for (int i = 0; i < N; ++i) {
      for (int j = 0; j < N; ++j) printf("%s ", board[i][j] ? "♛" : ".");
      printf("\n");
   }
   printf("\n");
}

bool is_safe(bool board[N][N], int row, int col) {
   // Column check
   // Line check can be omitted because we are filling
   // the board row by row
   for (int i = 0; i < row; i++)
      if (board[i][col] || board[row][i]) return false;

   // Diagonal upper left
   for (int i = row, j = col; i >= 0 && j >= 0; --i, --j)
      if (board[i][j]) return false;

   // Diagonal upper right
   for (int i = row, j = col; i >= 0 && j < N; --i, ++j)
      if (board[i][j]) return false;

   return true;
}

bool solve(bool board[N][N], int row) {
   // We have reached the end, this is a solution
   if (row >= N) {
      printSolution(board);
      return true;
   }

   bool is_solution = false;
   for (int col = 0; col < N; col++) {
      if (is_safe(board, row, col)) {
         board[row][col] = QUEEN;
         is_solution = solve(board, row + 1) || is_solution;
         board[row][col] = EMPTY;  // BACKTRACK
      }
   }

   return is_solution;
}

int main() {
   // False means empty, true means queen
   bool board[N][N] = {0};

   if (!solve(board, 0)) printf("Solution does not exist");
}