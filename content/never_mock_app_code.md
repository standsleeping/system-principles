---
id: NEVER_MOCK_APP_CODE
title: "Never mock application code."
essence: "If you need to mock your own code, restructure it until you don't."
---

Do not patch or fake your own functions, units, or integrators. Instead, run real code paths and only mock external boundaries. When tests would patch internal code, either refactor the code into units and integrators to make it more directly testable, or write integration tests that exercise the real code paths.