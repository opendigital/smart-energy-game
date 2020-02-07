# RCODI oTree Energy Game

oTree is a Python framework that lets you build:

- Multiplayer strategy games, like the prisoner's dilemma, public goods game, and auctions
- Controlled behavioral experiments in economics, psychology, and related fields
- Surveys and quizzes


## Requirements

note: oTree requires `Python 3.7.x` (not Python 3.6.x or Python 3.8.x)

Make sure you are running the correct version of Python before starting

```
pip install service_identity
```

## Installation

__Install oTree__

```
pip install -U otree
```

oTree also runs with heroku, to get started install the heroku cli utitily https://devcenter.heroku.com/articles/heroku-cli#download-and-install

See oTree documentation here: https://otree.readthedocs.io/en/latest/index.html


## Usage

__Commands__

- browser_bots
- create_session
- devserver
- django_test
- resetdb
- runprodserver
- runprodserver1of2
- runprodserver2of2
- shell
- startapp
- startproject
- test
- unzip
- zip
- zipserver


__Create new project__

*You can skip this step if you have cloned the github repo*

```
otree startproject <proj_name>
cd <proj_name>
```

__Start the Project__

```
otree devserver
```

## Live demo
http://demo.otree.org/

## Homepage
http://www.otree.org/

## Docs

http://otree.readthedocs.org

## Quick start

Rather than cloning this repo directly,
run these commands:

```
pip3 install -U otree
otree startproject oTree
cd oTree
otree devserver
```
