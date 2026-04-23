"""
Natural Language Query Parser
Converts plain English into database filters
"""

import re

def parse_natural_query(query):
    """
    Parse natural language query and return filters
    """
    
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
        'germany': 'DE', 'de': 'DE',
        'france': 'FR', 'fr': 'FR',
        'india': 'IN', 'in': 'IN',
        'brazil': 'BR', 'br': 'BR',
        'australia': 'AU', 'au': 'AU',
        'drc': 'CD', 'cd': 'CD',
        'congo': 'CG', 'cg': 'CG',
        'uganda': 'UG', 'ug': 'UG',
        'tanzania': 'TZ', 'tz': 'TZ',
        'ethiopia': 'ET', 'et': 'ET',
        'egypt': 'EG', 'eg': 'EG',
        'morocco': 'MA', 'ma': 'MA',
        'senegal': 'SN', 'sn': 'SN'
    }
    
    # Gender detection
    if re.search(r'\b(male|men|boys|guy|guys|males|man)\b', query):
        filters['gender'] = 'male'
    elif re.search(r'\b(female|women|girls|lady|ladies|females|woman)\b', query):
        filters['gender'] = 'female'
    
    # Age group detection
    if re.search(r'\b(child|children|kids|minor)\b', query):
        filters['age_group'] = 'child'
    elif re.search(r'\b(teenager|teenagers|teens|adolescent|teen)\b', query):
        filters['age_group'] = 'teenager'
    elif re.search(r'\b(adult|adults|grown|mature)\b', query):
        filters['age_group'] = 'adult'
    elif re.search(r'\b(senior|seniors|elderly|old|aged)\b', query):
        filters['age_group'] = 'senior'
    
    # Handle "young" (ages 16-24)
    if 'young' in query:
        filters['min_age'] = 16
        filters['max_age'] = 24
    
    # Handle age operators - ABOVE / OVER
    above_match = re.search(r'\b(?:above|over|older than|greater than)\s+(\d+)\b', query)
    if above_match:
        filters['min_age'] = int(above_match.group(1))
    
    # Handle age operators - BELOW / UNDER
    below_match = re.search(r'\b(?:below|under|younger than|less than)\s+(\d+)\b', query)
    if below_match:
        filters['max_age'] = int(below_match.group(1))
    
    # Handle "between X and Y"
    between_match = re.search(r'between\s+(\d+)\s+and\s+(\d+)', query)
    if between_match:
        filters['min_age'] = int(between_match.group(1))
        filters['max_age'] = int(between_match.group(2))
    
    # Country detection - check for "from {country}" or "in {country}"
    for country_name, country_code in countries.items():
        if f'from {country_name}' in query or f'in {country_name}' in query:
            filters['country_id'] = country_code
            break
        elif country_name in query and len(country_name) > 2:
            if f' {country_name} ' in f' {query} ' or query.startswith(country_name):
                filters['country_id'] = country_code
                break
    
    # If no filters were found, return None
    if not filters:
        return None
    
    return filters