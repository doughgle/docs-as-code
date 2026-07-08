# docs-as-code

[![Build, publish and sign](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml)

A pre-configured Docker image that bundles Hugo, Vale, markdownlint-cli2, htmltest, and Lychee for docs-as-code workflows. Zero setup, consistent environments across team and CI, and one image to maintain instead of many tools per machine — so you catch style issues, broken links, and formatting errors before they reach production. Pull the image, mount your content, and run the checks, or use it directly as a CI runner container to automate quality gates in every pull request.

## Why Docs-as-Code?

Docs-as-code applies software engineering practices — version control, code review, CI/CD, and automated testing — to documentation. Automated builds and parallel work through branches save time. Reduced rework and self-service publishing lower cost. Style enforcement, link validation, and peer review through pull requests raise quality. This image is the engine that makes the pipeline practical: pull it and you have every tool you need, pre-configured and consistent, from local development to production deployment.

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
