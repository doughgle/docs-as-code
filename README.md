# docs-as-code

[![Build, publish and sign](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml)

Builder container image for docs-as-code tooling. Used as the single source of
truth for documentation tool versions across projects.

## Included Tools

| Tool | Purpose | Source |
|---|---|---|
| [Vale](https://vale.sh) | Prose linter — checks style, consistency, and tone | `jdkato/vale` |
| [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | Markdown linter — catches formatting issues | `npm` (`^0.22.0`) |
| [htmltest](https://github.com/wjdp/htmltest) | HTML proofer — validates generated site output | `wjdp/htmltest` |
| [Hugo](https://gohugo.io) | Static site generator | `hugomods/hugo` |
| [Lychee](https://lychee.cli.rs) | Link checker — finds broken links in files and pages | `lycheeverse/lychee` |

## Usage

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/)

### Interactive (local development)

Run individual checks on your documentation by mounting a volume:

```bash
# Lint Markdown files
docker run --rm -v $(pwd):/src ghcr.io/doughgle/docs-as-code:main \
  markdownlint-cli2 .

# Check prose style
docker run --rm -v $(pwd):/src ghcr.io/doughgle/docs-as-code:main \
  vale .

# Check links
docker run --rm -v $(pwd):/src ghcr.io/doughgle/docs-as-code:main \
  lychee .

# Combine all checks in a single pass
docker run --rm -v $(pwd):/workspace -w /workspace \
  ghcr.io/doughgle/docs-as-code:main \
  sh -c 'markdownlint-cli2 . && vale . && lychee .'
```

### CI (GitHub Actions)

Use the image as the runner container for a GitHub Actions job:

```yaml
jobs:
  docs:
    runs-on: ubuntu-latest
    container: ghcr.io/doughgle/docs-as-code:main
    steps:
      - uses: actions/checkout@v4

      - name: Lint and check
        run: |
          vale .
          markdownlint-cli2 .
          lychee .

      - name: Build site
        run: hugo --minify

      - name: Test HTML
        run: htmltest
```

### Verify tool versions

```bash
docker run --rm ghcr.io/doughgle/docs-as-code:main \
  sh -c 'vale --version && markdownlint-cli2 --version && htmltest --version && hugo version && lychee --version'
```

## CI

The image is built on pushes to `main` (when `Containerfile`, `package.json`, or
`docker-publish.yml` change), on version tags (`v*.*.*`), and on pull requests.
Builds are signed with [cosign](https://github.com/sigstore/cosign) and pushed
to `ghcr.io/doughgle/docs-as-code`.

[Workflow](.github/workflows/docker-publish.yml)

## License

[MIT](LICENSE)
