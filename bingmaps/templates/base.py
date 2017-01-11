from .env import env

base_url = env.from_string('''\
{{ http_protocol }}://dev.virtualearth.net/REST/ \
{% if version %}{{ version }}/{% endif %} \
{% if rest_api %}{{ rest_api }}/{% endif %} \
{% if resource_path %}{{ resource_path }}?{% endif %} \
{% if query_params %}{{ query_params }}&{% endif %} \
key={% if key %}{{ key }}{% endif %}
''')
