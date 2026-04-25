"""
Natural Language Query Parser
Rule-based interpreter (NO AI / LLM as required)
"""

import re

def parse_natural_query(query):
    if not query or not isinstance(query, str):
        return None

    query = query.lower().strip()
    filters = {}

    # Country mapping
    countries = {
        'nigeria': 'NG', 'ng': 'NG', 'naija': 'NG',
        'ghana': 'GH', 'gh': 'GH',
        'kenya': 'KE', 'ke': 'KE', 'kenyan': 'KE',
        'south africa': 'ZA', 'za': 'ZA',
        'angola': 'AO', 'ao': 'AO',
        'usa': 'US', 'us': 'US', 'united states': 'US', 'america': 'US',
        'uk': 'GB', 'united kingdom': 'GB', 'britain': 'GB',
        'canada': 'CA', 'ca': 'CA',
        'germany': 'DE', 'france': 'FR',
        'india': 'IN', 'brazil': 'BR',
        'australia': 'AU',
        'drc': 'CD', 'congo': 'CG',
        'uganda': 'UG', 'tanzania': 'TZ',
        'ethiopia': 'ET', 'egypt': 'EG',
        'morocco': 'MA', 'senegal': 'SN'
    }

    # Gender
    if re.search(r'\b(male|men|boys|man|guy|guys)\b', query):
        filters['gender'] = 'male'
    elif re.search(r'\b(female|women|girls|woman|lady|ladies)\b', query):
        filters['gender'] = 'female'

    # Age group
    if re.search(r'\b(child|children|kids)\b', query):
        filters['age_group'] = 'child'
    elif re.search(r'\b(teen|teenager|teenagers|adolescent)\b', query):
        filters['age_group'] = 'teenager'
    elif re.search(r'\b(adult|adults|grown)\b', query):
        filters['age_group'] = 'adult'
    elif re.search(r'\b(senior|elderly|old)\b', query):
        filters['age_group'] = 'senior'

    # "young" special rule (REQUIRED by spec)
    if 'young' in query:
        filters['min_age'] = 16
        filters['max_age'] = 24

    # Age conditions
    above = re.search(r'\b(?:above|over|older than|greater than)\s+(\d+)\b', query)
    if above:
        filters['min_age'] = int(above.group(1))

    below = re.search(r'\b(?:below|under|younger than|less than)\s+(\d+)\b', query)
    if below:
        filters['max_age'] = int(below.group(1))

    between = re.search(r'between\s+(\d+)\s+and\s+(\d+)', query)
    if between:
        filters['min_age'] = int(between.group(1))
        filters['max_age'] = int(between.group(2))

    # Country detection (FIXED: more flexible matching)
    for country_name, country_code in countries.items():
        if country_name in query:
            filters['country_id'] = country_code
            break

    return filters if filters else None