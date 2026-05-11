#/usr/bin/env bash
tar --exclude={*__pycache__,*.pytest_cache,*.texbuild,*main.synctex.gz,*.agents,*.codex,*.venv,*todo} --exclude-vcs -acf MishaSolodilov.zip floppy tex
