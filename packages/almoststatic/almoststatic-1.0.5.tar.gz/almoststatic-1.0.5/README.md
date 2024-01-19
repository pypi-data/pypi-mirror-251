# Almoststatic

**Almoststatic** is a static sites and web pages generator engine written in
[Python](https://python.org) which utilizes the
[Jinja2 template system](https://jinja.palletsprojects.com) to render pages.
It can be integrated with [Flask](https://flask.palletsprojects.com) apps to
serve static contents on dynamic sites or used standalone for static sites
development.

Pages are declared in [YAML](https://yaml.org/) files and rendered with Jinja2
template files. The HTML contents can be written in [Markdown](https://www.markdownguide.org/)
markup language or in plain HTML. The “content” folder contains all data needed
to do the job, and the “config.yaml” is used to share global parameters and to
set up configuration.

It is loosely inspired by [Hugo](https://gohugo.io/) static site generator, but
it differs in many ways.

# Why Almoststatic?

There are many static site generators such as [Next.js](https://nextjs.org/),
[Hugo](https://gohugo.io/) or [Jekyll](https://jekyllrb.com/), but you can
prefer Almostatic because:

- **It's perfect for pythonist.** It uses Jinja2 and Flask which are widely
  used by python community, so you don\'t need to learn other programming
  languages or template engines.
- **It's easy!** In fact the rules are very few and this mean few things to
  learn and great flexibility.
- **It's versatile.** It's engine has a powerful recursive system for embedding
  and including contents. This helps you to build rich contents and also to
  split them in small pieces called *"widgets"* easier to maintain.
- **It has blog capabilities.** Contain functions used to query metadata info
  useful to organize blog pages by categories and tags.
- **You can deliver static and dynamic contents at same time.** With Flask you
  can build your dynamic content and let Almoststatic to render the rest of
  page or the whole page, if it is full static.
- **Write static sites.** Static sites are composed only by text files and media
  contents. They are easy to deliver on the web, are secure by design, require
  less maintenance and resources and are faster. If you have no need for dynamic
  contents, with **Almoststatic** you can write all pages as static.
- **Not only for pythonists.** Basic knowledge of python is needed, but once
  your developer environment is ready, Almoststatic lets you to focus on
  writing yaml and karkdown\'s contents and to create your own widgets in html
  and Jinja2.

# Quick start

The simplest way to see if **Almoststatic** is what you're looking for, is to
try the sample provided with source code package and explore the source code.

The following tutorial is tested on Linux Ubuntu, but it's easy to port on
other platforms such other Linux distros, Windows or Mac.

You need git and python3, install them with:
```bash
$ sudo apt install git python3
```
Last linux's releases comes with python3 already installed and you have only to
check if your version is 3.6 or higher:

```bash
$ python3 --version
```

Now clone Almoststatic with git and enter into the directory:

```bash
$ git clone https://gitlab.com/claudio.driussi/almoststatic.git
$ cd almoststatic
```
It's common in python using virtualenv for development, to do so and to install
Almoststatic, write:

```bash
$ python3 -m venv myvenv
$ source myvenv/bin/activate
$ pip install almoststatic
$ pip install pyftpsync
```

Done! Now you can try the sample, cd into sample directory and run flaskapp.py:

```bash
$ cd sample/
$ python flaskapp.py
```

A local host Flask App instance server is executed and you can test
Almoststatic features.

Open your browser and copy and paste the following URL: `http://127.0.0.1:5000/`
or `localhost:5000`

You will be redirected to the static site showing some widgets and feature
of Almostatic, you can navigate to see some examples.

You can always exit from server pressing CTRL-C on your terminal.

To build static site run:

```bash
$ python write_static.py
$ ls -l ../_static_site/
```
As you can see, your pages are written as *.html files, but this is not enough
to get a really static site, to do this you have to tune writing parameters and
copy media files on appropriate location. When you are done the site can be
published as static site.

If you wish, you can run tests:

```bash
$ cd ../test
$ python as_test.py
```
This do some tests and write a simpler static site.

Now if you decide that **Almoststatic** is right for you, you can dig into
source code of sample and tests and read the documentation at:
[https://almoststatic.readthedocs.io](https://almoststatic.readthedocs.io)

# Status of project

Almoststatic is young but stable! It has all planned features and always gave me
the right results so it can be considered "production ready"

At the moment there are only a few themes, we are developing a "rolling theme"
with some beautiful widgets ready to use.
See [Flatstep theme](https://gitlab.com/almoststatic-themes/flatstep)
and follow the tutorial.

I'm not a designer so the result is of average quality. But I'm sure that good
designers can write great themes.


# Donate

If you appreciate Almoststatic, you can make a donation via PayPal

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?hosted_button_id=JYJ6EMFY7YWJQ)
