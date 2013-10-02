=================
Django invitation
=================


This is a fairly simple user-invitation application for Django_,
designed to make allowing user signups as painless as possible
with quota restrictions: you need to be invited by someone else and
the number of invitations is limited by user.

.. _Django: http://www.djangoproject.com/


Overview
========

This application enables a common user-invitation workflow:

1. The inviting user fills out an invitation form, entering an email address.

2. An invitation key is created, and an invitation link is sent to
   the invited user's email address.

3. The invited user clicks the invitation link, and is then
   able to register and begin contributing to your site.

Various methods of extending and customizing the invitation process
are also provided.


Installation
============

In order to use django-invitation, you will need to have a
functioning installation of Django 1.0 or newer; due to changes needed
to stabilize Django's APIs prior to the 1.0 release,
django-invitation will not work with older releases of Django.

**The django-registration application is required in order to use 
django-invitation.**

Installing from a Mercurial checkout
------------------------------------

If you have `Mercurial`_ installed on your computer, you can also
obtain a complete copy of django-invitation by typing::

    hg clone http://code.welldev.org/django-invitation/

Inside the resulting "django-invitation" directory will be a
directory named "invitation", which is the actual Python module for
this application; you can symlink it from somewhere on your Python
path. Using a symlink offers easy upgrades: simply running ``hg pull -u``
inside the django-invitation directory will fetch updates from the
main repository and apply them to your local copy.

.. _Mercurial: http://www.selenic.com/mercurial/wiki/


Basic use
=========

To use the invitation system with all its default settings, you'll
need to do the following:

1. Add ``invitation`` to the ``INSTALLED_APPS`` setting of your
   Django project.

2. Set your django-invitation settings in your settings file.

  * ``INVITE_MODE`` - Boolean.  Whether users are required to be
    invited before registering.
  * ``ACCOUNT_INVITATION_DAYS`` - Integer.  The number of days 
    invitation keys will remain valid after an invitation is sent.
  * ``INVITATIONS_PER_USER`` - Integer.  The number of invitations
    that are initially allotted to each newly registered user.

3. Add this line to your site's root URLConf **before registration urls**::
   
       (r'^accounts/', include('invitation.urls')),

4. Run `python manage.py syncdb` to update your database with the
   django-invitation models.

5. Override the base template or individual invitation templates
   (see the section on templates below for details).

6. Link people to ``/accounts/invite/`` so they can start inviting.


Templates used by django-invitation
===================================

The views included in django-invitation make use of several templates,
which are provided by the application in a default version. To make use of these
templates you are required to have

    'django.template.loaders.app_directories.load_template_source'

in your TEMPLATE_LOADERS settings.

To adapt the default templates to the look and structure of your site, it may be
sufficient to override the "invitation/base.html" template in your project's template
directory. This template should be set up to inherit your site's base template like so::

{% extends "my_base.html" %}
{% block my_content_block %}
{% block invitation_content %}{% endblock %}
{% endblock %}

For further customization you can also override individual templates in your
site's templates directory.

* ``invitation/invitation_form.html`` displays the invitation
  form for users to invite contacts.

* ``invitation/invitation_complete.html`` is displayed after the
  invitation email has been sent, to tell the user his contact has been 
  emailed.

* ``invitation/invitation_email_subject.txt`` is used for the
  subject of the invitation email.

* ``invitation/invitation_email.txt`` is used for the body of the
  invitation email.

* ``invitation/invited.html`` is displayed when a user attempts to
  register his/her account.

* ``invitation/wrong_invitation_key.html`` is displayed when a user
  attempts to register his/her account with a wrong/expired key.

Additionally, the URLConf provided with django-invitation includes
URL patterns for useful views in Django's built-in authentication
application -- this means that a single ``include`` in your root
URLConf can wire up invitation process.


How it works
============

Using the recommended default configuration, the URL
``/accounts/invite/`` will map to the view
``invitation.views.invite``, which displays an invitation form
(an instance of ``invitation.forms.InvitationKeyForm``); this form
asks for an email address. It then does three things:

1. Validates the form to be sure it has a valid email address.

2. Creates an instance of ``invitation.models.InvitationKey``,
   stores an activation key (a SHA1 hash generated from the 
   inviting user's username plus a timestamp and a 
   randomly-generated "salt").

3. Sends an email to the invitee (at the supplied address)
   containing a link which can be clicked to register a new account.

For details on customizing this process, including use of alternate
invitation form classes, read the code (or django-registration documentation).

After the activation email has been sent,
``invitation.views.invite`` issues a redirect to the URL
``/accounts/invite/complete/``. By default, this is mapped to the
``direct_to_template`` generic view, and displays the template
``invitation/invitation_complete.html``; this is intended to show
a short message telling the user his/her contact has been emailed.

The invitation link will map to the view
``invitation.views.invited``, which will attempt to verify the activation key.
If the activation key has expired (this is controlled by the setting 
``ACCOUNT_INVITATION_DAYS``, as described above), the register page will not 
be reachable (see the section on maintenance below for instructions on 
cleaning out expired keys which have not been used).

Alternatively, you can directly redirect the user to the registration view
with the ``registration_key`` argument as a GET (or POST) parameter in order 
to verify if this user is allowed to register.

The ``INVITATIONS_PER_USER`` setting (integer) lets you decide the initial 
number of invitations left per user. Each new email sent consumes one 
invitation.  (Administrators can use the Django Admin interface to modify
the number of invitations a user has.)


Maintenance
===========

Inevitably, a site which uses a two-step process for user invitation --
invitation followed by accepting -- will accumulate a certain
number of keys which were created but never used. These
keys clutter up the database, so it's desirable to clean them out
periodically. For this purpose, a `Django command`_,
``cleanupinvitation``, is provided, which is
suitable for use as a regular cron job.

.. _Django command: http://docs.djangoproject.com/en/dev/ref/django-admin/#available-subcommands


Dependencies
============

This application is built on top of django-registration.  You need to install
this application (currently 0.7) and to resolve dependencies of this 
application.


If you spot a bug
=================

Head over to this application's `project page on Bitbucket`_ and
check `the issues list`_ to see if it's already been reported. If not,
open a new issue and we'll do our best to respond quickly.

.. _project page on Bitbucket: http://code.welldev.org/django-invitation/
.. _the issues list: http://code.welldev.org/django-invitation/issues/
