#/usr/bin/env bash
tar --exclude={*__pycache__,*.pytest_cache,*.texbuild,*main.synctex.gz,*.agents,*.codex,*.venv} --exclude-vcs -acf Misha-Solodilov.zip floppy tex
