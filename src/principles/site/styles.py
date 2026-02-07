"""CSS styles for the static site."""

CSS = """\
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:ital,wght@0,400;0,600;1,400&family=Rubik:wght@400;600;700&display=swap');

:root {
    --font-body: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI",
        Roboto, sans-serif;
    --font-heading: "Rubik", -apple-system, BlinkMacSystemFont, "Segoe UI",
        Roboto, sans-serif;
    --font-mono: "IBM Plex Mono", "SFMono-Regular", Consolas, monospace;
    --color-bg: #fafaf9;
    --color-text: #1c1917;
    --color-text-muted: #78716c;
    --color-link: #2563eb;
    --color-border: #d6d3d1;
    --color-code-bg: #f5f5f4;
    --color-sidebar-bg: #f5f5f4;
    --color-sidebar-active: #e7e5e4;
    --color-blockquote-bg: #f5f5f4;
    --color-blockquote-border: #a8a29e;
    --sidebar-width: 220px;
    --content-max-width: 680px;
}

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    font-size: 16px;
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body {
    font-family: var(--font-body);
    color: var(--color-text);
    background: var(--color-bg);
    line-height: 1.6;
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: var(--sidebar-width);
    min-width: var(--sidebar-width);
    background: var(--color-sidebar-bg);
    border-right: 1px solid var(--color-border);
    padding: 1rem 0;
    overflow-y: auto;
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
}

.sidebar-title {
    font-family: var(--font-heading);
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    padding: 0 1rem 1rem;
}

.sidebar-title a {
    color: inherit;
    text-decoration: none;
}

.sidebar-title a:hover {
    color: var(--color-link);
}

.sidebar nav ul {
    list-style: none;
}

.sidebar nav a {
    display: block;
    padding: 0.3rem 1rem;
    color: var(--color-text);
    text-decoration: none;
    font-family: var(--font-heading);
    font-size: 0.85rem;
}

.sidebar nav a:hover {
    color: var(--color-link);
    background: var(--color-sidebar-active);
}

.sidebar nav a.active {
    color: var(--color-link);
    background: var(--color-sidebar-active);
    font-weight: 600;
}

/* Main content */
.main {
    margin-left: var(--sidebar-width);
    flex: 1;
    min-width: 0;
    padding: 2rem 2.5rem;
    max-width: calc(var(--content-max-width) + 5rem);
    overflow-wrap: break-word;
}

.main h1,
.main h2,
.main h3,
.main h4,
.main h5,
.main h6 {
    font-family: var(--font-heading);
    line-height: 1.1;
    letter-spacing: 0.02em;
    overflow-wrap: break-word;
}

.main h1 {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    padding-top: 0.5rem;
}

.main h2 {
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
    padding-top: 0.5rem;
}

.main h3 {
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

.main p {
    margin-bottom: 1rem;
}

.main ul,
.main ol {
    margin-bottom: 1rem;
    padding-left: 1.5rem;
}

.main li {
    margin-bottom: 0.4rem;
}

.main a {
    color: var(--color-link);
    font-weight: 600;
    text-decoration: none;
}

.main a:visited {
    color: var(--color-link);
}

.main a:hover {
    text-decoration: underline;
}

/* Blockquotes */
blockquote {
    padding: 0.75rem 1rem;
    margin: 0 0 0.75rem;
    border-left: 4px solid var(--color-blockquote-border);
    background: var(--color-blockquote-bg);
    font-style: italic;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* Description/essence text */
.description {
    color: var(--color-text-muted);
    margin-bottom: 1.5rem;
}

.essence {
    font-style: italic;
    color: var(--color-text-muted);
    font-size: 1.05rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

/* Breadcrumb */
.breadcrumb {
    font-family: var(--font-heading);
    font-size: 0.8rem;
    color: var(--color-text-muted);
    margin-bottom: 1rem;
}

.breadcrumb a {
    color: var(--color-text-muted);
    font-weight: 400;
}

.breadcrumb a:hover {
    color: var(--color-link);
}

/* Principle list items */
.principle-list {
    list-style: none;
    padding: 0;
}

.principle-list li {
    padding: 0.75rem 0;
}

.principle-list .principle-title a {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.95rem;
}

.principle-list .principle-essence {
    font-size: 0.85rem;
    color: var(--color-text);
    margin-top: 0.2rem;
}

/* Group cards on index page */
.group-list {
    list-style: none;
    padding: 0;
}

.group-list li {
    padding: 0.75rem 0;
}

.group-list .group-name a {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 1.05rem;
}

.group-list .group-description {
    font-size: 0.85rem;
    color: var(--color-text);
    margin-top: 0.2rem;
}

.group-list .group-count {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-top: 0.1rem;
}

/* Related principles */
.related {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-border);
}

.related h3 {
    margin-top: 0;
}

/* Tags */
.tags {
    margin-top: 1rem;
}

.tag {
    display: inline-block;
    font-size: 0.7rem;
    padding: 0.1rem 0.45rem;
    background: var(--color-code-bg);
    border-radius: 3px;
    color: var(--color-text-muted);
    margin-right: 0.3rem;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
}

th, td {
    padding: 0.4rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

th {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.8rem;
}

/* Code */
code {
    font-family: var(--font-mono);
    font-size: 0.875em;
    background: var(--color-code-bg);
    padding: 0.15em 0.3em;
    border-radius: 3px;
}

pre {
    background: var(--color-code-bg);
    padding: 1rem;
    overflow-x: auto;
    border-radius: 4px;
    margin-bottom: 0.75rem;
    line-height: 1.5;
}

pre code {
    background: none;
    padding: 0;
}

/* Principle page ID label */
.principle-id {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--color-text-muted);
    letter-spacing: 0.03em;
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        position: static;
        width: 100%;
        min-width: 100%;
        border-right: none;
        border-bottom: 1px solid var(--color-border);
        padding: 1rem 0;
    }

    body {
        flex-direction: column;
    }

    .main {
        margin-left: 0;
        padding: 1.5rem 1rem;
    }
}
"""
