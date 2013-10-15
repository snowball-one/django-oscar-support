======================================
Django Oscar Ticketing
======================================

**Disclaimer:** the project is still under heavy development. Things might
change rapidly, so please use with caution.

Django Oscar ticketing  is a ticketing and support system for Oscar. It
currently provides an interface to the customer to submit a support ticket. In
the dashboard, authorised users can see the tickets and respond or act on them.

Currently it only allow very basic functionality such as:

    #. Setting the status of a ticket.
    #. Reply to a customer with a message.
    #. Make a note on the ticket for internal use.
    #. Assign tickets to a staff user.

Features currently in the making:

    #. Relating a ticket to products, orders or order lines
    #. Allow file attachments
    #. Integrate with Oscar's alert system to notify the user of new replies.
    #. Add templating for messages in the dashboard for quicker replies.

Longer-term direction:

    * Add support for a rules engine to handle ticket-related tasks. This will
      include adding custom rules and actions that can be used globally or only
      by the support agent creating the rule/action.
    * Provide an extensive templating system that can be used within ticket
      messages to respond quicker.
    * Integrating an optional Service Level Agreement (SLA) workflow that
      defines time frames for ticket resolution of different types. The tickets
      are then prioritized or re-assigned according to actions related to these
      SLAs.


Screenshots
-----------

.. image:: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/customer_create_ticket.thumb.png
    :target: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/customer_create_ticket.png

.. image:: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/customer_ticket_list.thumb.png
    :target: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/customer_ticket_list.png

.. image:: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/dashboard_new_ticket.thumb.png
    :target: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/dashboard_new_ticket.png

.. image:: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/dashboard_update_ticket.thumb.png
    :target: https://github.com/tangentlabs/django-oscar-support/raw/master/docs/source/_static/screenshots/dashboard_update_ticket.png


Getting Started
---------------

Setup instructions are following soon. Stay tuned...


License
-------

*django-oscar-support* is released under the permissive `New BSD License`_

.. _`New BSD License`: https://github.com/tangentlabs/django-oscar-support/blob/master/LICENSE
