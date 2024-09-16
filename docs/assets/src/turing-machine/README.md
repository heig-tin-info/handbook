# Turing Machine Simulator

This is a simple Turing Machine simulator written in C. The program reads a number in binary and adds one to it.

```bash
gcc turing.c -o turing
echo "100101101011" >> ./turing
100101101100
```

The algorithm is the following:

```text
input: '101'
table:
  right:
    [1,0]: R
    ' '  : {L: carry}
  carry:
    1      : {write: 0, L}
    [0,' ']: {write: 1, L: done}
done:
```