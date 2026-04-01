# Browser Tools Reference

Detailed usage guide for both browser automation tools supported by the `web-browser-search` skill.

## Table of Contents

- [agent-browser (Preferred)](#agent-browser-preferred)
- [playwright-cli (Fallback)](#playwright-cli-fallback)
- [Common Workflows](#common-workflows)
- [Choosing Between Tools](#choosing-between-tools)

---

## agent-browser (Preferred)

Chrome DevTools Protocol-based browser automation CLI. Preferred for its richer API and element reference system.

### Core Workflow

```bash
# 1. Open page
agent-browser open "https://example.com"

# 2. Get interactive elements (returns @refs like @e1, @e2)
agent-browser snapshot -i

# 3. Interact using refs
agent-browser click @e1
agent-browser fill @e2 "search text"
agent-browser press Enter

# 4. Re-snapshot after DOM changes
agent-browser snapshot -i

# 5. Extract content
agent-browser get text @e3
agent-browser get url
agent-browser get title

# 6. Close
agent-browser close
```

### Navigation

```bash
agent-browser open "https://example.com"
agent-browser goto "https://other-page.com"    # alias for open
agent-browser back                              # go back
agent-browser forward                           # go forward
agent-browser reload                            # reload page
```

### Snapshots

```bash
agent-browser snapshot                          # full accessibility tree
agent-browser snapshot -i                       # interactive elements only (recommended)
agent-browser snapshot -c                       # compact output
agent-browser snapshot -s "#content"            # scoped to CSS selector
```

### Element Interaction

```bash
agent-browser click @e1                         # click element
agent-browser dblclick @e1                      # double click
agent-browser fill @e2 "text"                   # clear + type
agent-browser type @e2 "text"                   # type without clearing
agent-browser press Enter                       # keyboard press
agent-browser hover @e1                         # mouse hover
agent-browser check @e1                         # check checkbox
agent-browser select @e1 "option"               # select dropdown option
agent-browser scroll down 500                   # scroll
agent-browser scrollintoview @e1                # scroll to element
agent-browser upload @e1 file.pdf               # file upload
```

### Data Extraction

```bash
agent-browser get text @e1                      # element text
agent-browser get html @e1                      # element HTML
agent-browser get value @e1                     # input value
agent-browser get attr @e1 href                 # attribute value
agent-browser get title                         # page title
agent-browser get url                           # current URL
agent-browser get count ".item"                 # count elements
```

### Waiting

```bash
agent-browser wait @e1                          # wait for element
agent-browser wait 2000                         # wait milliseconds
agent-browser wait --text "Success"             # wait for text
agent-browser wait --url "**/dashboard"         # wait for URL pattern
agent-browser wait --load networkidle           # wait for network idle
```

### Screenshots & PDFs

```bash
agent-browser screenshot                        # screenshot to temp dir
agent-browser screenshot page.png               # named screenshot
agent-browser screenshot --full                 # full page
agent-browser pdf output.pdf                    # save as PDF
```

### JavaScript Evaluation

```bash
agent-browser eval 'document.title'
agent-browser eval 'document.querySelector("meta[name=description]")?.content'
```

### Session Management

```bash
agent-browser --session myapp open "https://app.com"
agent-browser session list                      # list active sessions
agent-browser close --all                       # close all
```

### Authentication

```bash
# Method 1: Persistent profile
agent-browser --profile ~/.myapp open "https://app.com/login"
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"

# Method 2: Save/load state
agent-browser state save ./auth.json
agent-browser state load ./auth.json
```

> For full reference: see `agent-browser` skill (references/commands.md, references/authentication.md)

---

## playwright-cli (Fallback)

Playwright framework-based browser automation. Used when agent-browser is not available.

### Core Workflow

```bash
# 1. Open page
playwright-cli open "https://example.com"

# 2. Get page elements (returns refs like e1, e2)
playwright-cli snapshot

# 3. Interact using refs
playwright-cli click e1
playwright-cli fill e2 "search text" --submit   # fill + Enter
playwright-cli press Enter

# 4. Re-snapshot
playwright-cli snapshot

# 5. Extract content
playwright-cli get text e3
playwright-cli eval "document.URL"
playwright-cli eval "document.title"

# 6. Close
playwright-cli close
```

### Navigation

```bash
playwright-cli open "https://example.com"
playwright-cli goto "https://other-page.com"
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### Element Targeting

```bash
# By ref (from snapshot)
playwright-cli click e15

# By CSS selector
playwright-cli click "#main > button.submit"

# By role locator
playwright-cli click "getByRole('button', { name: 'Submit' })"

# By test ID
playwright-cli click "getByTestId('submit-button')"
```

### Data Extraction

```bash
playwright-cli get text e5                      # element text
playwright-cli eval "document.title"            # page title
playwright-cli eval "document.URL"              # current URL
playwright-cli eval "el => el.textContent" e5   # element text via JS
playwright-cli eval "el => el.getAttribute('href')" e5  # attribute
```

### Screenshots & PDFs

```bash
playwright-cli screenshot                       # default filename
playwright-cli screenshot --filename=page.png   # named
playwright-cli screenshot e5                    # element screenshot
playwright-cli pdf --filename=page.pdf          # save as PDF
```

### Tabs

```bash
playwright-cli tab-list                         # list open tabs
playwright-cli tab-new "https://example.com"    # new tab
playwright-cli tab-select 0                     # switch tab
playwright-cli tab-close                        # close current tab
```

### State Persistence

```bash
playwright-cli state-save auth.json             # save cookies + localStorage
playwright-cli state-load auth.json             # restore state
```

### Session Management

```bash
playwright-cli -s=mysession open "https://app.com"
playwright-cli list                             # list sessions
playwright-cli -s=mysession close               # close session
playwright-cli close-all                        # close all
```

> For full reference: see `playwright-cli` skill (references/session-management.md, references/storage-state.md)

---

## Common Workflows

### DOI Validation

```bash
# Using agent-browser
agent-browser open "https://doi.org/10.1038/s41586-024-07487-w"
agent-browser wait --load networkidle
FINAL_URL=$(agent-browser get url)
TITLE=$(agent-browser get title)
# If FINAL_URL is not an error page → DOI is valid
agent-browser close

# Using playwright-cli
playwright-cli open "https://doi.org/10.1038/s41586-024-07487-w"
playwright-cli eval "document.URL"
playwright-cli eval "document.title"
playwright-cli close
```

### Content Extraction from Academic Pages

```bash
# Open paper page
agent-browser open "https://publisher.com/paper/12345"
agent-browser wait --load networkidle

# Extract metadata
agent-browser eval 'document.querySelector("meta[name=citation_title]")?.content'
agent-browser eval 'document.querySelector("meta[name=citation_author]")?.content'
agent-browser eval 'document.querySelector("meta[name=citation_doi]")?.content'
agent-browser eval 'document.querySelector("meta[name=citation_journal_title]")?.content'
agent-browser eval 'document.querySelector("meta[name=citation_date]")?.content'
```

### Search + Browse Pipeline

```bash
# 1. Search
source .venv/bin/activate
python3 -c "
from duckduckgo_search import DDGS
results = DDGS().text('\"exact paper title\" site:doi.org', max_results=5)
for r in results:
    print(r['href'])
"

# 2. Browse top result
agent-browser open "https://doi.org/10.xxxx/xxxxx"
agent-browser wait --load networkidle
agent-browser get title
agent-browser close
```

---

## Choosing Between Tools

| Criteria | agent-browser | playwright-cli |
|----------|--------------|----------------|
| Element refs | `@e1` (rich) | `e1` (standard) |
| Network inspection | Yes (HAR, route, filter) | Yes (route, mock) |
| Device emulation | Yes | Yes (browsers: chrome, firefox, webkit) |
| Video recording | Yes | Yes (with chapters) |
| Semantic locators | Yes (`find text`, `find label`) | Yes (`getByRole`, `getByTestId`) |
| Test code generation | No | Yes (auto-generates Playwright tests) |
| Session management | Named sessions | Named sessions |
| Best for | Rich automation, content extraction | Testing, multi-browser support |
