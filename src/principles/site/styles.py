"""CSS styles for the static site.

Adopts the design-kit visual language:
- Recursive variable font, monospace-first (MONO: 1 for UI/headings, MONO: 0 for prose)
- Gray + purple palette, purple as sole accent
- Square corners (radius: 0), flat hierarchy (borders, not shadows)
- CSS layer architecture: reset, tokens, defaults, components, utilities
- light-dark() semantic colors for automatic dark mode
"""

CSS = """\
@import url('https://fonts.googleapis.com/css2?family=Recursive:slnt,wght,CASL,CRSV,MONO@-15..0,300..1000,0..1,0..1,0..1&display=swap');

@layer reset, tokens, defaults, components, utilities;

/* ========================================================================
   RESET
   ======================================================================== */
@layer reset {
    *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-variation-settings: inherit;
    }

    html {
        -webkit-text-size-adjust: 100%;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        line-height: var(--font-line-height-base);
    }

    ul, ol { list-style: none; padding-inline-start: 0; }
    h1, h2, h3, h4, h5, h6 { font-weight: var(--font-weight-semibold); text-wrap: balance; }
    p { text-wrap: pretty; }
    button, input, textarea, select { font-family: inherit; font-size: inherit; }
    img, svg { display: block; max-width: 100%; }
}

/* ========================================================================
   TOKENS
   ======================================================================== */
@layer tokens {
    :root {
        color-scheme: light dark;

        /* color primitives */
        --color-white: #ffffff;
        --color-black: #000000;
        --color-gray-50:  #F5F5F5;
        --color-gray-100: #ECECED;
        --color-gray-200: #C5C3C7;
        --color-gray-300: #9F9CA2;
        --color-gray-400: #7B777F;
        --color-gray-500: #57545A;
        --color-gray-600: #363438;
        --color-gray-700: #181619;
        --color-purple-100: #F1E8FF;
        --color-purple-200: #D6B6FF;
        --color-purple-300: #BF80FF;
        --color-purple-400: #AC38FF;
        --color-purple-500: #8300CA;
        --color-purple-600: #530082;
        --color-purple-700: #280042;

        /* spacing scale */
        --spacing-xs:  0.125rem;
        --spacing-sm:  0.25rem;
        --spacing-md:  0.5rem;
        --spacing-lg:  0.75rem;
        --spacing-xl:  1rem;
        --spacing-2xl: 1.5rem;
        --spacing-3xl: 2rem;
        --spacing-4xl: 3rem;
        --spacing-5xl: 4rem;

        /* font primitives */
        --font-family: "Recursive", ui-monospace, "SFMono-Regular", Consolas, monospace;
        --font-axis-mono: 1;
        --font-axis-casl: 0;
        --font-axis-slnt: 0;
        --font-axis-crsv: 0.5;
        --font-size-2xs:  0.625rem;
        --font-size-xs:   0.75rem;
        --font-size-sm:   0.875rem;
        --font-size-base: 1rem;
        --font-size-lg:   1.125rem;
        --font-size-xl:   1.25rem;
        --font-size-2xl:  1.5rem;
        --font-size-3xl:  2rem;
        --font-size-4xl:  2.5rem;
        --font-size-5xl:  3rem;
        --font-size-display: clamp(2.5rem, 6vw, 5rem);
        --font-weight-light: 300;
        --font-weight-regular: 400;
        --font-weight-medium: 500;
        --font-weight-semibold: 600;
        --font-weight-bold: 700;
        --font-weight-extrabold: 800;
        --font-weight-black: 900;
        --font-line-height-tight:   1.1;
        --font-line-height-base:    1.5;
        --font-line-height-relaxed: 1.6;
        --font-letter-spacing-tight:  0;
        --font-letter-spacing-normal: 0.02em;
        --font-letter-spacing-wide:   0.05em;
        --font-letter-spacing-wider:  0.08em;

        /* borders (radius is always 0) */
        --border-width-thin:   1px;
        --border-width-medium: 2px;
        --border-width-thick:  3px;

        /* motion */
        --motion-duration-fast:   100ms;
        --motion-duration-normal: 200ms;
        --motion-easing-default:  ease-in-out;

        /* z */
        --z-sticky:  10;
        --z-overlay: 1000;

        /* layout — widened from design-kit defaults (220/200/680) to fit
           two-word group names + two-digit count badge in the sidebar, and
           to give the principle content column room for wrapped tables. */
        --layout-sidebar-width:      240px;
        --layout-toc-width:          220px;
        --layout-content-max-width:  760px;

        /* semantic colors (light-dark) */
        --color-bg:               light-dark(var(--color-gray-50),  var(--color-gray-700));
        --color-surface:          light-dark(var(--color-white),    var(--color-gray-600));
        --color-text:             light-dark(var(--color-gray-700), var(--color-gray-100));
        --color-text-muted:       light-dark(var(--color-gray-500), var(--color-gray-300));
        --color-text-subtle:      light-dark(var(--color-gray-400), var(--color-gray-400));
        /* Placeholder — lighter than text-muted but tuned to hit ≥4.5:1 AA
           on bg in both modes (light ~4.7:1, dark ~5.4:1). Not in the
           primitive gray ramp; this is a one-off semantic shade. */
        --color-placeholder:      light-dark(#706D73, #8F8C93);
        --color-link:             light-dark(var(--color-purple-500), var(--color-purple-300));
        --color-link-hover:       light-dark(var(--color-purple-600), var(--color-purple-200));
        --color-border:           light-dark(var(--color-gray-200), var(--color-gray-600));
        --color-border-heavy:     light-dark(var(--color-gray-400), var(--color-gray-500));
        --color-code-bg:          light-dark(var(--color-gray-100), var(--color-gray-600));
        --color-focus-ring:       light-dark(var(--color-purple-500), var(--color-purple-400));
        /* Dark value uses purple-600, not purple-700: purple-700 has nearly
           identical luminance to gray-700 page bg, so the active-nav tint and
           ::selection highlight would vanish. TOKEN_PAIR_CONTRAST in action. */
        --color-focus-ring-light: light-dark(var(--color-purple-100), var(--color-purple-600));
        --color-hover-bg:         light-dark(var(--color-gray-100), var(--color-gray-600));
        --color-active-bg:        light-dark(var(--color-gray-200), var(--color-gray-500));
        --color-syntax-keyword:   light-dark(var(--color-purple-500), var(--color-purple-300));
        --color-syntax-string:    light-dark(var(--color-gray-700), var(--color-gray-100));
        --color-syntax-comment:   light-dark(var(--color-gray-500), var(--color-gray-300));
        --color-syntax-function:  light-dark(var(--color-purple-500), var(--color-purple-300));

        /* typography semantic aliases */
        --typography-body: var(--font-family);
        --typography-mono: var(--font-family);

        /* variable-font axes (cascadable) */
        --mono: var(--font-axis-mono);
        --casl: var(--font-axis-casl);
        --slnt: var(--font-axis-slnt);
        --crsv: var(--font-axis-crsv);
        font-family: var(--font-family);
        font-variation-settings:
            'MONO' var(--mono),
            'CASL' var(--casl),
            'CRSV' var(--crsv),
            'slnt' var(--slnt);
    }

    [data-luminance="dark"]  { color-scheme: dark; }
    [data-luminance="light"] { color-scheme: light; }
}

/* ========================================================================
   DEFAULTS
   ======================================================================== */
@layer defaults {
    html {
        accent-color: var(--color-link);
        caret-color: var(--color-link);
        -webkit-tap-highlight-color: transparent;
        scrollbar-color: var(--color-border-heavy) transparent;
        scrollbar-width: thin;
        height: 100%;
    }

    ::selection { background: var(--color-focus-ring-light); color: var(--color-text); }
    ::placeholder { color: var(--color-placeholder); opacity: 1; }
    ::marker { color: var(--color-text-muted); }
    :focus-visible { outline: 2px solid var(--color-focus-ring); outline-offset: 2px; }
    :focus:not(:focus-visible) { outline: none; }

    body {
        font-family: var(--typography-body);
        --mono: 0;
        color: var(--color-text);
        background: var(--color-bg);
        line-height: var(--font-line-height-relaxed);
        height: 100%;
        overflow: hidden;
    }

    h1, h2, h3, h4, h5, h6 {
        --mono: 1;
        line-height: var(--font-line-height-tight);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
    }
    h1 { font-size: var(--font-size-2xl); font-weight: var(--font-weight-bold); }
    h2 { font-size: var(--font-size-lg);  font-weight: var(--font-weight-semibold); }
    h3 { font-size: var(--font-size-base); font-weight: var(--font-weight-semibold); }
    h4, h5, h6 { font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); }

    a {
        color: var(--color-link);
        font-weight: var(--font-weight-semibold);
        text-decoration: none;
    }
    a:hover { text-decoration: underline; color: var(--color-link-hover); }

    code {
        --mono: 1; --casl: 0;
        font-family: var(--typography-mono);
        font-size: 0.875em;
        background: var(--color-code-bg);
        padding: 0.15em 0.3em;
    }

    pre {
        background: var(--color-code-bg);
        padding: var(--spacing-xl);
        overflow-x: auto;
        line-height: var(--font-line-height-base);
        font-size: var(--font-size-sm);
        border-left: var(--border-width-medium) solid var(--color-border-heavy);
    }
    pre code { background: none; padding: 0; font-size: 1em; }

    blockquote {
        padding: var(--spacing-md) var(--spacing-xl);
        border-left: var(--border-width-thick) solid var(--color-border-heavy);
        background: var(--color-code-bg);
        font-style: italic;
    }
    blockquote p:last-child { margin-bottom: 0; }

    hr {
        border: none;
        border-top: var(--border-width-thin) solid var(--color-border);
        margin: var(--spacing-2xl) 0;
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            transition-duration: 0.01ms !important;
            animation-duration: 0.01ms !important;
        }
    }
}

/* ========================================================================
   COMPONENTS
   ======================================================================== */
@layer components {
    /* --- APP SHELL --- */
    .app-shell {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    .app-shell-header,
    .app-shell-footer { flex-shrink: 0; }
    .app-shell-body {
        display: flex;
        flex: 1;
        min-height: 0;
        overflow: hidden;
    }
    .app-shell-left,
    .app-shell-right { flex-shrink: 0; }
    .app-shell-main {
        flex: 1;
        min-width: 0;
        overflow: auto;
        scroll-behavior: smooth;
    }

    /* --- TOP HEADER BAR --- */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: var(--spacing-xl);
        padding: var(--spacing-md) var(--spacing-xl);
        border-bottom: var(--border-width-thin) solid var(--color-border);
        background: var(--color-bg);
    }
    .app-header-brand {
        --mono: 1;
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-bold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text);
        text-decoration: none;
    }
    .app-header-brand:hover { text-decoration: none; color: var(--color-text); }
    .app-header-meta {
        display: flex;
        gap: var(--spacing-xl);
        min-width: 0;
        --mono: 1;
        font-size: var(--font-size-2xs);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
    }
    .app-header-context {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 40ch;
    }
    .app-header-meta a {
        color: var(--color-text-muted);
        font-weight: var(--font-weight-regular);
    }
    .app-header-meta a:hover { color: var(--color-text); }

    /* --- SIDEBAR (LEFT) --- */
    .app-sidebar {
        position: relative;
        display: flex;
        flex-direction: column;
        width: var(--layout-sidebar-width);
        height: 100%;
        min-width: 0;
        overflow: hidden;
        border-right: var(--border-width-thin) solid var(--color-border);
    }
    .app-sidebar-main {
        flex: 1;
        overflow-x: hidden;
        overflow-y: auto;
        scrollbar-width: none;
    }
    .app-sidebar-main::-webkit-scrollbar { display: none; }

    .nav-section { padding: var(--spacing-md) 0; }
    .nav-section + .nav-section {
        border-top: var(--border-width-thin) solid var(--color-border);
    }
    .nav-section-title {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        padding: var(--spacing-md) var(--spacing-lg) var(--spacing-sm);
    }
    .nav-link {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: var(--spacing-md);
        padding: var(--spacing-sm) var(--spacing-lg);
        border-left: var(--border-width-medium) solid transparent;
        --mono: 1;
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-regular);
        color: var(--color-text-muted);
        text-decoration: none;
        transition: background var(--motion-duration-fast) var(--motion-easing-default),
                    color var(--motion-duration-fast) var(--motion-easing-default);
    }
    .nav-link:hover {
        color: var(--color-text);
        background: var(--color-hover-bg);
        text-decoration: none;
    }
    .nav-link-active {
        color: var(--color-link);
        background: var(--color-focus-ring-light);
        border-left-color: var(--color-link);
        font-weight: var(--font-weight-semibold);
    }
    .nav-link-active:hover { color: var(--color-link); }
    .nav-link-count {
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-regular);
        color: var(--color-text-subtle);
    }
    .nav-link-active .nav-link-count { color: var(--color-link); }

    /* --- TOC (RIGHT) --- */
    .app-toc {
        position: relative;
        display: flex;
        flex-direction: column;
        width: var(--layout-toc-width);
        height: 100%;
        overflow: hidden;
        border-left: var(--border-width-thin) solid var(--color-border);
    }
    .app-toc-main {
        flex: 1;
        overflow-y: auto;
        padding: var(--spacing-2xl) var(--spacing-xl);
        scrollbar-width: none;
    }
    .app-toc-main::-webkit-scrollbar { display: none; }
    .app-toc-title {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        padding-bottom: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .toc-list {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-sm);
    }
    .toc-item {
        --mono: 1;
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-regular);
        color: var(--color-text-muted);
        text-decoration: none;
        padding: var(--spacing-xs) 0 var(--spacing-xs) var(--spacing-md);
        border-left: var(--border-width-thin) solid var(--color-border);
        line-height: var(--font-line-height-base);
        transition: color var(--motion-duration-fast) var(--motion-easing-default),
                    border-color var(--motion-duration-fast) var(--motion-easing-default);
    }
    .toc-item:hover {
        color: var(--color-text);
        border-left-color: var(--color-border-heavy);
        text-decoration: none;
    }
    .toc-item-level-3 { padding-left: var(--spacing-2xl); }

    /* --- MAIN CONTENT CONTAINER --- */
    .main-content {
        padding: var(--spacing-3xl) var(--spacing-3xl) var(--spacing-5xl);
        max-width: calc(var(--layout-content-max-width) + var(--spacing-3xl) * 2);
    }
    .main-content-wide { max-width: none; }

    /* --- BREADCRUMB --- */
    .breadcrumb {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-xl);
    }
    .breadcrumb-crumb {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-medium);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        text-decoration: none;
    }
    a.breadcrumb-crumb:hover { color: var(--color-text); text-decoration: none; }
    .breadcrumb-current { color: var(--color-text); }
    .breadcrumb-separator {
        --mono: 1;
        font-size: var(--font-size-2xs);
        color: var(--color-text-subtle);
        user-select: none;
    }

    /* --- HERO (landing) --- */
    .hero { padding: var(--spacing-xl) 0 var(--spacing-md); }
    .hero-eyebrow {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        margin-bottom: var(--spacing-md);
    }
    .hero-title {
        --mono: 1;
        font-size: var(--font-size-display);
        font-weight: var(--font-weight-extrabold);
        line-height: var(--font-line-height-tight);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        margin-bottom: var(--spacing-xl);
    }
    .hero-description {
        --mono: 0;
        font-size: var(--font-size-lg);
        color: var(--color-text-muted);
        max-width: 60ch;
        line-height: var(--font-line-height-relaxed);
    }

    /* --- STATS BAR --- */
    .stats-bar {
        display: flex;
        align-items: baseline;
        gap: var(--spacing-5xl);
        padding: var(--spacing-xl) 0;
        margin: var(--spacing-2xl) 0 var(--spacing-3xl);
        border-top: var(--border-width-medium) solid var(--color-border-heavy);
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .stat-item { display: flex; flex-direction: column; gap: var(--spacing-xs); }
    .stat-value {
        --mono: 1;
        font-size: var(--font-size-3xl);
        font-weight: var(--font-weight-extrabold);
        line-height: 1;
        color: var(--color-text);
    }
    .stat-label {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
    }

    /* --- SECTION --- */
    .section { margin-top: var(--spacing-3xl); }
    .section-heading {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: var(--spacing-xl);
        padding-bottom: var(--spacing-sm);
        margin-bottom: var(--spacing-xl);
        border-bottom: var(--border-width-medium) solid var(--color-border-heavy);
    }
    .section-heading-title {
        font-size: var(--font-size-lg);
        font-weight: var(--font-weight-bold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
    }
    .section-heading-meta {
        --mono: 1;
        font-size: var(--font-size-2xs);
        color: var(--color-text-muted);
        font-weight: var(--font-weight-regular);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
    }

    /* --- PAGE TITLE (group/principle) --- */
    .page-title {
        --mono: 1;
        font-size: var(--font-size-3xl);
        font-weight: var(--font-weight-extrabold);
        line-height: var(--font-line-height-tight);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        margin-bottom: var(--spacing-md);
    }
    .page-title-prose {
        --mono: 0;
        --casl: 0.3;
        font-size: var(--font-size-2xl);
        font-weight: var(--font-weight-bold);
        line-height: var(--font-line-height-tight);
        text-transform: none;
        letter-spacing: var(--font-letter-spacing-normal);
        text-wrap: balance;
        margin-bottom: var(--spacing-md);
    }
    .page-description {
        --mono: 0;
        color: var(--color-text-muted);
        font-size: var(--font-size-base);
        line-height: var(--font-line-height-relaxed);
        margin-bottom: var(--spacing-2xl);
        max-width: 60ch;
    }

    /* --- ESSENCE (principle) --- */
    .page-essence {
        --mono: 0;
        --casl: 0.5;
        color: var(--color-text);
        font-size: var(--font-size-lg);
        line-height: var(--font-line-height-relaxed);
        margin-bottom: var(--spacing-2xl);
        max-width: 62ch;
        font-style: italic;
    }

    /* --- META STRIP --- */
    .meta-strip {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, auto));
        gap: var(--spacing-2xl);
        padding: var(--spacing-md) 0;
        margin: var(--spacing-md) 0 var(--spacing-3xl);
        border-top: var(--border-width-thin) solid var(--color-border);
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .meta-item { display: flex; flex-direction: column; gap: var(--spacing-xs); min-width: 0; }
    .meta-label {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
    }
    .meta-value {
        --mono: 1;
        font-size: var(--font-size-xs);
        color: var(--color-text);
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .meta-value a { color: var(--color-text); font-weight: var(--font-weight-regular); }
    .meta-value a:hover { color: var(--color-link); }

    /* --- DATA TABLE --- */
    .data-table-wrap {
        position: relative;
        width: 100%;
        overflow-x: auto;
        scrollbar-color: var(--color-border-heavy) transparent;
        scrollbar-width: thin;
    }
    .data-table-wrap::-webkit-scrollbar { height: 8px; }
    .data-table-wrap::-webkit-scrollbar-thumb { background: var(--color-border-heavy); }
    .data-table-wrap::-webkit-scrollbar-track { background: transparent; }

    .data-table {
        border-collapse: collapse;
        width: 100%;
        --mono: 0;
        font-size: var(--font-size-sm);
    }
    .data-table caption {
        --mono: 1;
        caption-side: top;
        font-size: var(--font-size-2xs);
        color: var(--color-text-muted);
        text-align: left;
        padding-bottom: var(--spacing-md);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
    }
    .data-table th,
    .data-table td {
        padding: var(--spacing-md) var(--spacing-lg);
        text-align: left;
        vertical-align: top;
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .data-table th {
        --mono: 1;
        font-weight: var(--font-weight-semibold);
        font-size: var(--font-size-2xs);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        border-bottom: var(--border-width-medium) solid var(--color-border-heavy);
        background: var(--color-bg);
        white-space: nowrap;
    }
    .data-table tbody tr:last-child td { border-bottom: none; }
    /* Hover boundary: one outline on the row itself rather than composing
       corner shadows on individual cells. Row-level outline is independent
       of column order, hidden columns, last-row rules, and stacked mode,
       so it can't drift out of sync with DOM structure.
       Uses --color-border-heavy, not --color-border: the latter collapses
       to the same value as --color-hover-bg in dark mode (both gray-600),
       which would make the outline invisible against the hover fill. */
    .data-table tbody tr:hover {
        background: var(--color-hover-bg);
        outline: var(--border-width-thin) solid var(--color-border-heavy);
        outline-offset: -1px;
    }

    .data-table .col-id {
        --mono: 1;
        font-size: var(--font-size-2xs);
        color: var(--color-text-muted);
        white-space: nowrap;
        letter-spacing: var(--font-letter-spacing-wide);
    }
    .data-table .col-title {
        /* Let the browser size this column to its content (capped) so the
           longest title doesn't dominate the row; essence takes the rest. */
        min-width: 14rem;
        max-width: 22rem;
    }
    .data-table .col-title a {
        font-weight: var(--font-weight-semibold);
    }
    .data-table .col-essence {
        --mono: 0;
        color: var(--color-text);
        line-height: var(--font-line-height-base);
        /* Claim the remaining space: with table-layout auto, width:100% on
           one cell tells the browser "grow me after fixed-width neighbours
           settle," so this column soaks up what id/group/count leave. */
        width: 100%;
    }

    .data-table .col-group {
        --mono: 1;
        font-size: var(--font-size-2xs);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        color: var(--color-text-muted);
        white-space: nowrap;
    }
    .data-table .col-group a { color: var(--color-text-muted); font-weight: var(--font-weight-regular); }
    .data-table .col-group a:hover { color: var(--color-link); }

    /* col-meta stacks group + id in one column, saving horizontal space. */
    .data-table .col-meta {
        --mono: 1;
        font-size: var(--font-size-2xs);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        color: var(--color-text-muted);
        white-space: nowrap;
        line-height: var(--font-line-height-base);
    }
    .data-table .col-meta .meta-group {
        display: block;
        color: var(--color-text-muted);
        font-weight: var(--font-weight-regular);
    }
    .data-table .col-meta .meta-group:hover { color: var(--color-link); }
    .data-table .col-meta .meta-id {
        display: block;
        color: var(--color-text-subtle);
        font-weight: var(--font-weight-regular);
    }
    .data-table .col-count {
        --mono: 1;
        font-size: var(--font-size-xs);
        text-align: right;
        color: var(--color-text-muted);
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
    }
    .data-table-empty {
        padding: var(--spacing-2xl);
        text-align: center;
        color: var(--color-text-muted);
        --mono: 1;
        font-size: var(--font-size-xs);
    }

    /* --- FILTER BAR --- */
    .filter-bar {
        display: flex;
        align-items: baseline;
        gap: var(--spacing-lg);
        padding: var(--spacing-md) 0;
        margin-bottom: var(--spacing-md);
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .filter-label {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        white-space: nowrap;
    }
    .filter-input {
        flex: 1;
        --mono: 1;
        font-family: var(--typography-mono);
        font-size: var(--font-size-sm);
        color: var(--color-text);
        background: transparent;
        border: none;
        padding: var(--spacing-xs) 0;
        outline: none;
        min-width: 0;
    }
    .filter-count {
        --mono: 1;
        font-size: var(--font-size-2xs);
        color: var(--color-text-muted);
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }

    /* --- TAGS --- */
    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-sm) var(--spacing-lg);
        padding: var(--spacing-md) 0;
        margin-bottom: var(--spacing-xl);
    }
    .tag {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-medium);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        color: var(--color-text-muted);
    }
    .tag::before {
        content: "#";
        color: var(--color-text-subtle);
        margin-right: 0.05em;
    }

    /* --- RELATED --- */
    .related-section { margin-top: var(--spacing-3xl); }
    .related-list { display: flex; flex-direction: column; padding: var(--spacing-md) 0; }
    .related-item {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: var(--spacing-xl);
        padding: var(--spacing-md) 0;
        border-bottom: var(--border-width-thin) solid var(--color-border);
        align-items: baseline;
    }
    .related-item:last-child { border-bottom: none; }
    .related-id {
        --mono: 1;
        font-size: var(--font-size-2xs);
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
        white-space: nowrap;
    }
    .related-title {
        --mono: 0;
        font-size: var(--font-size-sm);
        color: var(--color-link);
        font-weight: var(--font-weight-semibold);
    }

    /* --- PAGE NAV (prev/next) --- */
    .page-nav {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--spacing-xl);
        margin-top: var(--spacing-4xl);
        padding-top: var(--spacing-xl);
        border-top: var(--border-width-thin) solid var(--color-border);
    }
    .page-nav-link {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xs);
        padding: var(--spacing-lg) var(--spacing-xl);
        border: var(--border-width-thin) solid var(--color-border);
        color: var(--color-text);
        text-decoration: none;
        transition: border-color var(--motion-duration-fast) var(--motion-easing-default),
                    background var(--motion-duration-fast) var(--motion-easing-default);
    }
    .page-nav-link:hover {
        border-color: var(--color-link);
        background: var(--color-hover-bg);
        text-decoration: none;
    }
    .page-nav-link-prev { grid-column: 1; text-align: left; }
    .page-nav-link-next { grid-column: 2; text-align: right; }
    .page-nav-direction {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
    }
    .page-nav-title {
        --mono: 0;
        font-size: var(--font-size-sm);
        font-weight: var(--font-weight-semibold);
        color: var(--color-link);
        line-height: var(--font-line-height-base);
    }

    /* --- CONTENT (markdown-rendered body) --- */
    .content {
        --mono: 0;
        line-height: var(--font-line-height-relaxed);
    }
    .content h1, .content h2, .content h3, .content h4 {
        --mono: 1;
        margin-top: var(--spacing-3xl);
        margin-bottom: var(--spacing-md);
        scroll-margin-top: var(--spacing-2xl);
    }
    .content h1:first-child,
    .content h2:first-child,
    .content h3:first-child { margin-top: 0; }
    .content h1 { font-size: var(--font-size-xl); }
    .content h2 {
        font-size: var(--font-size-lg);
        padding-bottom: var(--spacing-sm);
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .content h3 { font-size: var(--font-size-base); }
    .content h4 { font-size: var(--font-size-sm); color: var(--color-text-muted); }
    .content p { margin-bottom: var(--spacing-xl); }
    .content ul, .content ol {
        padding-left: var(--spacing-2xl);
        margin-bottom: var(--spacing-xl);
    }
    .content ul { list-style: disc; }
    .content ol { list-style: decimal; }
    .content li { margin-bottom: var(--spacing-md); }
    .content ul ul, .content ol ul, .content ul ol, .content ol ol {
        margin-top: var(--spacing-sm);
        margin-bottom: 0;
    }
    .content pre { margin: var(--spacing-xl) 0; }
    .content blockquote { margin: var(--spacing-xl) 0; }

    .content table {
        border-collapse: collapse;
        width: 100%;
        --mono: 0;
        font-size: var(--font-size-sm);
        margin: var(--spacing-xl) 0;
    }
    .content th, .content td {
        padding: var(--spacing-sm) var(--spacing-lg);
        text-align: left;
        vertical-align: top;
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .content th {
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        border-bottom: var(--border-width-medium) solid var(--color-border-heavy);
    }

    .heading-anchor {
        color: inherit;
        text-decoration: none;
        font-weight: inherit;
    }
    .heading-anchor:hover { text-decoration: none; color: inherit; }
    .heading-anchor::after {
        content: " #";
        color: transparent;
        font-weight: var(--font-weight-regular);
        transition: color var(--motion-duration-fast) var(--motion-easing-default);
    }
    .heading-anchor:hover::after { color: var(--color-text-muted); }

    /* --- SYNTAX HIGHLIGHTING (light-touch) --- */
    .language-python .kw,
    .language-lean .kw { color: var(--color-syntax-keyword); }
    .language-python .str,
    .language-lean .str { color: var(--color-syntax-string); }
    .comment,
    .language-python .comment,
    .language-lean .comment {
        color: var(--color-syntax-comment);
        --slnt: -12;
    }
}

/* ========================================================================
   UTILITIES
   ======================================================================== */
@layer utilities {
    .sr-only {
        position: absolute;
        width: 1px; height: 1px;
        padding: 0; margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    .sr-only:focus-visible {
        position: fixed;
        top: var(--spacing-md);
        left: var(--spacing-md);
        width: auto; height: auto;
        padding: var(--spacing-md) var(--spacing-xl);
        margin: 0;
        overflow: visible;
        clip: auto;
        white-space: normal;
        background: var(--color-bg);
        color: var(--color-link);
        --mono: 1;
        font-size: var(--font-size-xs);
        font-weight: var(--font-weight-semibold);
        border: var(--border-width-medium) solid var(--color-focus-ring);
        z-index: var(--z-overlay);
    }

    .text-muted { color: var(--color-text-muted); }
    .font-mono { --mono: 1; }
    .font-sans { --mono: 0; }
    .font-casual { --casl: 0.5; }
    .uppercase {
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wide);
    }
}

/* ========================================================================
   RESPONSIVE
   ======================================================================== */
@media (max-width: 1200px) and (min-width: 901px) {
    .app-toc { display: none; }
}

@media (max-width: 900px) {
    html, body { height: auto; overflow: auto; }
    .app-shell { height: auto; min-height: 100vh; overflow: visible; }
    .app-shell-body { flex-direction: column; overflow: visible; }
    .app-sidebar, .app-toc {
        width: 100%;
        height: auto;
        max-height: none;
        border-right: none;
        border-left: none;
        border-bottom: var(--border-width-thin) solid var(--color-border);
    }
    .app-sidebar-main, .app-toc-main {
        overflow: visible;
    }
    .app-shell-main { overflow: visible; }
    .app-toc-main { padding: var(--spacing-xl); }
    .main-content { padding: var(--spacing-xl); }
    .app-header { padding: var(--spacing-md) var(--spacing-xl); }

    .hero-title { font-size: var(--font-size-4xl); }
    .stats-bar { gap: var(--spacing-3xl); }
    .stat-value { font-size: var(--font-size-2xl); }
    .page-nav { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
    .main-content { padding: var(--spacing-lg); }
    .hero-title { font-size: var(--font-size-3xl); }
    .page-title { font-size: var(--font-size-2xl); }
    .meta-strip { grid-template-columns: 1fr 1fr; gap: var(--spacing-xl); }

    /* Stacked table mode: each row becomes a block with labels inline.
       Column headers hide; cells promote to block-level; [data-label]
       renders the header text as a ::before pseudo; [data-primary="true"]
       cell shows without a label at a larger weight. */
    .data-table,
    .data-table tbody,
    .data-table tr,
    .data-table td {
        display: block;
        width: auto;
    }
    .data-table thead { display: none; }
    .data-table tbody tr {
        padding: var(--spacing-md) 0;
        border-bottom: var(--border-width-thin) dashed var(--color-border);
    }
    .data-table tbody tr:last-child { border-bottom: none; }
    .data-table td {
        padding: var(--spacing-xs) 0;
        border-bottom: none;
    }
    .data-table td[data-label] {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: var(--spacing-lg);
        text-align: right;
        overflow-wrap: anywhere;
    }
    .data-table td[data-label]::before {
        content: attr(data-label);
        --mono: 1;
        font-size: var(--font-size-2xs);
        font-weight: var(--font-weight-semibold);
        text-transform: uppercase;
        letter-spacing: var(--font-letter-spacing-wider);
        color: var(--color-text-muted);
        flex-shrink: 0;
        text-align: left;
    }
    .data-table td[data-primary="true"] {
        --mono: 0;
        font-size: var(--font-size-base);
        font-weight: var(--font-weight-semibold);
        padding-bottom: var(--spacing-sm);
        text-align: left;
    }
    .data-table td[data-primary="true"][data-label]::before {
        display: none;
    }
    /* Column-scoped overrides that applied in table mode don't belong in
       stacked mode; force cells back to a single visual rhythm. The
       explicit display:block also un-hides col-id which mid-width media
       queries set to display:none. */
    .data-table .col-id,
    .data-table .col-group,
    .data-table .col-count {
        display: block;
        white-space: normal;
        text-align: right;
    }
}

@media print {
    html, body { height: auto; overflow: visible; }
    .app-shell { height: auto; overflow: visible; }
    .app-shell-body { display: block; }
    .app-sidebar, .app-toc, .app-header, .page-nav { display: none; }
    .main-content { max-width: none; padding: 0; }
}
"""
