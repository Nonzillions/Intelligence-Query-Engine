"""
Natural Language Query Parser
Converts plain English into database filters
"""

import re

def parse_natural_query(query):
    """
    Parse natural language query and return filters
    
    Examples:
    "young males from nigeria" -> {"gender": "male", "min_age": 16, "max_age": 24, "country_id": "NG"}
    "females above 30" -> {"gender": "female", "min_age": 30}
    "adult males from kenya" -> {"gender": "male", "age_group": "adult", "country_id": "KE"}
    "Male and female teenagers above 17" -> {"age_group": "teenager", "min_age": 17}
    """
    
    if not query or not isinstance(query, str):
        return None
    
    query = query.lower().strip()
    filters = {}
    
    # Country mapping
    countries = {
        'nigeria': 'NG', 'ng': 'NG', 'naija': 'NG',
        'ghana': 'GH', 'gh': 'GH',
        'kenya': 'KE', 'ke': 'KE',
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
    gender_keywords = {
        'male': ['male', 'men', 'boys', 'guy', 'guys', 'males', 'man'],
        'female': ['female', 'women', 'girls', 'lady', 'ladies', 'females', 'woman']
    }
    
    for gender, keywords in gender_keywords.items():
        for keyword in keywords:
            if keyword in query:
                filters['gender'] = gender
                break
        if 'gender' in filters:
            break
    
    # Age group detection
    age_groups = {
        'child': ['child', 'children', 'kids', 'minor'],
        'teenager': ['teenager', 'teenagers', 'teens', 'adolescent', 'teen'],
        'adult': ['adult', 'adults', 'grown', 'mature'],
        'senior': ['senior', 'seniors', 'elderly', 'old', 'aged']
    }
    
    for group, keywords in age_groups.items():
        for keyword in keywords:
            if keyword in query:
                filters['age_group'] = group
                break
        if 'age_group' in filters:
            break
    
    # Handle "young" (ages 16-24)
    if 'young' in query:
        filters['min_age'] = 16
        filters['max_age'] = 24
    
    # Handle age operators - ABOVE / OVER
    above_patterns = [
        r'above\s*(\d+)',
        r'over\s*(\d+)',
        r'older than\s*(\d+)',
        r'>\s*(\d+)',
        r'greater than\s*(\d+)'
    ]
    
    for pattern in above_patterns:
        match = re.search(pattern, query)
        if match:
            filters['min_age'] = int(match.group(1))
            break
    
    # Handle age operators - BELOW / UNDER
    below_patterns = [
        r'below\s*(\d+)',
        r'under\s*(\d+)',
        r'younger than\s*(\d+)',
        r'<\s*(\d+)',
        r'less than\s*(\d+)'
    ]
    
    for pattern in below_patterns:
        match = re.search(pattern, query)
        if match:
            filters['max_age'] = int(match.group(1))
            break
    
    # Handle "between X and Y"
    between_match = re.search(r'between\s*(\d+)\s+and\s*(\d+)', query)
    if between_match:
        filters['min_age'] = int(between_match.group(1))
        filters['max_age'] = int(between_match.group(2))
    
    # Country detection - check for "from {country}" or "in {country}"
    for country_name, country_code in countries.items():
        if f'from {country_name}' in query or f'in {country_name}' in query:
            filters['country_id'] = country_code
            break
        # Also check if country name appears alone (but avoid false matches)
        elif country_name in query and len(country_name) > 2:
            # Make sure it's not part of another word
            if f' {country_name} ' in f' {query} ' or query.startswith(country_name):
                filters['country_id'] = country_code
                break
    
    # Handle "and" queries - remove gender for "male and female" (too broad)
    if 'male and female' in query or 'male & female' in query:
        if 'gender' in filters:
            del filters['gender']
    
    # If no filters were found, return None
    if not filters:
        return None
    
    return filters