# True Colors

For presenting the idea of true colors and the role of assurance contracts in protest movements.

The essay lives in [`content.md`](content.md) and is published as a website with GitHub Pages.

## Layout

- `content.md`: the essay, served as the site's home page.
- `simulation/`: Python code that renders the cascade videos cited in the essay. The `.mp4` files are published with the site; the code is not.
- `_config.yml`, `_includes/`, `Gemfile`: Jekyll site configuration (minima theme, with MathJax for `$...$` math).
- `.github/workflows/pages.yml`: builds and deploys the site on every push to `main`.

## Preview locally

```sh
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Embedding a simulation video

```html
<video controls width="100%" src="{{ '/simulation/grid_protest.mp4' | relative_url }}"></video>
```

## Publishing

Push to `main`. The first time, set **Settings → Pages → Source** to **GitHub Actions** in the GitHub repository.

To regenerate the videos, see [`simulation/README.md`](simulation/README.md).
