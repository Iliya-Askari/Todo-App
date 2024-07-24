{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
https://project-askari.liara.run/accounts/api/v1/activations/confirm/{{token}}
{% endblock %}