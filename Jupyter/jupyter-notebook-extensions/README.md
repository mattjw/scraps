# Configure Jupyter notebook with extensions

Setup...

```bash
pipenv --three
pipenv install jupyter

pipenv install --editable jupyter_contrib_nbextensions
pipenv run jupyter contrib nbextension install --sys-prefix
    # --sys-prefix will install to the pipenv's virtualenv
```

You can install a GUI to select extensions...

```bash
pipenv install jupyter_nbextensions_configurator
pipenv run jupyter nbextensions_configurator enable --sys-prefix
# visit http://localhost:8888/nbextensions
```

Enable chosen extensions...

```bash
pipenv run jupyter nbextension enable ruler/main
pipenv run jupyter nbextension enable help_panel/help_panel
pipenv run jupyter nbextension enable notify/notify
pipenv run jupyter nbextension enable execute_time/ExecuteTime
pipenv run jupyter nbextension enable spellchecker/main
pipenv run jupyter nbextension enable toggle_all_line_numbers/main
pipenv run jupyter nbextension enable freeze/main
pipenv run jupyter nbextension enable code_font_size/code_font_size
pipenv run jupyter nbextension enable varInspector/main
```

See [here](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions.html) for more extensions.

Start notebook...

```bash
pipenv run jupyter notebook
```
