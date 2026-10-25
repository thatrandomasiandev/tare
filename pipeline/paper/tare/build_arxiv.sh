#!/usr/bin/env bash
# Build the named arXiv PDF (system = TARE, real authors).
# Refuses to build while any PENDING macros remain.
# Restores OSDI figure labels (PARE) afterward.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "${HERE}"

if [[ ! -f macros_pending.tex ]]; then
  echo "build_arxiv: missing macros_pending.tex" >&2
  exit 1
fi
# Match real unfilled macros: \pending{...} on a non-comment line.
# Ignore the fill_macros header comment and the \newcommand{\pending} definition.
if grep -v '^%' macros_pending.tex | grep -q '\\pending{'; then
  echo "build_arxiv: refuses PENDING macros — run finalize.sh until macros are filled" >&2
  grep -v '^%' macros_pending.tex | grep '\\pending{' >&2 || true
  exit 1
fi
# Exclude comments and the \pending macro definition line itself (-F: literal).
if grep -v '^%' main.tex | grep -vF '\newcommand{\pending}' | grep -E '\\pending\{|\[PENDING' >/dev/null; then
  echo "build_arxiv: refuses PENDING markers in main.tex" >&2
  grep -v '^%' main.tex | grep -vF '\newcommand{\pending}' | grep -E '\\pending\{|\[PENDING' >&2 || true
  exit 1
fi

echo "=== arXiv figures (TARE labels) ==="
export TARE_SYS_NAME=TARE
python3 figures/make_figures.py
python3 figures/make_churn_pairs.py

echo "=== arXiv PDF ==="
# Wrapper so latexmk sees a stable job name; main.tex branches on \arxivbuild.
cat > arxiv_wrap.tex <<'EOF'
\def\arxivbuild{1}
\input{main.tex}
EOF
latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=arxiv arxiv_wrap.tex
rm -f arxiv_wrap.tex

echo "=== restore OSDI figures (PARE labels) ==="
export TARE_SYS_NAME=PARE
python3 figures/make_figures.py
python3 figures/make_churn_pairs.py

echo "Wrote ${HERE}/arxiv.pdf"
