.. _devblog:

=============================
Start your own developer blog
=============================

This section explains what a **developer blog** is, why you need it,
why *we* need it, and how you do it.

Getting started
===============

The basic idea of a developer blog is that you **leave a trace** about
what you have been doing, and that this trace is accessible at least
to yourself.

In your developer blog you report about your daily work.  Day by day.
Using plain English language. It is your diary.

Of course it's not always easy to explain what you are doing.  The
daily work of a software developer includes things like modifying
source code, pushing changes to public repositories, writing comments
in forums, surfing around, reading books, discovering new
technologies, dreaming about a better world, reinventing wheels...

But keep in mind: when you develop or maintain a software used by
people who pay you for this job, documenting *what you change* and
*why you change it* is more important than actually fixing their
problem.  My first developer blog was a simple plain text file (one
per month) where I noted every code change for my own reference.  It
happens surprisingly often that I want to know why I did some change
one year ago.  And I was often amazed about how many things both my
customers and I were able to forget during one year.

.. glossary::

  developer blog

    A blog written by a developer using his editor of choice and the team's
    static html generator (i.e. Sphinx).

    It usually has at most one entry per day, each entry having potentially a
    series of headings

Qualities of a developer blog
=============================

A developer blog does not need to be cool, exciting, popular or easy
to follow.  It should rather be:

- **complete** (e.g. don't forget to mention any important code change
  you did)
- **concise** (e.g. avoid re-explaining things that are explained somewhere
  else)
- **understandable** (e.g. use references to point to these other
  places so that anybody with enough time and motivation has a chance
  to follow).

Note that these qualities are listed in order of difficulty.  Being
*complete* is rather easy and just a question of motivation.  Staying
*concise* without becoming incomplete takes some exercise.  And being
*understandable* requires some talent and much feedback from readers.  In
practice I just just try to be understandable at least to myself.

Note also that none of these qualities is required.  Even an
incomplete and unconcise developer blog is better than no blog at all.


Going public
============

When working as a professional on a free software project, it is
important that you share your developer blog in a public place where
others can access it.  Your blog becomes an integral part of the
software.  You share your know-how, your experience and your learning
(which includes successes, failures and stumblings).  You share it
also with future contributors who might want to explore why you have
been doing things the way you did them.

Before publishing your blog, make sure that you understand the usual rules:

- Don't disclose any passwords or private data.
- Respect other people's privacy.
- Reference your sources of information.
- Don't quote other author's words without naming them.

A public developer blog can be the easiest way to ask for help in complex cases
that need screenshots, links, sections etc.


Luc's blogging system
=====================

You probably know already one example of a public developer blog,
namely `Luc's developer blog <http://luc.lino-framework.org>`_.  The
remaining sections describe how you can use Luc's system for your own
blog.

You may of course use another blogging system (blogger.com,
wordpress.com etc,), especially if you have been blogging before.

Luc's developer blog is free, simple and extensible.
It answers well to certain requirements that we perceive as
important:

- A developer uses some editor for writing code, and wants to use that
  same editor for writing his blog.

- A developer usually works on more than one software projects at a
  time.

- A developer should not be locked just because there is no internet
  connection available for a few hours.

It is based on `Sphinx <http://sphinx-doc.org/>`_, which is the
established standard for Python projects. This has the advantage that
your blog has the same syntax as your docstrings.

Followers can subscribe to it using an RSS reader.


"Blog" versus "Documentation tree"
==================================

Luc's blogging system uses *daily* entries (maximum one blog entry per
day), and is part of some Sphinx documentation tree.

But don't mix up "a blog" with "a documentation tree".  You will
probably maintain only one *developer blog*, but you will maintain
many different *documentation trees*.  Not every documentation tree
contains a blog.

You probably will soon have other documentation trees than the one
which contains your blog. For example your first Lino application
might have a local project name "hello", and it might have two
documentation trees, one in English (`hello/docs`) and another in
Spanish (`hello/docs_es`). :cmd:`inv pd` would upload them to
`public_html/hello_docs` and `public_html/hello_docs_es` respectively.
See :attr:`env.docs_rsync_dest <atelier.fablib.env.docs_rsync_dest>`.


.. _dblog:

The `dblog` project template
============================

To help you get started with blogging in your own developer blog,
there is a project template at https://github.com/lsaffre/dblog


.. You may find inspiration from the Lino website for configuring your
   developer blog.

    - Interesting files are:
      :file:`/docs/conf.py`
      :file:`/docs/.templates/layout.html`
      :file:`/docs/.templates/links.html`
