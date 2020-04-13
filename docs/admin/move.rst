.. _hosting.move:

================================
Move a Lino site to a new server
================================

This document explains the following situation: you have a running
:term:`production site` on a server S1 and you want to move that site to a new
server S2.  You have installed S2 as described in :doc:`install`, so you have
the same application running on both servers, maybe different versions. S2 has
fictive demo data while S2 has confidential production data. You now want to
copy the data from S1 to S2.

Procedure
=========

- Create a snapshot with the special name :file:`snapshot2preview` on the old
  production site::

    $ go prod
    $ python manage.py dump2py snapshot2preview

- Create the file :xfile:`restore2preview.py`, which initially is just a copy of
  the  :xfile:`restore.py` created by the :xfile:`make_snapshot.sh`::

    $ cd snapshot2preview
    $ cp restore.py restore2preview.py

  You might need to edit this file e.g. if the new
  server has a newer version of the application.  And you don't want these edits
  to get overwritten in case you need to run the procedure again.

- Create a file :xfile:`initdb_from_prod.sh` in the project root of the future
  production server.  Adapt it as needed:

  - set ``OLD`` to `user@S1:/path/to/prod/on/old/server`
  - set ``NEW`` to `/path/to/prod/on/new/server`
  - remove ``PART1`` as this is supposed to be done on the old production server.

- Run the script.
  This will first copy all relevant data from S1 to S2 using :cmd:`rsync`,
  then delete all data in the database on the new site and
  replace it with the data that has been copied from the old production site.

- You might need to edit the file :xfile:`restore2preview.py`,  e.g.  if S2 has
  a newer version of the application. Of course you must edit this file *on the
  old server*, as it will be mirrored to the new server.

- Restart the Lino services on the new server and check whether it now has a
  copy of the production data. Take care to check whether uploaded files
  (:mod:`lino.modlib.uploads`) have been copied and are available on S1.

General workflow
================

When your manual tests pass, you inform the :term:`site operator` that it's now
their turn to test the new server.  There are chances that they will find more
problems.

After fixing the problems, you can simply run the procedure again (make a
:file:`snapshot2preview` on S1 and then run  :xfile:`initdb_from_prod.sh` on
S2). When no more problems are detected and the :term:`site operator` decided to
actually move, you will run it a last time to synchronize their latest data
before stopping the old production server.