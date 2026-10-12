// Buggy ! TODO: Fix it

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STATES 256
#define MAX_TRANSITIONS (MAX_STATES)

typedef struct Transition
{
    char symbol;
    int to_state;
    struct Transition *next;
} Transition;

typedef struct State
{
    int id;
    int is_final;
    Transition *transitions;
} State;

typedef struct NFA
{
    State states[MAX_STATES];
    int start_state;
    int num_states;
} NFA;

typedef struct DFA
{
    int transitions[MAX_STATES][128]; // ASCII characters
    int is_final[MAX_STATES];
    int start_state;
    int num_states;
} DFA;

NFA *create_nfa(int num_states)
{
    NFA *nfa = (NFA *)malloc(sizeof(NFA));
    nfa->num_states = num_states;
    for (int i = 0; i < num_states; i++)
    {
        nfa->states[i].id = i;
        nfa->states[i].is_final = 0;
        nfa->states[i].transitions = NULL;
    }
    return nfa;
}

void add_transition(NFA *nfa, int from, char symbol, int to)
{
    Transition *t = (Transition *)malloc(sizeof(Transition));
    t->symbol = symbol;
    t->to_state = to;
    t->next = nfa->states[from].transitions;
    nfa->states[from].transitions = t;
}

void set_final_state(NFA *nfa, int state)
{
    nfa->states[state].is_final = 1;
}

void free_nfa(NFA *nfa)
{
    for (int i = 0; i < nfa->num_states; i++)
    {
        Transition *t = nfa->states[i].transitions;
        while (t != NULL)
        {
            Transition *next = t->next;
            free(t);
            t = next;
        }
    }
    free(nfa);
}
NFA *regex_to_nfa(const char *regex)
{
    NFA *nfa = create_nfa(MAX_STATES);
    int state_count = 0;
    int start_state = state_count++;
    int current_state = start_state;

    int start_stack[MAX_STATES];
    int end_stack[MAX_STATES];
    int stack_size = 0;

    for (int i = 0; i < strlen(regex); i++)
    {
        char c = regex[i];
        printf("Processing: %c\n", c);

        switch (c)
        {
        case '(':
            start_stack[stack_size] = current_state;
            end_stack[stack_size] = -1; // Placeholder for end state
            stack_size++;
            break;

        case ')':
            if (stack_size == 0)
            {
                printf("Error: Unmatched closing parenthesis.\n");
                return NULL;
            }
            stack_size--;
            if (end_stack[stack_size] != -1)
            {
                current_state = end_stack[stack_size];
            }
            break;

        case '|':
            end_stack[stack_size - 1] = state_count++;
            add_transition(nfa, start_stack[stack_size - 1], '\0', current_state);
            current_state = state_count++;
            add_transition(nfa, current_state, '\0', end_stack[stack_size - 1]);
            break;

        case '*':
            add_transition(nfa, current_state, '\0', start_stack[stack_size - 1]);
            add_transition(nfa, start_stack[stack_size - 1], '\0', current_state);
            break;

        case '+':
            add_transition(nfa, current_state, '\0', start_stack[stack_size - 1]);
            break;

        case '.':
            add_transition(nfa, current_state, '\0', ++state_count);
            current_state = state_count;
            break;

        default:
            add_transition(nfa, current_state, c, ++state_count);
            current_state = state_count;
            break;
        }
    }

    set_final_state(nfa, current_state);
    nfa->num_states = state_count + 1;
    return nfa;
}

DFA *nfa_to_dfa(NFA *nfa)
{
    DFA *dfa = (DFA *)malloc(sizeof(DFA));
    memset(dfa->transitions, -1, sizeof(dfa->transitions));
    memset(dfa->is_final, 0, sizeof(dfa->is_final));
    dfa->num_states = 1; // start with one state
    dfa->start_state = 0;

    // Conversion simplifiée, ne gère pas toutes les transitions NFA -> DFA.
    for (int i = 0; i < nfa->num_states; i++)
    {
        State *state = &nfa->states[i];
        if (state->is_final)
        {
            dfa->is_final[i] = 1;
        }
        Transition *t = state->transitions;
        while (t != NULL)
        {
            dfa->transitions[i][t->symbol] = t->to_state;
            t = t->next;
        }
    }
    return dfa;
}

int match(DFA *dfa, const char *input)
{
    int current_state = dfa->start_state;
    for (int i = 0; i < strlen(input); i++)
    {
        char c = input[i];
        if (dfa->transitions[current_state][(int)c] == -1)
        {
            return 0; // No valid transition
        }
        current_state = dfa->transitions[current_state][(int)c];
    }
    return dfa->is_final[current_state];
}

void print_nfa(NFA *nfa)
{
    printf("NFA Transition Table:\n");
    printf("State\tInput\tNext States\n");
    for (int i = 0; i < nfa->num_states; i++)
    {
        Transition *t = nfa->states[i].transitions;
        while (t != NULL)
        {
            printf("%d\t%c\t%d\n", i, t->symbol == '\0' ? 'e' : t->symbol, t->to_state);
            t = t->next;
        }
    }
    printf("Final States: ");
    for (int i = 0; i < nfa->num_states; i++)
    {
        if (nfa->states[i].is_final)
        {
            printf("%d ", i);
        }
    }
    printf("\n\n");
}

void print_dfa(DFA *dfa)
{
    printf("DFA Transition Table:\n");
    printf("State\tInput\tNext State\n");
    for (int i = 0; i < dfa->num_states; i++)
    {
        for (int c = 0; c < 128; c++)
        { // 128 for all ASCII characters
            if (dfa->transitions[i][c] != -1)
            {
                printf("%d\t%c\t%d\n", i, c, dfa->transitions[i][c]);
            }
        }
    }
    printf("Final States: ");
    for (int i = 0; i < dfa->num_states; i++)
    {
        if (dfa->is_final[i])
        {
            printf("%d ", i);
        }
    }
    printf("\n\n");
}

void print_mermaid_nfa(NFA *nfa)
{
    printf("```mermaid\n");
    printf("stateDiagram-v2\n");

    for (int i = 0; i < nfa->num_states; i++)
    {
        Transition *t = nfa->states[i].transitions;
        while (t != NULL)
        {
            char symbol = (t->symbol == '\0') ? 'e' : t->symbol;
            printf("    S%d --> S%d : %c\n", i, t->to_state, symbol);
            t = t->next;
        }
    }

    for (int i = 0; i < nfa->num_states; i++)
    {
        if (nfa->states[i].is_final)
        {
            printf("    state S%d <<final>>\n", i);
        }
    }

    printf("```\n");
}

int main()
{
    const char *regex = "XY"; // Un exemple d'expression régulière.
    NFA *nfa = regex_to_nfa(regex);
    print_nfa(nfa); // Afficher la table de transition du NFA
    print_mermaid_nfa(nfa);

    DFA *dfa = nfa_to_dfa(nfa);
    print_dfa(dfa); // Afficher la table de transition du DFA

    const char *test_str = "XY";
    if (match(dfa, test_str))
    {
        printf("Match found!\n");
    }
    else
    {
        printf("No match found.\n");
    }

    free_nfa(nfa);
    free(dfa);
}
