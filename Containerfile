FROM klakegg/hugo:ext-alpine-ci

# + link checker e.g. https://github.com/wjdp/htmltest
RUN wget https://htmltest.wjdp.uk -O - | bash -s -- -b /usr/local/bin

# + markdown linter (https://github.com/DavidAnson/markdownlint-cli2)
RUN npm install markdownlint-cli2 --global

# + spell checker (https://github.com/lukeapage/node-markdown-spellcheck)
RUN npm install markdown-spellcheck --global

# to be installed and configured
# + hemingway scorer (https://github.com/btford/write-good)
RUN npm install write-good --global

# + writing style linter (https://github.com/errata-ai/vale)
ENV VALE_VERSION=3.8.0
RUN wget https://github.com/errata-ai/vale/releases/download/v${VALE_VERSION}/vale_${VALE_VERSION}_Linux_64-bit.tar.gz \
    && tar -xzf vale_${VALE_VERSION}_Linux_64-bit.tar.gz vale -C /usr/local/bin \
    && rm vale_${VALE_VERSION}_Linux_64-bit.tar.gz
