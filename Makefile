# __MODULE__ top-level targets. Run from the repo root.
#   brew install graphviz librsvg qpdf poppler kicad; pipx install wireviz

KICAD_CLI ?= /opt/homebrew/bin/kicad-cli
export KICAD_CLI

# Phase gates: make check (Phase 0), make check STRICT=1 (Phase 1)
check:
	python3 tools/check.py $(if $(STRICT),--strict,)

# Phase 2: regenerate schematic, ERC, netlist, PDF, BOM, netlist assertions
erc:
	sh hardware/run_erc.sh

# Phase 3: wiring diagrams docs/wiring/*.yml -> .svg/.png/.pdf
wiring:
	wireviz -f sp docs/wiring/system.yml
	wireviz -f sp docs/wiring/panel.yml
	rsvg-convert -f pdf -o docs/wiring/system.pdf docs/wiring/system.svg
	rsvg-convert -f pdf -o docs/wiring/panel.pdf docs/wiring/panel.svg

# Letter-size tiled PDFs for printing at the bench
wiring-print: wiring
	docs/wiring/tile.sh system
	docs/wiring/tile.sh panel

# Phase 4: 1:1 panel drill template
panel:
	python3 tools/panel.py
	rsvg-convert -f pdf -o docs/panel_drill.pdf docs/panel_drill.svg

all: check erc wiring panel

.PHONY: check erc wiring wiring-print panel all
