Description
===========

This script generates color scheme configuration files for IDEs from vim color
schemes. The configuration of the vim color schemes is generated on the fly,
because some of the vim configuration files use functions to set the values.

Currently only IntelliJ IDEA is supported.

Usage
=====

    ./vim_color_exporter.py -icd ~/.IdeaIC11/config  badwolf

Dependencies
============

* [jinja2](http://jinja.pocoo.org/)
