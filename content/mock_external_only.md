---
id: MOCK_EXTERNAL_ONLY
title: "Mock only external boundaries."
essence: "Mock the world outside your system; run everything inside it for real."
---

External system boundaries (HTTP, filesystem, environment variables, databases) must be mocked for reliable, deterministic testing. Use helpers in `boundaries.py` to simulate HTTP, filesystem, environment, and session state. Keep your domain logic real.