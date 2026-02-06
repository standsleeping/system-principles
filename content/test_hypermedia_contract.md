---
id: TEST_HYPERMEDIA_CONTRACT
title: "System tests verify the hypermedia contract."
summary: "System tests exist to exercise navigation, links, and form submissions. Anything that can be tested without interacting with markup should not be tested here. Each test performs one action and covers one page behavior."
---

System tests exist to exercise navigation, links, and form submissions. Anything that can be tested without interacting with markup should not be tested here. Each test performs one action and covers one page behavior.

Push logic testing into unit tests. System tests answer a narrow question: does clicking this link or submitting this form produce the expected navigation and state change?

Each test file targets one page and one action. Name files accordingly: `test_[PAGE]_page_[ACTION].py`. One action means one `click()` or one `submit()` per test. If multiple systems interact, each gets its own action.

View functions are tested in isolation, separately from system tests. View tests verify that the view produces the expected structure, not that the full request cycle works.
