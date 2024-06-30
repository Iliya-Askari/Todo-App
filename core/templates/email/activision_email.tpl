{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
<a href="http://127.0.0.1:8000/accounts/api/v1/activations/confirm/{{token}}">verified</a>
{% endblock %}
