const CV_HEADING_PATTERNS = {
    summary: ['summary', 'professional summary', 'profile', 'career summary', 'about me', 'objective'],
    skills: ['skills', 'key skills', 'technical skills', 'professional skills', 'core skills', 'competencies', 'expertise'],
    experience: ['experience', 'work experience', 'professional experience', 'employment history', 'career history', 'work history'],
    education: ['education', 'academic background', 'educational qualifications', 'qualifications'],
    projects: ['projects', 'personal projects', 'academic projects', 'professional projects'],
    certifications: ['certifications', 'licenses', 'certified courses', 'certificates', 'certificate'],
    achievements: ['achievements', 'accomplishments', 'awards', 'honors'],
    interests: ['interests', 'hobbies', 'activities', 'extracurricular activities'],
    languages: ['languages', 'language proficiency'],
    publications: ['publications', 'research', 'papers'],
    references: ['references', 'referees'],
    personal: ['personal details', 'personal information', 'contact details']
};

function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function spacedWord(word) {
    return word.split('').join('\\s*');
}

function spacedPhrase(phrase) {
    return phrase.trim().split(/\s+/).map(w => spacedWord(w)).join('\\s+');
}

function buildHeadingRegex(variants) {
    const patterns = [];
    for (const v of variants) {
        const escaped = escapeRegex(v);
        patterns.push(escaped);
        if (/^[a-zA-Z\s]+$/.test(v)) {
            patterns.push(spacedPhrase(v));
        }
    }
    // Fixed Regex line below:
    return new RegExp(
        `^\\s*(?:#{1,6}\\s*)?[\\*_]*(?:${patterns.join('|')})[\\s\\*_\\.\\-:]*$`,
        'im'
    );
}

function detectCVHeadings(cvText) {
    const lines = cvText.split(/\r?\n/);
    const headings = [];
    Object.entries(CV_HEADING_PATTERNS).forEach(([section, variants]) => {
        const regex = buildHeadingRegex(variants);
        lines.forEach((line, index) => {
            if (regex.test(line)) {
                headings.push({
                    section,
                    line: line.trim(),
                    lineNumber: index
                });
            }
        });
    });
    return headings.sort((a, b) => a.lineNumber - b.lineNumber);
}

function extractSections(cvText) {
    const headings = detectCVHeadings(cvText);
    const lines = cvText.split(/\r?\n/);
    const sections = {};

    if (headings.length > 0 && headings[0].lineNumber > 0) {
        sections['general'] = lines.slice(0, headings[0].lineNumber).join('\n').trim();
    }

    for (let i = 0; i < headings.length; i++) {
        const start = headings[i].lineNumber + 1;
        const end = i + 1 < headings.length ? headings[i + 1].lineNumber : lines.length;
        sections[headings[i].section] = lines.slice(start, end).join('\n').trim();
    }
    return sections;
}

// --- TEST ---
const data = `
#### **Professional Summary**
A final year B.Tech...

#### **Education**
# **Cochin University...**
#### **P R O J E C T S:---**
new project
# **Experience**
# **Project Intern at N-OMS**
- Contributed to the N-OMS...
`;



console.log(extractSections(data))

module.exports = {
    extractSections
};

