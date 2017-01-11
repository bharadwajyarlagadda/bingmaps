from .env import env

address_params = env.from_string('''\
{% if admin_district %}adminDistrict={{ admin_district }}&{% endif %} \
{% if locality %}locality={{ locality }}&{% endif %} \
{% if postal_code %}postalCode={{ postal_code }}&{% endif %} \
{% if address_line %}addressLine={{ address_line }}&{% endif %} \
{% if country_region %}countryRegion={{ country_region }}&{% endif %} \
{% if include_neighborhood %} \
    includeNeighborhood={{ include_neighborhood }}& \
{% endif %} \
{% if include_ %}include={{ include_ }}&{% endif %} \
{% if max_results %}maxResults={{ max_results }}&{% endif %} \
{% if culture %}culture={{ culture }}&{% endif %} \
{% if output %}output={{ output }}{% endif %} \
''')

point_params = env.from_string('''\
{% if include_entity_types %} \
    includeEntityTypes={{ include_entity_types }}& \
{% endif %} \
{% if point %}point={{ point }}&{% endif %} \
{% if include_neighborhood %} \
    includeNeighborhood={{ include_neighborhood }}& \
{% endif %} \
{% if include_ %}include={{ include_ }}&{% endif %} \
{% if culture %}culture={{ culture }}&{% endif %} \
{% if output %}output={{ output }}{% endif %} \
''')

query_params = env.from_string('''\
{% if query %}query={{ query }}&{% endif %} \
{% if includeNeighborhood %} \
    includeNeighborhood={{ includeNeighborhood }}& \
{% endif %} \
{% if include_ %}include={{ include_ }}&{% endif %} \
{% if max_results %}maxResults={{ max_results }}&{% endif %} \
{% if culture %}culture={{ culture }}&{% endif %} \
{% if output %}output={{ output }}{% endif %} \
''')
