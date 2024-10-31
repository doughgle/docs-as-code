FROM ghcr.io/gohugoio/hugo:v0.136.5

USER root
# + link checker e.g. https://github.com/wjdp/htmltest
RUN wget https://htmltest.wjdp.uk -O - | ash -s -- -b /usr/local/bin

# + markdown linter (https://github.com/DavidAnson/markdownlint-cli2)
RUN npm install markdownlint-cli2 --global

# + spell checker (https://github.com/lukeapage/node-markdown-spellcheck)
RUN npm install markdown-spellcheck --global

# to be installed and configured
# + hemingway scorer (https://github.com/btford/write-good)
RUN npm install write-good --global

USER hugo:hugo