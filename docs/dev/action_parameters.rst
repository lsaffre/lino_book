.. doctest docs/dev/action_parameters.rst

=================================
Introduction to action parameters
=================================

Any action in Lino can have an optional dialog window that pops up before the
action is actually executed. The fields of this dialog window are called
:term:`action parameters <action parameter>`.


.. contents::
    :depth: 2
    :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.noi1e.settings.demo')
>>> from lino.api.doctest import *



.. glossary::

  action parameter

    The run-time parameters of an action that can be given by the :term:`end
    user` in a dialog window that is shown before executing the action.

    Action parameters are stored in the :attr:`parameters
    <lino.core.actions.Action.parameters>` attribute of their :class:`Action
    <lino.core.actions.Action>`).

  dialog action

    An action that opens a dialog window where the :term:`end user`  can specify
    :term:`action parameters <action parameter>`  before actually running the
    action.

    An :class:`lino.core.actions.Action` is a :term:`dialog action` if it has
    :attr:`lino.core.actions.Action.parameters` defined and
    :attr:`lino.core.actions.Action.no_params_window` has not been enabled.


The merge action is an example of an action with parameters.  When you
click the merge button on a ticket, Lino reacts by popping up a dialog
window asking for parameters.  The action request is submitted only
when you confirm this window.

.. image:: /specs/noi/tickets.Ticket.merge.png
   :width: 80%


>>> ba = rt.models.tickets.AllTickets.get_action_by_name('merge_row')
>>> action = ba.action
>>> p = action.parameters
>>> p['merge_to']
<django.db.models.fields.related.ForeignKey: merge_to>

>>> p['reason']
<django.db.models.fields.CharField: reason>


How to get the layout elements of an action parameter window.

You need the front end.

>>> ui = settings.SITE.kernel.default_ui
>>> ui
lino.modlib.extjs (media_name=ext-3.3.1)

This will give you a layout handle:

>>> lh = action.params_layout.get_layout_handle(ui)
>>> lh #doctest: +ELLIPSIS
<lino.core.layouts.LayoutHandle object at ...>

>>> lh.main
<ActionParamsPanel main in lino.core.layouts.ActionParamsLayout on <lino.core.merge.MergeAction merge_row ('Merge')>>

>>> lh['main'] is lh.main
True

>>> lh['merge_to']
<ForeignKeyElement merge_to in lino.core.layouts.ActionParamsLayout on <lino.core.merge.MergeAction merge_row ('Merge')>>

>>> lh['reason']
<CharFieldElement reason in lino.core.layouts.ActionParamsLayout on <lino.core.merge.MergeAction merge_row ('Merge')>>

You can **walk** over the elements of a panel:

>>> ses = rt.login('robin')
>>> with ses.get_user().user_type.context():
...     for e in lh.walk():
...        print("{} {}".format(e.name, e.__class__.__name__))
merge_to ForeignKeyElement
merge_to_ct Wrapper
tickets_Link BooleanFieldElement
tickets_Link_ct Wrapper
reason CharFieldElement
reason_ct Wrapper
main ActionParamsPanel



Calling a parameter action programmatically
===========================================

In doctests we sometimes want to call an action programmatically
without doing a web request.

In that case we must specify the `action_param_values`.  It must be a
dict.  Lino checks whether the keys of the dict corresponds to the
names of the parameter fields:

>>> pv = dict(foo=1, reason="test")
>>> ar = ba.request_from(ses, action_param_values=pv)
Traceback (most recent call last):
...
Exception: Invalid key 'foo' in action_param_values of tickets.AllTickets request (possible keys are ['merge_to', 'reason', 'tickets_Link'])

Lino does not validate the values when calling it programmatically.
For example `merge_to` should be a Ticket instance.
But here we specify an integer value instead, and Lino does not complain:

>>> pv = dict(merge_to=1, reason="test")
>>> ar = ba.request_from(ses, action_param_values=pv)
>>> ar.action_param_values
{'merge_to': 1, 'reason': 'test', 'tickets_Link': False}

Basically the following should work as well. (But nobody ever asked us
to make it possible).

>>> o1 = rt.models.tickets.Ticket.objects.get(pk=1)
>>> o2 = rt.models.tickets.Ticket.objects.get(pk=2)
>>> pv = dict(merge_to=o2, reason="test")
>>> ar = ba.request_from(ses, action_param_values=pv)
>>> ar.set_confirm_answer(False)
>>> o1.merge_row.run_from_ui(ar)
>>> 'xcallback' in ar.response
True
>>> msg = ar.response['message']
>>> print(tostring(msg))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
<div class="htmlText"><p>Are you sure you want to merge #1 (⚹ Föö fails
to bar when baz) into #2 (☎ Bar is not always baz)?</p><ul><li>1 Dependencies
<b>will be deleted.</b></li><li>1 Sessions, 7 Comments <b>will get
reassigned.</b></li><li>#1 (⚹ Föö fails to bar when baz) will be
deleted</li></ul></div>



Here is a list of all :term:`dialog actions <dialog action>` in :ref:`noi`:

>>> show_dialog_actions()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- cal.EventTypes.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- cal.GuestRoles.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- contacts.Companies.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **List memberships** (lists_Member), **Reason** (reason)
- contacts.Partners.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **List memberships** (lists_Member), **Reason** (reason)
- contacts.Persons.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **List memberships** (lists_Member), **Reason** (reason)
- groups.Groups.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Group memberships** (groups_Membership), **Reason** (reason)
- ledger.AccountingPeriods.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- ledger.Accounts.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- ledger.FiscalYears.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- ledger.Journals.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Match rules** (ledger_MatchRule), **Reason** (reason)
- ledger.PaymentTerms.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- lists.Lists.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **List memberships** (lists_Member), **Reason** (reason)
- tickets.Sites.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Site summaries** (working_SiteSummary), **Reason** (reason)
- tickets.Tickets.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Dependencies** (tickets_Link), **Reason** (reason)
- tickets.Tickets.spawn_ticket : Spawn child ticket
  (main) [visible for all]: **Dependency type** (link_type), **Summary** (ticket_summary)
- uploads.Volumes.merge_row : Merge
  (main) [visible for all]: **into...** (merge_to), **Reason** (reason)
- users.AllUsers.change_password : Change password
  (main) [visible for all]: **Current password** (current), **New password** (new1), **New password again** (new2)
- users.AllUsers.merge_row : Merge
  (main) [visible for all]:
  - **into...** (merge_to)
  - **Also reassign volatile related objects** (keep_volatiles):
    - (keep_volatiles_1): **Reactions** (comments_Reaction), **Group memberships** (groups_Membership)
    - (keep_volatiles_2): **User summaries** (working_UserSummary), **List memberships** (lists_Member)
- **Reason** (reason)
- users.AllUsers.send_welcome_email : Welcome mail
  (main) [visible for all]: **e-mail address** (email), **Subject** (subject)
- users.AllUsers.verify : Verify
  (main) [visible for all]: **e-mail address** (email), **Verification code** (verification_code)
- users.NewUsers.send_welcome_email : Welcome mail
  (main) [visible for all]: **e-mail address** (email), **Subject** (subject)
- users.UsersOverview.sign_in : Sign in
  (main) [visible for all]: **Username** (username), **Password** (password)
<BLANKLINE>
