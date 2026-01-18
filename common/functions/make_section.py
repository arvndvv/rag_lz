import re

CV_HEADING_PATTERNS = {
    'summary': ['summary', 'professional summary', 'profile', 'career summary', 'about me', 'objective'],
    'skills': ['skills', 'key skills', 'technical skills', 'professional skills', 'core skills', 'competencies', 'expertise'],
    'experience': ['experience', 'work experience', 'professional experience', 'employment history', 'career history', 'work history'],
    'education': ['education', 'academic background', 'educational qualifications', 'qualifications'],
    'projects': ['projects', 'personal projects', 'academic projects', 'professional projects'],
    'certifications': ['certifications', 'licenses', 'certified courses', 'certificates', 'certificate'],
    'achievements': ['achievements', 'accomplishments', 'awards', 'honors'],
    'interests': ['interests', 'hobbies', 'activities', 'extracurricular activities'],
    'languages': ['languages', 'language proficiency'],
    'publications': ['publications', 'research', 'papers'],
    'references': ['references', 'referees'],
    'personal': ['personal details', 'personal information', 'contact details']
}

def spaced_word(word):
    """
    Converts 'word' to 'w\\s*o\\s*r\\s*d' to match spaced-out text.
    """
    return r'\s*'.join(list(word))

def spaced_phrase(phrase):
    """
    Splits a phrase, applies spaced_word to parts, and rejoins with flexible whitespace.
    """
    words = phrase.strip().split()
    return r'\s+'.join([spaced_word(w) for w in words])

def build_heading_regex(variants):
    patterns = []
    for v in variants:
        escaped = re.escape(v)
        patterns.append(escaped)
        # If the variant is purely alphabetic (allowing spaces), create a spaced version
        if re.match(r'^[a-zA-Z\s]+$', v):
            patterns.append(spaced_phrase(v))
    
    # Construct the regex pattern
    # Corresponds to JS: ^\s*(?:#{1,6}\s*)?[\*_]*(?:patterns)[\s\*_\.\-:]*$
    pattern_string = (
        r'^\s*(?:#{1,6}\s*)?[\*_]*(?:' + 
        '|'.join(patterns) + 
        r')[\s\*_\.\-:]*$'
    )
    
    return re.compile(pattern_string, re.IGNORECASE | re.MULTILINE)

def detect_cv_headings(cv_text):
    # Using splitlines() handles \r\n and \n automatically
    lines = cv_text.splitlines()
    headings = []
    
    for section, variants in CV_HEADING_PATTERNS.items():
        regex = build_heading_regex(variants)
        for index, line in enumerate(lines):
            # Using search ensures we check the pattern against the string.
            # Since the pattern has ^ and $, it validates the whole line structure.
            if regex.search(line):
                headings.append({
                    'section': section,
                    'line': line.strip(),
                    'lineNumber': index
                })
    
    # Sort by line number
    return sorted(headings, key=lambda x: x['lineNumber'])

def extract_sections(cv_text):
    headings = detect_cv_headings(cv_text)
    lines = cv_text.splitlines()
    sections = {}

    # Extract 'general' section (text before the first heading)
    if headings and headings[0]['lineNumber'] > 0:
        sections['general'] = '\n'.join(lines[:headings[0]['lineNumber']]).strip()

    for i in range(len(headings)):
        start = headings[i]['lineNumber'] + 1
        # If there is a next heading, end there; otherwise go to end of text
        if i + 1 < len(headings):
            end = headings[i + 1]['lineNumber']
        else:
            end = len(lines)
            
        content = '\n'.join(lines[start:end]).strip()
        
        # In case duplicate sections exist, this implementation overwrites (like the JS version).
        # To append instead, you would check if key exists.
        sections[headings[i]['section']] = content

    return sections

# --- TEST ---
if __name__ == "__main__":
    data = """
#### **Professional Summary**
A final year B.Tech...

#### **Education**
# **Cochin University...**
#### **P R O J E C T S:---**
new project
# **Experience:**
# **Project Intern at N-OMS**
- Contributed to the N-OMS...
"""
    
    result = extract_sections(data)
    print(result)