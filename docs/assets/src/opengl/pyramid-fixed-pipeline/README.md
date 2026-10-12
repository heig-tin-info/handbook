---
# Notes on the sample next to it, not a page of the handbook. MkDocs drops
# it through `exclude_docs: README.md`; Zensical builds every file under
# `docs/`, and this is what keeps it out of the search.
search:
  exclude: true
---

# OpenGL Pyramid with old style OpenGL

Before OpenGL 3.0, OpenGL was using a fixed pipeline. This means that the rendering pipeline was fixed and you could not change it. This is not the case anymore with OpenGL 3.0 and above. However, it is still possible to use the old fixed pipeline with OpenGL 3.0 and above.

This example shows how to draw a pyramid using the old fixed pipeline in pure C.

![Pyramid](pyramid.png)

## Build

```bash
make
```
