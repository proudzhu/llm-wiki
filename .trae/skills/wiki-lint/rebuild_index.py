import os, re, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

def get_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(2000)
    m = re.search(r'---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm

def get_entity_summary(filepath):
    """Extract a one-line summary from an entity page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Try to get the first paragraph after the H1 heading
    lines = content.split('\n')
    in_body = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and not in_body:
            in_body = True
            continue
        if in_body and stripped and not stripped.startswith('---') and not stripped.startswith('>') and not stripped.startswith('!') and not stripped.startswith('- ') and not stripped.startswith('**Affiliation**') and not stripped.startswith('**Role**') and not stripped.startswith('**Research Focus**') and not stripped.startswith('**Notable') and len(stripped) > 20:
            return stripped[:150]
    # Fallback: try frontmatter
    fm = get_frontmatter(filepath)
    if 'summary' in fm:
        return fm['summary'][:150]
    return ''

def get_concept_summary(filepath):
    """Extract a one-line summary from a concept page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm = get_frontmatter(filepath)
    if 'summary' in fm:
        return fm['summary'][:150]
    lines = content.split('\n')
    in_body = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and not in_body:
            in_body = True
            continue
        if in_body and stripped and not stripped.startswith('---') and not stripped.startswith('>') and not stripped.startswith('!') and not stripped.startswith('|') and not stripped.startswith('- ') and len(stripped) > 20:
            return stripped[:150]
    return ''

def get_source_summary(filepath):
    """Extract a one-line summary from a source page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fm = get_frontmatter(filepath)
    if 'summary' in fm:
        return fm['summary'][:150]
    return ''

def title_from_name(name):
    words = name.replace('-', ' ').split()
    result = []
    for w in words:
        if w.lower() in ('of', 'the', 'and', 'for', 'in', 'on', 'a', 'an', 'to', 'vs', 'mc', 'bc', 'anc', 'svm', 'lms', 'fxlms', 'mvdr', 'mwf', 'vslf', 'scm', 'doa', 'rtf', 'wng', 'dl', 'evd', 'itl', 'mcc', 'gmcc', 'ggd', 'pod', 'mse', 'lmmse', 'mpdr', 'gsc', 'lcMV', 'soCP', 'rmt', 'vm', 'rm', 'bf', 'se', 'crn', 'lstm', 'bptt', 'fptt', 'snn', 'ann', 'dnn', 'cnn', 'gan', 'dfanc', 'ekf', 'dfg', 'sfanc', 'pd', 'dsfanc', 'gfanc', 'e2e', 'cfg', 'frm', 'hmm', 'cam', 'isnr', 'ddap', 'aAR', 'sht', 'sh', 'bcs', 'asr', 'vad', 'conformer', 'unilstm', 'bilstm', 'vlm', 'ndf', 'vdm', 'dma', 'ldma', 'cdma', 'rt60', 'drr', 'edt', 'di', 'ir', 'hrtf', 'dhrtf', 'imu', 'afc', 'imc', 'mvc', 'ff', 'fb', 'qp', 'ode', 'wpr1', 'is', 'rnn', 'lrn', 'rtl', 'mcalms', 'mvanc', 'hvsf', 'obs', 'tasnet', 'dtw', 'spm', 'vss', 'fxaps', 'fxgmcc', 'ifxgmcc', 'c-ifxgmcc', 'lqg', 'hinf', 'flnn', 'rls'):
            result.append(w.upper() if len(w) <= 4 else w)
        else:
            result.append(w.capitalize())
    return ' '.join(result)

# Read existing index entries
def read_index_entries(filepath):
    """Read existing entries from an index file, return dict of name -> (summary, date)."""
    entries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match table rows: | [[dir/name|Display]] | summary | date |
    pattern = r'\|\s*\[\[(?:entities|concepts|sources|synthesis|queries)/([^\|]+)\|[^\]]+\]\]\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
    for m in re.finditer(pattern, content):
        name = m.group(1).strip()
        summary = m.group(2).strip()
        date = m.group(3).strip()
        entries[name] = (summary, date)
    return entries

# Read existing wiki/index.md entries
existing_entities = read_index_entries('wiki/index.md')
existing_concepts = read_index_entries('wiki/index.md')
existing_sources = read_index_entries('wiki/index.md')

# Actually, let me re-read more carefully - the pattern above matches all types
# Let me separate them properly
def read_index_entries_by_type(filepath, dir_type):
    """Read existing entries from wiki/index.md for a specific section."""
    entries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find the section
    section_pattern = r'## ' + dir_type.capitalize() + r'\s*\n.*?\n(.*?)(?=\n---|\n## |\Z)'
    section_m = re.search(section_pattern, content, re.DOTALL)
    if not section_m:
        return entries
    section = section_m.group(1)
    # Handle both escaped \| and unescaped | in wikilinks
    pattern = r'\|\s*\[\[' + dir_type + r'/([^\|\\]+)(?:\\?\|[^\]]+)?\]\]\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
    for m in re.finditer(pattern, section):
        name = m.group(1).strip()
        summary = m.group(2).strip()
        date = m.group(3).strip()
        entries[name] = (summary, date)
    return entries

existing_entities = read_index_entries_by_type('wiki/index.md', 'entities')
existing_concepts = read_index_entries_by_type('wiki/index.md', 'concepts')
existing_sources = read_index_entries_by_type('wiki/index.md', 'sources')

print("Existing entities in index: %d" % len(existing_entities))
print("Existing concepts in index: %d" % len(existing_concepts))
print("Existing sources in index: %d" % len(existing_sources))

# Find missing entries
def find_missing(directory, existing):
    files = sorted(glob.glob('wiki/%s/*.md' % directory))
    files = [f for f in files if not f.endswith('index.md')]
    missing = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        if name not in existing:
            fm = get_frontmatter(f)
            date = fm.get('updated', fm.get('created', 'unknown'))
            if directory == 'entities':
                summary = get_entity_summary(f)
            elif directory == 'concepts':
                summary = get_concept_summary(f)
            else:
                summary = get_source_summary(f)
            display = title_from_name(name)
            missing.append((name, display, summary, date))
    return missing

missing_entities = find_missing('entities', existing_entities)
missing_concepts = find_missing('concepts', existing_concepts)
missing_sources = find_missing('sources', existing_sources)

print("\n=== MISSING ENTITIES (%d) ===" % len(missing_entities))
for name, display, summary, date in missing_entities:
    print('| [[entities/%s|%s]] | %s | %s |' % (name, display, summary, date))

print("\n=== MISSING CONCEPTS (%d) ===" % len(missing_concepts))
for name, display, summary, date in missing_concepts:
    print('| [[concepts/%s|%s]] | %s | %s |' % (name, display, summary, date))

print("\n=== MISSING SOURCES (%d) ===" % len(missing_sources))
for name, display, summary, date in missing_sources:
    print('| [[sources/%s|%s]] | %s | %s |' % (name, display, summary, date))
