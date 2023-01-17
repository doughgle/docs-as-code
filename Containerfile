FROM klakegg/hugo:ext-pandoc-ci

# + link checker e.g. https://github.com/wjdp/htmltest
RUN wget https://htmltest.wjdp.uk -O - | bash -s -- -b /usr/local/bin

# to be installed and configured
# + markdown linter
# + spell checker
# + hemingway scorer