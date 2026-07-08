# docs-as-code

[![Build, publish and sign](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/doughgle/docs-as-code/actions/workflows/docker-publish.yml)

Builder container image for docs-as-code tooling. Used as the single source of
truth for documentation tool versions across projects.

## Included Tools

| Tool | Purpose | Source |
|---|---|---|
| [Vale](https://vale.sh) | Prose linter | `jdkato/vale` |
| [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | Markdown linter | `npm` (`^0.22.0`) |
| [htmltest](https://github.com/wjdp/htmltest) | HTML proofer | `wjdp/htmltest` |
| [Hugo](https://gohugo.io) | Static site generator | `hugomods/hugo` |
| [Lychee](https://lychee.cli.rs) | Link checker | `lycheeverse/lychee` |

## Usage

```bash
# Pull the image
docker pull ghcr.io/doughgle/docs-as-code:main

# Verify tool versions
docker run --rm ghcr.io/doughgle/docs-as-code:main \
  sh -c 'vale --version && markdownlint-cli2 --version && htmltest --version && hugo version && lychee --version'

# Run checks on your documentation
docker run --rm -v $(pwd):/workspace -w /workspace \
  ghcr.io/doughgle/docs-as-code:main \
  sh -c 'markdownlint-cli2 . && vale . && lychee .'
```

## CI

The image is built on pushes to `main` (when `Containerfile`, `package.json`, or
`docker-publish.yml` change), on version tags (`v*.*.*`), and on pull requests.
Builds are signed with [cosign](https://github.com/sigstore/cosign) and pushed
to `ghcr.io/doughgle/docs-as-code`.

[Workflow](.github/workflows/docker-publish.yml)

## License

[MIT](LICENSE)
