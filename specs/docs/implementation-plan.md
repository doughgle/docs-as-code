# Add Lychee to docs-as-code Image — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Lychee link checker to the docs-as-code builder container image, update CI verification, and rewrite the README to OSS standards.

**Architecture:** Multi-stage Containerfile addition using the official Lychee Alpine image as a source stage (`COPY --from`), keeping the existing `node:20-alpine` final base untouched. CI verify step extended with a simple `&&` chain. README rewritten to document all tools, usage patterns, and CI status.

**Tech Stack:** Docker multi-stage build, `lycheeverse/lychee:latest-alpine`, GitHub Actions (`.github/workflows/docker-publish.yml`), cosign signing.

## Global Constraints

- Final base image remains `node:20-alpine` — no base image changes
- Existing tools (Vale, htmltest, Hugo, markdownlint-cli2) must continue working
- The image build+sign+push workflow must remain functional
- No new entrypoint, CMD, or runtime changes to the image
- Lychee version is semi-pinned to `latest-alpine` (verify latest version before implementation, replace `latest-alpine` with a specific version tag if pinning is desired)
- All `{owner}` and `{repo}` placeholders in README must be replaced with actual GitHub org/user and repo name

---

### Task 1: Add Lychee to Containerfile

**Files:**
- Modify: `Containerfile`

**Interfaces:**
- Consumes: Existing multi-stage structure (`FROM jdkato/vale`, `FROM wjdp/htmltest`, `FROM hugomods/hugo`, `FROM node:20-alpine`)
- Produces: Image with `/usr/local/bin/lychee` available

- [x] **Step 1: Add source stage after the existing Hugo source stage**

Add after line 4 (`FROM hugomods/hugo:exts AS hugo`):

```dockerfile
# Lychee link checker (Alpine variant for musl compatibility)
FROM lycheeverse/lychee:latest-alpine AS lychee
```

- [x] **Step 2: Add COPY command in the final stage after the Hugo COPY**

Add after line 15 (`COPY --from=hugo /usr/bin/hugo /usr/local/bin/`):

```dockerfile
COPY --from=lychee /usr/local/bin/lychee /usr/local/bin/
```

Full resulting `Containerfile`:

```dockerfile
# Source Stages (Dependabot tracks these)
FROM jdkato/vale:latest AS vale
FROM wjdp/htmltest:latest AS htmltest
FROM hugomods/hugo:exts AS hugo
# Lychee link checker (Alpine variant for musl compatibility)
FROM lycheeverse/lychee:latest-alpine AS lychee

# Final Stage
FROM node:20-alpine

# Install System Dependencies
RUN apk add --no-cache bash git

# Copy Binaries from source stages
COPY --from=vale /bin/vale /usr/local/bin/
COPY --from=htmltest /bin/htmltest /usr/local/bin/
COPY --from=hugo /usr/bin/hugo /usr/local/bin/
COPY --from=lychee /usr/local/bin/lychee /usr/local/bin/

# Install Node Tools
COPY package.json /tmp/package.json
RUN npm install -g markdownlint-cli2

# Set working directory
WORKDIR /src
```

- [x] **Step 3: Commit**

```bash
git add Containerfile
git commit -m "feat: add lychee link checker to image"
```

---

### Task 2: Update CI verification step

**Files:**
- Modify: `.github/workflows/docker-publish.yml` (lines 104-107)

- [x] **Step 1: Add `lychee --version` to the verify command**

Change line 107 from:

```yaml
          bash -c "vale --version && markdownlint-cli2 --version && htmltest --version && hugo version"
```

to:

```yaml
          bash -c "vale --version && markdownlint-cli2 --version && htmltest --version && hugo version && lychee --version"
```

Full resulting step in context:

```yaml
      # Verify tool versions (compatibility with build.yml)
      - name: Verify Tool Versions
        run: |
          docker run --rm ${{ steps.image-tag.outputs.tag }} \
          bash -c "vale --version && markdownlint-cli2 --version && htmltest --version && hugo version && lychee --version"
```

The `&&` chain ensures:
- All five tools must report their version successfully
- Any non-zero exit (missing binary, runtime error) fails the step
- CI logs show the output of each tool up to the failure point

- [x] **Step 2: Commit**

```bash
git add .github/workflows/docker-publish.yml
git commit -m "ci: verify lychee version in image build workflow"
```

---

### Task 3: Rewrite README.md to OSS standards

**Files:**
- Modify: `README.md`

Replace the single-line description with a comprehensive OSS README: badges, tool inventory table, usage examples, CI explanation, and license.

- [x] **Step 1: Rewrite README** (subsequently expanded with interactive and CI usage examples per review feedback)

```markdown
# docs-as-code
...
```

- [x] **Step 2: Commit** (includes follow-up commit for expanded examples)

```bash
git add README.md
git commit -m "docs: rewrite README with tool inventory, usage, and CI documentation"
```

---

### Verification

After all tasks, run these commands from the repo root:

```bash
# Build the image locally
docker build -t docs-as-code:test -f Containerfile .

# Verify all five tools report versions
docker run --rm docs-as-code:test \
  sh -c "vale --version && markdownlint-cli2 --version && htmltest --version && hugo version && lychee --version"
# Expected: all five tools print version info, exit 0

# Verify lychee specifically
docker run --rm docs-as-code:test lychee --version
# Expected: lychee <version number>
```

### Definition of Done

- [ ] `Containerfile` builds successfully with Lychee included ⚠️ needs Docker (unavailable in this env)
- [ ] `docker run --rm <image> lychee --version` succeeds ⚠️ needs Docker
- [ ] All five tools (vale, markdownlint-cli2, htmltest, hugo, lychee) report versions from the image ⚠️ needs Docker
- [x] CI `docker-publish.yml` "Verify Tool Versions" step includes `lychee --version` ✅ verified by file inspection
- [x] README.md lists all tools, usage patterns, and CI badge ✅ verified by file inspection
- [ ] Image is pushed to `ghcr.io` with cosign signature ⚠️ needs Docker + deploy
