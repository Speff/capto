# Introduction
A tool for Discord server admins to auto-post messages tweeted out or favorited by specified users. An alternative for those who don't want a in-server bot to perform the same function and more flexible than IFTTT.

# Index

- [About](#beginner-about)
- [Usage](#sunny-usage)
  - [Installation](#electric_plug-installation)
  - [Commands](#package-commands)
- [Development](#wrench-development)
  - [Pre-Requisites](#notebook-pre-requisites)
  - [Developmen Environment](#nut_and_bolt-development-environment)
  - [File Structure](#file_folder-file-structure)
  - [Build](#hammer-build)  
  - [Deployment](#rocket-deployment)  
- [FAQ](#question-faq)
- [Resources](#page_facing_up-resources)
- [Gallery](#camera-gallery)
- [Credit/Acknowledgment](#star2-creditacknowledgment)

# About
This project was created out of a need for a front-end for the Discord auto-posting bot I created. The application is self-contained within docker - from the bot itself to the Postgres database used to keep track of its queries.--MORE TO BE ADDED--

# Usage
Write about how to use this project. --TBA--

###  Installation
- Steps on how to install this project, to use it. --TBA--



###  Commands
- Commands to start the project. --TBA--

#  Development

### Pre-Requisites
--TBA--

###  Development Environment
--TBA--
Write about setting up the working environment for your project.
- How to download the project...
- How to install dependencies...


###  File Structure

```
├── README.md
├── app
│   ├── Dockerfile
│   └── src
│       ├── __pycache__
│       │   ├── db_0x.cpython-37.pyc
│       │   ├── discord_auto.cpython-37.pyc
│       │   └── twit_0x.cpython-37.pyc
│       ├── db_0x.py
│       ├── discord_auto.py
│       ├── server.py
│       └── twit_0x.py
├── app.env
├── db
│   ├── Dockerfile
│   └── init.sql
├── docker-compose.yml
└── web
    ├── Dockerfile
    ├── nginx
    │   ├── fastcgi.conf
    │   ├── fastcgi_params
    │   ├── html
    │   ├── koi-utf
    │   ├── koi-win
    │   ├── mime.types
    │   ├── nginx.conf
    │   ├── scgi_params
    │   ├── sites-available
    │   │   └── default
    │   ├── uwsgi_params
    │   └── win-utf
    └── www
        ├── capto_twit_auth.js
        ├── capto_twit_cb.html
        ├── discord_auto.html
        ├── discord_auto.js
        ├── favicon.ico
        ├── index.html
        └── style
            ├── 0x-IA.css
            ├── dark-grey.css
            └── hack.css```
```

###  Build
--TBA--
Write the build Instruction here.

### Deployment
--TBA--
Write the deployment instruction here.

# FAQ
--TBA--
You can optionally add a FAQ section about the project.

#  Resources
--TBA--
Add important resources here

#  Gallery
--TBA--
Pictures of your project.

# Credit/Acknowledgment
--TBA--
Credit the authors here.

