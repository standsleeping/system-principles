---
id: FUNCTIONS_IN_SUBDIR
title: "Functions in subdirectory."
essence: "Keep functions in the package's `functions/` folder, separate from types and integrators. This separates 'how values transform' from 'what values are'."
---

Functions, wherever possible, are kept in the package's `functions` folder. These functions operate on the well-defined types, with their signatures serving as executable documentation of the transformations they perform.