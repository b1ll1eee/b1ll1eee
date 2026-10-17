# Profile README tooling. Everything under assets/ is generated; edit scripts/gen_assets.py instead.
CHROME ?= /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
PREVIEW ?= /tmp/profile-preview

.PHONY: assets preview check

assets:            ## regenerate assets/*.svg from scripts/gen_assets.py
	python3 scripts/gen_assets.py assets

check: assets      ## fail if committed assets differ from the generator output
	git diff --exit-code -- assets

preview: assets    ## render PNG previews with headless Chrome (animations advanced ~2s)
	mkdir -p $(PREVIEW)
	@for f in assets/*.svg; do \
	  h=$$(sed -nE 's/.*<svg[^>]* height="([0-9]+)".*/\1/p' $$f | head -1); \
	  "$(CHROME)" --headless=new --disable-gpu --hide-scrollbars --window-size=1200,$$h \
	    --virtual-time-budget=2000 --screenshot=$(PREVIEW)/$$(basename $$f .svg).png "file://$(PWD)/$$f" >/dev/null 2>&1; \
	done; ls $(PREVIEW)
