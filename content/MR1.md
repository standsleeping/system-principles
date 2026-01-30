---
id: MR1
title: "Never mock application code."
summary: "Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries. When tests would patch internal code, either refactor the code into u..."
---

Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries. When tests would patch internal code, either refactor the code into units and integrators to make it more directly testable, or write integration tests that exercise the real code paths.