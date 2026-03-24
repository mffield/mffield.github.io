# Guide to modifying `mffield/mffield.github.io`

## 1. What this repository is

The repository is an Academic Pages site built on Jekyll. The quickest way to think about it is:

- `_config.yml` controls site-wide metadata and sidebar/profile fields
- `_data/navigation.yml` controls the top navigation
- `_pages/` contains standalone pages such as the home page and CV
- `_publications/` contains one markdown file per publication
- `_portfolio/` contains one markdown file per project
- `files/` is where downloadable assets such as PDFs belong
- `images/` stores images used by pages or profile settings

## 2. Recommended editing workflow

### GitHub web UI
Good for small edits:
1. Open the file in GitHub.
2. Click the pencil icon.
3. Edit the Markdown or YAML.
4. Commit directly to a branch and open a pull request.

### Local workflow
Better for larger updates:
1. Clone the repo.
2. Copy this bundle into the repository root.
3. Remove the template/demo content listed in `docs/DELETE_OR_REPLACE.md`.
4. Preview locally with Jekyll.
5. Commit and push.

## 3. Running locally

### Native Ruby / Bundler
```bash
bundle install
bundle exec jekyll serve -l -H localhost
```

Then visit `http://localhost:4000`.

### Docker
```bash
docker compose up
```

## 4. How to add new publications

Create a new file in `_publications/` with a name like:

```text
2026-03-19-my-paper-title.md
```

Use front matter like:

```yaml
---
title: "My paper title"
collection: publications
category: manuscripts   # or conferences
permalink: /publication/2026-03-19-my-paper-title
excerpt: "Short one-line summary"
date: 2026-03-19
venue: "Journal or Conference Name"
paperurl: "https://doi.org/..."
bibtexurl: "/files/bib/my-paper-title.bib"
citation: 'Author A, Author B. (2026). &quot;My paper title.&quot; <i>Journal Name</i>.'
---
```

Then add a short body below the front matter. If you have BibTeX, place it in `files/bib/`.

## 5. How to add new projects

Create a new file in `_portfolio/`:

```yaml
---
title: "Project title"
collection: portfolio
permalink: /portfolio/2026-03-19-project-title
date: 2026-03-19
excerpt: "One-sentence summary"
---
```

Then write the project description in Markdown below.

## 6. How to update the homepage

Edit `_pages/about.md`. Keep the YAML front matter at the top. Everything below the second `---` is ordinary Markdown.

## 7. How to update the sidebar/profile

Edit these fields in `_config.yml`:

- `title`
- `description`
- `author.name`
- `author.bio`
- `author.location`
- `author.employer`
- social profile fields such as `github`, `linkedin`, `twitter`, `googlescholar`, `orcid`

If you change `_config.yml`, restart the local Jekyll server.

## 8. What I would do next after applying this bundle

1. Open a branch such as `content-migration`.
2. Copy in this bundle.
3. Remove the template/demo files.
4. Build locally and fix any layout issues.
5. Decide whether to keep or remove Talks, Teaching, and Blog sections.
6. Add real talk / teaching / software pages only when you have genuine content for them.

## 9. Suggested pull request title

`Migrate content from previous Hugo site into Academic Pages structure`
