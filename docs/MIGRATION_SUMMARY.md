# Matthew Field website migration summary

This bundle was generated from the archived Hugo site and reshaped for the current Academic Pages / Jekyll repository.

## Migrated content

- About / homepage content
- CV page content
- Navigation
- 28 publication entries
- 3 project entries
- PDF CV
- Master bibliography and per-paper BibTeX files
- Optional organization / branding images copied from the old site

## Intentionally excluded

These items looked like template/demo content rather than Matthew Field-specific content, so they were not migrated:

- `content/publication/preprint/` (dummy example preprint)
- `content/post/` (template blog/news posts)
- `content/teaching/js/` and `content/teaching/python/` (template teaching/demo pages)

## Old-to-new mapping

- `content/authors/admin/_index.md` -> `_config.yml`, `_pages/about.md`, `_pages/cv.md`
- `content/publication/*/index.md` -> `_publications/*.md`
- `content/project/*/index.md` -> `_portfolio/*.md`
- `static/uploads/CV.pdf` -> `files/CV.pdf`
- `publications.bib` -> `files/publications.bib` and `files/bib/*.bib`
