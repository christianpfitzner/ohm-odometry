# Build the handout: make (latexmk -pdf). One TikZ figure, no external graphics.
LATEXMK := latexmk

odometry.pdf: odometry.tex figures/diffdrive.tikz figures/nodegraph.tikz figures/mecanum.tikz
	$(LATEXMK) -pdf -interaction=nonstopmode odometry.tex

.PHONY: log clean

log:
	@grep -nE "^!|Overfull \\\\hbox \(([1-9][0-9]|[0-9]+[0-9])pt|Undefined control|LaTeX Warning: (Reference|Citation)" odometry.log || echo "log clean"

clean:
	-$(LATEXMK) -c odometry.tex >/dev/null 2>&1
