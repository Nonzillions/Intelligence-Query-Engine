"""
Natural Language Query Parser
Converts plain English into database filters
"""

def parse_natural_query(query):
    """
    Parse a natural language query and return filters
    
    Examples:
    "young males from nigeria" -> {"gender": "male", "min_age": 16, "max_age": 24, "country_id": "NG"}
    "females above 30" -> {"gender": "female", "min_age": 30}
    "people from angola" -> {"country_id": "AO"}
    """
    
    if not query or not isinstance(query, str):
        return None
    
    query = query.lower().strip()
    filters = {}
    
    # Country mapping (common country names to ISO codes)
    countries = {
        'nigeria': 'NG', 'ng': 'NG',
        'ghana': 'GH', 'gh': 'GH',
        'kenya': 'KE', 'ke': 'KE',
        'south africa': 'ZA', 'za': 'ZA',
        'angola': 'AO', 'ao': 'AO',
        'usa': 'US', 'us': 'US',
        'united states': 'US', 'america': 'US',
        'uk': 'GB', 'united kingdom': 'GB',
        'canada': 'CA', 'ca': 'CA',
        'germany': 'DE', 'de': 'DE',
        'france': 'FR', 'fr': 'FR',
        'india': 'IN', 'in': 'IN',
        'brazil': 'BR', 'br': 'BR',
        'australia': 'AU', 'au': 'AU',
        'drc': 'CD', 'cd': 'CD', 'democratic republic of congo': 'CD',
        'congo': 'CG', 'cg': 'CG',
        'uganda': 'UG', 'ug': 'UG',
        'tanzania': 'TZ', 'tz': 'TZ',
        'ethiopia': 'ET', 'et': 'ET',
        'egypt': 'EG', 'eg': 'EG',
        'morocco': 'MA', 'ma': 'MA',
        'senegal': 'SN', 'sn': 'SN',
        'ivory coast': 'CI', 'ci': 'CI', "côte d'ivoire": 'CI'
    }
    
    # Gender detection
    if 'male' in query or 'men' in query or 'boys' in query or 'guys' in query:
        filters['gender'] = 'male'
    elif 'female' in query or 'women' in query or 'girls' in query or 'ladies' in query:
        filters['gender'] = 'female'
    
    # Age group detection
    age_groups = {
        'child': 'child',
        'children': 'child',
        'kids': 'child',
        'teenager': 'teenager',
        'teenagers': 'teenager',
        'teens': 'teenager',
        'adult': 'adult',
        'adults': 'adult',
        'senior': 'senior',
        'seniors': 'senior',
        'elderly': 'senior',
        'old': 'senior'
    }
    
    for word, group in age_groups.items():
        if word in query:
            filters['age_group'] = group
            break
    
    # Age range for "young"
    if 'young' in query:
        filters['min_age'] = 16
        filters['max_age'] = 24
    
    # Age operators (above, below, between)
    import re
    
    # Pattern: "above X", "older than X", "over X"
    above_match = re.search(r'(?:above|older than|over|greater than|>)\s*(\d+)', query)
    if above_match:
        filters['min_age'] = int(above_match.group(1))
    
    # Pattern: "below X", "younger than X", "under X"
    below_match = re.search(r'(?:below|younger than|under|less than|<)\s*(\d+)', query)
    if below_match:
        filters['max_age'] = int(below_match.group(1))
    
    # Pattern: "between X and Y"
    between_match = re.search(r'between\s*(\d+)\s*and\s*(\d+)', query)
    if between_match:
        filters['min_age'] = int(between_match.group(1))
        filters['max_age'] = int(between_match.group(2))
    
    # Country detection
    for country_name, country_code in countries.items():
        if country_name in query:
            filters['country_id'] = country_code
            break
    
    # If no filters were found, return None
    if not filters:
        return None
    
    return filters