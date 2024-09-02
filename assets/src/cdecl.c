#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_type(char *str) {
   const char *type[] = {"int",   "char",   "short", "long",
                         "float", "double", "void"};
   const int n = sizeof(type) / sizeof(type[0]);
   for (int i = 0; i < n; i++) {
      const int len = strlen(type[i]);
      if (strncmp(str, type[i], len) == 0) return len;
   }
   return 0;
}

char *find_identifier(char *decl, size_t *len) {
   // Find first string that is not a type
   while (*decl) {
      if (isalpha(*decl)) {
         int len = is_type(decl);
         if (len) {
            decl += len;
            continue;
         }
         break;
      }
      decl++;
   }

   // Find end of identifier and its length
   char *c = decl;
   while (isalnum(*c) || *c == '_') c++;
   *len = c - decl;
   return decl;
}

char *explore_right(char *right) {
   while (*right && *right != ')') {
      if (*right == '[') {
         right++;
         printf("un tableau de ");
         while (*right != ']') {
            putchar(*right++);
         }
         putchar(' ');
      } else if (*right == '(') {
         right++;
         printf("une fonction aux arguments '");
         while (*right != ')') putchar(*right++);
         printf("' et retournant un ");
      }
      right++;
   }
   return right;
}

char *explore_left(char *left, char *start) {
   while (left >= start && *left != '(') {
      if (*left == '*') printf("pointeur sur ");
      if (*left == ']') {
         printf("un tableau de ");
         while (left >= start && *left != '[') left--;
      }
      if (*left == ')') {
         printf("une fonction retournant ");
         while (left >= start && *left != '(') left--;
      } else if (isalpha(*left)) {
         int len = 0;
         while (left >= start && isalpha(*left)) {
            left--;
            len++;
         }
         printf("%.*s ", len, left + 1);
      }
      left--;
   }
   return left;
}

void cdecl(char *decl) {
   // Step 1 : Find identifier
   size_t len;
   char *left = find_identifier(decl, &len);
   printf("L'identifiant '%.*s' est ", (int)len, left);

   // Step 2 and 3 : Explore right and left
   char *right = left + len;
   left--;
   do {
      right = explore_right(right) + 1;
      left = explore_left(left, decl) - 1;
   } while (left > decl && *right);
   putchar('\n');
}

int main() { cdecl("char (*(*foo[3])(int a))[5]"); }
