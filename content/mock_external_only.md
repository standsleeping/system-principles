---
id: MOCK_EXTERNAL_ONLY
title: "Mock only external boundaries."
summary: "External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. Use helpers in `boundaries.py` to simulate HTTP, filesystem, envi..."
---

External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. Use helpers in `boundaries.py` to simulate HTTP, filesystem, environment, and session state. Keep your domain logic real.