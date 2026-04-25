---
id: DECLARATIVE_TEST_DOCS
title: "Declarative test documentation."
essence: "Name a test as the fact it asserts, not the activity it performs. When it passes, the sentence is true. When it fails, the sentence tells you what broke."
---

Tests are written before implementation with declarative assertion documentation. BAD: "Tests that env is loaded in non-containerized environment". GOOD: "Loads env in non-containerized environment".

Test names should read as statements of fact, not descriptions of test activity. When the test passes, the statement is true. When it fails, you know exactly what broke.