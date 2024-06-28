# We convert all the vector source images into svg
# .vsdx -> .contrib.svg
# .pdf  -> .svg
DISTDIR=dist
SRCDIR=src

VSDXs=$(shell find src/* -type f -name '*.vsdx')
SVGS=$(patsubst src/%.vsdx,$(DISTDIR)/%.svg,$(VSDXs))

all: $(SVGS)

$(DISTDIR)/%.svg: $(SRCDIR)/%.vsdx | $(DISTDIR)
	mkdir -p $(dir $@)
	./visio2svg.sh $< $@

$(DISTDIR):
	mkdir $@

COMMIT!=git rev-parse HEAD

.PHONY: all
