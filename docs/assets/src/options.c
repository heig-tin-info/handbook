#include <getopt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Options {
    bool is_verbose;

    bool has_add;
    bool has_append;
    bool has_delete;
    bool has_create;

    char *create_name;
    char *delete_name;
    char *file_name;
} Options;

Options parse_options(int argc, char *argv[])
{
    Options options = {0};

    int c;
    static int verbose_flag;  // Set by --verbose/--brief

    for (;;) {
        static struct option long_options[] = {
            // These options set a flag.
            {"verbose", no_argument, &verbose_flag, true},
            {"brief", no_argument, &verbose_flag, false},

            // These options don’t set a flag. We distinguish them by their
            // indices.
            {"add", no_argument, 0, 'a'},
            {"append", no_argument, 0, 'b'},
            {"delete", required_argument, 0, 'd'},
            {"create", required_argument, 0, 'c'},
            {"file", required_argument, 0, 'f'},

            // Sentinel marking the end of the structure.
            {0, 0, 0, 0}};

        // getopt_long stores the option index here.
        int option_index = 0;

        c = getopt_long(argc, argv, "abc:d:f:", long_options, &option_index);

        // Detect the end of the options.
        if (c == -1) break;

        switch (c) {
            case 'a':
                options.has_add = true;
                break;

            case 'b':
                options.has_append = true;
                break;

            case 'c':
                options.create_name = optarg;
                break;

            case 'd':
                options.delete_name = optarg;
                break;

            case 'f':
                options.file_name = optarg;
                break;

            case '?':
                // getopt_long already printed an error message.
                break;

            default:
                abort();
        }
    }
    options.is_verbose = verbose_flag;

    // Parses the remaining command line arguments if got any
    while (optind < argc) printf("%s\n", argv[optind++]);

    return options;
}

int main(int argc, char **argv)
{
    Options options = parse_options(argc, argv);

    // ...
}
