# Test

```text
                  //   a
void foo(int a) { //   ┬ b
    int b;        //   │ ┬
    ...           //   │ │
    {             //   │ │ c
       int c;     //   │ │ ┬
       ...        //   │ │ │ d
       int d;     //   │ │ │ ┬
       ...        //   │ │ │ │
    }             //   │ │ ┴ ┴
    ...           //   │ │
}                 //   ┴ ┴
```

```mermaid
%% Les enfants bleus
graph TD
CD("CD (2)") --> C("C (1)")
CD --> D("D (1)")
```
