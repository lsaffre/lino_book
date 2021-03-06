.. doctest docs/specs/noi/working.rst
.. include:: /shared/include/defs.rst
.. _specs.clocking:
.. _noi.specs.clocking:

==============================
`working` : Work time tracking
==============================


.. currentmodule:: lino_xl.lib.working

The :mod:`lino_xl.lib.working` adds functionality for managing work
time tracking.

.. contents::
  :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.noi1e.settings.demo')
>>> from lino.api.doctest import *

Note that the demo data is on fictive demo date **May 23, 2015**:

>>> dd.today()
datetime.date(2015, 5, 23)


Overview
========

.. glossary::

  work session

    A database record expressing the fact that a given user works (or has been
    working) on a given "ticket" for a given lapse of time.

    See `Work sessions`_ below.

  service report

    A document used in various discussions with a stakeholder.

    See `Service reports`_ below.

The :attr:`ticket_model <Plugin.ticket_model>` defines what a ticket actually
is.  It can be any model that implements :class:`Workable`.  In :ref:`noi` this
points to :class:`tickets.Ticket <lino_xl.lib.tickets.Ticket>`.


Work sessions
=============

Extreme case example of a :term:`work session`:

- I start to work on an existing ticket #1 at 9:23.  A customer phones
  at 10:17 with a question. I create #2 for this.  That call is interrupted
  several times by the customer himself.  During the first
  interruption another customer calls, with another problem (ticket
  #3) which we solve together within 5 minutes.  During the second
  interruption of #2 (which lasts 7 minutes) I make a coffee break.

  During the third interruption I continue to analyze the
  customer's problem.  When ticket #2 is solved, I decided that
  it's not worth to keep track of each interruption and that the
  overall session time for this ticket can be estimated to 0:40.

  ::

    Ticket start end    Pause  Duration
    #1      9:23 13:12  0:45
    #2     10:17 11:12  0:12       0:43
    #3     10:23 10:28             0:05


A :term:`site administrator` can see all sessions of the demo project:

>>> rt.show(working.Sessions, limit=15)
... #doctest: -REPORT_UDIFF
================================================= ========= ============ ============ ============ ========== ============ ========= =========== ===================
 Ticket                                            Worker    Start date   Start time   End Date     End Time   Break Time   Summary   Duration    Ticket #
------------------------------------------------- --------- ------------ ------------ ------------ ---------- ------------ --------- ----------- -------------------
 #1 (⚹ Föö fails to bar when baz)                  Luc       23/05/2015   09:00:00                                                                `#1 <Detail>`__
 #5 (☾ Cannot create Foo)                          Jean      23/05/2015   09:00:00                                                                `#5 <Detail>`__
 #69 (☾ Default account in invoices per partner)   Mathieu   23/05/2015   09:00:00                                                                `#69 <Detail>`__
 #4 (⚒ Foo and bar don't baz)                      Luc       22/05/2015   09:00:00     22/05/2015   11:18:00                          2:18        `#4 <Detail>`__
 #21 (☾ Irritating message when bar)               Jean      22/05/2015   09:00:00     22/05/2015   12:29:00                          3:29        `#21 <Detail>`__
 #85 (☾ How can I see where bar?)                  Mathieu   22/05/2015   09:00:00     22/05/2015   12:53:00                          3:53        `#85 <Detail>`__
 #11 (☉ Class-based Foos and Bars?)                Mathieu   20/05/2015   09:05:00     20/05/2015   09:17:00                          0:12        `#11 <Detail>`__
 #12 (⚒ Foo cannot bar)                            Luc       20/05/2015   09:00:00     20/05/2015   10:30:00                          1:30        `#12 <Detail>`__
 #37 (☾ Cannot delete foo)                         Jean      20/05/2015   09:00:00     20/05/2015   09:37:00                          0:37        `#37 <Detail>`__
 #101 (☾ Why is foo so bar)                        Mathieu   20/05/2015   09:00:00     20/05/2015   09:05:00                          0:05        `#101 <Detail>`__
 #14 (☐ Bar cannot baz)                            Luc       19/05/2015   09:00:00     19/05/2015   09:10:00                          0:10        `#14 <Detail>`__
 #53 (☾ Foo never bars)                            Jean      19/05/2015   09:00:00     19/05/2015   10:02:00                          1:02        `#53 <Detail>`__
 #27 (☉ No more foo when bar is gone)              Mathieu   19/05/2015   09:00:00     19/05/2015   11:18:00                          2:18        `#27 <Detail>`__
 **Total (13 rows)**                                                                                                                  **15:34**
================================================= ========= ============ ============ ============ ========== ============ ========= =========== ===================
<BLANKLINE>


Some sessions are on private tickets:

>>> from django.db.models import Q
>>> rt.show(working.Sessions, column_names="ticket user duration", filter=Q(ticket__private=True))
... #doctest: -REPORT_UDIFF
============================== ======== ==========
 Ticket                         Worker   Duration
------------------------------ -------- ----------
 #4 (⚒ Foo and bar don't baz)   Luc      2:18
 #12 (⚒ Foo cannot bar)         Luc      1:30
 **Total (2 rows)**                      **3:48**
============================== ======== ==========
<BLANKLINE>


Worked hours
============

The :class:`WorkedHours` table is useful to manually edit your working times or
to see on which tickets you have been working recently. It is shown in your
dashboard (unless you configured your dashboard to hide it).

.. class:: WorkedHours

  Shows a summary of your :term:`work sessions <work session>` of the last seven
  days, one row per day.

>>> rt.login('jean').show(working.WorkedHours)
... #doctest: -REPORT_UDIFF
============================= ================== ========= ======= ========== ==========
 Description                   Worked tickets     Regular   Extra   Free       Total
----------------------------- ------------------ --------- ------- ---------- ----------
 `Sat 23/05/2015 <Detail>`__   `#5 <Detail>`__                      0:01       0:01
 `Fri 22/05/2015 <Detail>`__   `#21 <Detail>`__                     3:29       3:29
 `Thu 21/05/2015 <Detail>`__                                                   0:00
 `Wed 20/05/2015 <Detail>`__   `#37 <Detail>`__                     0:37       0:37
 `Tue 19/05/2015 <Detail>`__   `#53 <Detail>`__                     1:02       1:02
 `Mon 18/05/2015 <Detail>`__                                                   0:00
 `Sun 17/05/2015 <Detail>`__                                                   0:00
 **Total (7 rows)**                                                 **5:09**   **5:09**
============================= ================== ========= ======= ========== ==========
<BLANKLINE>

To manually edit your :term:`work sessions <work session>`, click on a date in
the `Description` column to open :class:`MySessionsByDate`.

In the :guilabel:`Worked tickets` column you see a list of the tickets on which
you worked that day. This is a convenient way to continue some work you started
some days ago.

..
    Find the users who worked on more than one site:
    >>> for u in users.User.objects.all():
    ...     qs = tickets.Site.objects.filter(tickets_by_site__sessions_by_ticket__user=u).distinct()
    ...     if qs.count() > 1:
    ...         print("{} {} {}".format(str(u.username), "worked on", [o for o in qs]))
    mathieu worked on [Site #3 ('pypi'), Site #6 ('aab')]

    Render this table to HTML in order to reproduce :ticket:`523`:

    >>> url = "/api/working/WorkedHours?"
    >>> #url += "_dc=1583295523012&cw=398&cw=398&cw=76&cw=76&cw=76&cw=76&cw=281&cw=76&ch=&ch=&ch=&ch=&ch=&ch=&ch=true&ch=true&ci=detail_link&ci=worked_tickets&ci=vc0&ci=vc1&ci=vc2&ci=vc3&ci=description&ci=day_number&name=0&pv=188&pv=&pv=&pv=&lv=1583294270.8095002&an=show_as_html&sr="
    >>> url += "an=show_as_html"
    >>> test_client.force_login(rt.login('jean').user)
    >>> res = test_client.get(url, REMOTE_USER="jean")
    >>> json.loads(res.content.decode()) == {'open_url': '/bs3/working/WorkedHours?limit=15', 'success': True}
    True

    The html version of this table table has only 5 rows (4 data rows and
    the total row) because valueless rows are not included by default:

    >>> ar = rt.login('jean')
    >>> u = ar.get_user()
    >>> ar = working.WorkedHours.request(user=u)
    >>> ar = ar.spawn(working.WorkedHours)
    >>> lst = list(ar)
    >>> len(lst)
    7
    >>> e = ar.table2xhtml()
    >>> len(e.findall('./tbody/tr'))
    8




Service reports
===============

A :term:`service report` is a document used in various discussions with
a stakeholder.
It reports about the working time invested during a given date range.
This report can serve as a base for writing invoices.

It can be addressed to a recipient (a user) and in that case will
consider only the tickets for which this user has specified interest.

Database model: :class:`ServiceReport`.

A service report currently contains three tables:

- a list of work sessions
- a list of the tickets mentioned in the work sessions and their
  invested time
- a list of sites mentioned in the work sessions and their invested
  time


.. class:: ServiceReport

    Django model representing a :term:`service report`.

    Database fields:

    .. attribute:: user

        This can be empty and will then show the working time of all
        users.

    .. attribute:: start_date
    .. attribute:: end_date


    .. attribute:: interesting_for

        Show only tickets on sites assigned to this partner.

    .. attribute:: ticket_state

        Show only tickets having this state.

    .. attribute:: printed

        See :attr:`lino_xl.lib.exerpts.Certifiable.printed`



>>> obj = working.ServiceReport.objects.get(pk=1)
>>> obj.printed_by.build_method
<printing.BuildMethods.weasy2html:weasy2html>


>>> obj.interesting_for
Partner #100 ('Rumma & Ko OÜ')

>>> rt.show(working.SessionsByReport, obj)
... #doctest: -REPORT_UDIFF +SKIP
==================== ============ ========== ============ ================== ========== ======= ======
 Start date           Start time   End Time   Break Time   Description        Regular    Extra   Free
-------------------- ------------ ---------- ------------ ------------------ ---------- ------- ------
 23/05/2015           09:00:00                             `#1 <Detail>`__    0:01
 22/05/2015           09:00:00     12:29:00                `#11 <Detail>`__   3:29
 20/05/2015           09:00:00     09:05:00                `#6 <Detail>`__    0:05
 **Total (3 rows)**                                                           **3:35**
==================== ============ ========== ============ ================== ========== ======= ======
<BLANKLINE>

Note that sessions on #1 have actually no duration because they are active. But
in the report they are shown with one minute. That's a bug (TODO: fix it).  It's
not an urgent bug because that's not any normal situation (you are not going to
write reports for a date range when there are still active session).

>>> rt.login("robin").show(working.TicketsByReport, obj)
... #doctest: -REPORT_NDIFF +NORMALIZE_WHITESPACE
==== =============================================== =============== ======== ========= ========== ======= ======
 ID   Ticket                                          End user        Site     State     Regular    Extra   Free
---- ----------------------------------------------- --------------- -------- --------- ---------- ------- ------
 1    `#1 (⚹ Föö fails to bar when baz) <Detail>`__   Andreas Arens   welket   New       0:01
 4    `#4 (⚒ Foo and bar don't baz) <Detail>`__       Andreas Arens   welket   Working   2:18
 12   `#12 (⚒ Foo cannot bar) <Detail>`__             Andreas Arens   welket   Working   1:30
 14   `#14 (☐ Bar cannot baz) <Detail>`__             Andreas Arens   welket   Ready     0:10
                                                                                         **3:59**
==== =============================================== =============== ======== ========= ========== ======= ======
<BLANKLINE>


Reporting type
==============

The :attr:`reporting_type` of a site indicates how the client is going
to pay for the work done.

The default implementation offers three choices "Worker", "Employer"
and "Customer". "Worker" is for volunteer work and "private fun" where
the worker does not get paid by anybody.  "Employer" is when working
time should be reported to the employer (but no customer is going to
pay for it directly).  "Customer" is when working time should be
reported to the customer.

>>> rt.show(working.ReportingTypes)
======= ========= =========
 value   name      text
------- --------- ---------
 10      regular   Regular
 20      extra     Extra
 30      free      Free
======= ========= =========
<BLANKLINE>


The local site admin can adapt above list to the site's needs. He also
defines a default reporting type:

>>> dd.plugins.working.default_reporting_type
<working.ReportingTypes.regular:10>


Database models
===============

.. class:: SessionType

    The type of a :class:`Session`.

.. class:: Session

    Django model representing a :term:`work session`.

    .. attribute:: start_date

        The date when you started to work.

    .. attribute:: start_time

        The time (in `hh:mm`) when you started working on this
        session.

        This is your local time according to the time zone specified
        in your preferences.

    .. attribute:: end_date

        Leave this field blank if it is the same date as start_date.

    .. attribute:: end_time

        The time (in `hh:mm`) when the worker stopped to work.

        An empty :attr:`end_time` means that the user is still busy
        with that session, the session is not yet closed.

        :meth:`end_session` sets this to the current time.

    .. attribute:: break_time

       The time (in `hh:mm`) to remove from the duration resulting
       from the difference between :attr:`start_time` and
       :attr:`end_time`.

    .. attribute:: faculty

       The faculty that has been used during this session. On a new
       session this defaults to the needed faculty currently specified
       on the ticket.

    .. attribute:: site_ref

    .. method:: end_session

        Tell Lino that you stop this session for now.
        This will simply set the :attr:`end_time` to the current time.

        Implemented by :class:`EndThisSession`.


Tables reference
================

.. class:: Sessions

.. class:: SessionsByTicket

    The "Sessions" panel in the detail of a ticket.

    .. attribute:: slave_summary

        This panel shows:

.. class:: MySessions

  Shows all my sessions.

  Use the |filter| button to filter them. You can export them to Excel.

.. class:: MySessionsByDate

  Shows my sessions of a given day.

  Use this to manually edit your :term:`work sessions <work session>`.

.. class:: SessionsByReport
.. class:: TicketsReport
.. class:: SitesByReport

     The list of tickets mentioned in a service report.

.. class:: WorkersByReport


Actions reference
=================

.. class:: StartTicketSession

    The action behind :class:`Workable.start_session`.


.. class:: EndSession

    Common base for :class:`EndThisSession` and :class:`EndTicketSession`.

.. class:: EndTicketSession

    The action behind :class:`Workable.end_session`.

.. class:: EndThisSession

    The action behind :class:`Session.end_session`.


The `Workable` model mixin
==========================

.. class:: Workable

    Base class for things that workers can work on.

    The model specified in :attr:`ticket_model <Plugin.ticket_model>`
    must be a subclass of this.
    For example, in :ref:`noi` tickets are workable.

    .. method:: is_workable_for

        Return True if the given user can start a *work session* on
        this object.

    .. method:: on_worked

        This is automatically called when a *work session* has been
        created or modified.

    .. method:: start_session

        Start a :term:`work session` on this ticket.

        See :class:`StartTicketSession`.


    .. method:: end_session

        Tell Lino that you stop working on this ticket for now.
        This will simply set the :attr:`Session.end_time` to the current time.

        Implemented by :class:`EndTicketSession`.



Actions reference
=================


.. class:: ShowMySessionsByDay

    Shows your :term:`work sessions <work session>` per day.


.. class:: TicketHasSessions

    Select only tickets for which there has been at least one session
    during the given period.

    This is added as item to :class:`lino_xl.lib.tickets.TicketEvents`.


.. class:: ProjectHasSessions

    Select only projects for which there has been at least one session
    during the given period.

    This is added as item to :class:`lino_xl.lib.tickets.ProjectEvents`.

.. class:: Worker

    A user who is candidate for working on a ticket.



Summaries
=========

.. class:: SiteSummary

    An automatically generated record with yearly summary data about a site.

.. class:: SummariesBySite

    Shows the summary records for a given site.

.. class:: UserSummary

    An automatically generated record with monthly summary data about a user.

.. class:: SummariesByUser

    Shows the summary records for a given user.

>>> rt.show(working.SiteSummaries, exclude=dict(regular_hours=""))
... #doctest: -REPORT_UDIFF
==== ====== ======= ======== ================ ================== ========= ======= ======
 ID   Year   Month   Site     Active tickets   Inactive tickets   Regular   Extra   Free
---- ------ ------- -------- ---------------- ------------------ --------- ------- ------
 3    2015           welket   0                0                  3:58
==== ====== ======= ======== ================ ================== ========= ======= ======
<BLANKLINE>


>>> rt.show(working.UserSummaries, exclude=dict(regular_hours=""))
... #doctest: -REPORT_UDIFF
==== ====== ======= ====== ========= ======= ======
 ID   Year   Month   User   Regular   Extra   Free
---- ------ ------- ------ --------- ------- ------
 65   2015   5       Luc    3:58
==== ====== ======= ====== ========= ======= ======
<BLANKLINE>


Don't read me
=============

>>> working.WorkedHours
lino_xl.lib.working.ui.WorkedHours

>>> print(working.WorkedHours.column_names)
detail_link worked_tickets  vc0:5 vc1:5 vc2:5 vc3:5 *

>>> working.WorkedHours.get_data_elem('detail_link')
lino.core.actors.Actor.detail_link
