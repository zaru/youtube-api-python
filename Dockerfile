FROM python:3.8.6-buster

WORKDIR /app

RUN pip install requests pycodestyle autopep8 mypy \
    black pandas numpy matplotlib workflow colorama docopt bokeh pandas-bokeh
