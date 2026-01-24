# Source Stages (Dependabot tracks these)
FROM jdkato/vale:latest as vale
FROM wjdp/htmltest:latest as htmltest
FROM hugomods/hugo:exts as hugo

# Final Stage
FROM node:20-alpine

# Install System Dependencies
RUN apk add --no-cache bash git

# Copy Binaries from source stages
COPY --from=vale /bin/vale /usr/local/bin/
COPY --from=htmltest /usr/local/bin/htmltest /usr/local/bin/
COPY --from=hugo /usr/bin/hugo /usr/local/bin/

# Install Node Tools
COPY package.json /tmp/package.json
RUN npm install -g markdownlint-cli2 markdown-spellcheck write-good

# Set working directory
WORKDIR /src
