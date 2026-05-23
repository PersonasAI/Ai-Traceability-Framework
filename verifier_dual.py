#!/usr/bin/env python3
"""
Dual Authorship Verifier - v1.0
Analyzes: Output (Persona) + Prompt (Prompter Style)
"""

import sys
import re

# ECHO PERSONA SIGNATURES
ECHO_VOCAB = ['nostalgia', 'nostalgic', 'fading', 'decay', 'analog', 'cassette', 'vinyl', 
              'worn', 'aged', 'memory', 'memories', 'lo-fi', 'lofi', 'imperfect', 'flaw',
              'crackle', 'hiss', 'tape', 'warm', 'bittersweet']

ECHO_PATTERNS = [
    r'sun-?bleached', r'scratched', r'degraded', r'preserved',
    r'lost\s+(studio|recording|moment)', r'passing\s+time',
    r'beauty\s+in\s+(imperfection|decay|aging)'
]

ECHO_THEMES = ['time passing', 'lost moments', 'analog technology', 'imperfection',
               'urban loneliness', 'late night', 'preservation']

# MARCUS PROMPTER SIGNATURES
MARCUS_BPM_EXACT = r'BPM[:\s]+\d{2,3}(?!\s*-)'  # BPM: 87 (not BPM: 80-90)
MARCUS_VECTOR = r'(?:melancholy|energy|nostalgia)[:\s=]+\d{1,2}'  # Melancholy=8
MARCUS_INSTRUMENTS_ROLE = r'\w+\s+\([^)]*(?:lead|texture|sub|rhythm|fill|foundation)[^)]*\)'
MARCUS_TECHNICAL_PERCENT = r'(?:reverb|compression|width|saturation)[:\s]+\w+\s+\d{1,3}%'
MARCUS_STRUCTURE_BARS = r'\d+\s+bars?'

def analyze_output_for_echo(text):
    """Detect ECHO persona in generated output"""
    text_lower = text.lower()
    
    vocab_count = sum(text_lower.count(word) for word in ECHO_VOCAB)
    pattern_count = sum(len(re.findall(p, text_lower)) for p in ECHO_PATTERNS)
    theme_count = sum(text_lower.count(theme) for theme in ECHO_THEMES)
    
    # Scoring
    vocab_score = min(vocab_count * 5, 40)
    pattern_score = min(pattern_count * 10, 30)
    theme_score = min(theme_count * 8, 30)
    
    total = vocab_score + pattern_score + theme_score
    return min(total, 100)

def analyze_prompt_for_marcus(prompt_text):
    """Detect MARCUS prompter style in prompt used"""
    
    has_exact_bpm = bool(re.search(MARCUS_BPM_EXACT, prompt_text))
    vector_count = len(re.findall(MARCUS_VECTOR, prompt_text, re.IGNORECASE))
    role_count = len(re.findall(MARCUS_INSTRUMENTS_ROLE, prompt_text, re.IGNORECASE))
    technical_count = len(re.findall(MARCUS_TECHNICAL_PERCENT, prompt_text, re.IGNORECASE))
    bars_count = len(re.findall(MARCUS_STRUCTURE_BARS, prompt_text))
    
    # Check fixed order (simplified: genre first, BPM second)
    lines = [l.strip() for l in prompt_text.split('\n') if l.strip()]
    has_order = False
    if len(lines) >= 2:
        if 'genre' in lines[0].lower() and 'bpm' in lines[1].lower():
            has_order = True
    
    # Scoring
    score = 0
    if has_exact_bpm: score += 20
    score += min(vector_count * 15, 30)  # Up to 2 vectors expected
    score += min(role_count * 8, 24)      # Up to 3 instruments
    score += min(technical_count * 6, 18) # Up to 3 parameters
    if bars_count >= 2: score += 8
    if has_order: score += 10
    
    return min(score, 100)

def verify_dual_authorship(output_file, prompt_file=None):
    """Main verification function"""
    
    print("\n" + "="*60)
    print("DUAL AUTHORSHIP VERIFICATION - v1.0")
    print("="*60 + "\n")
    
    # Read output
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            output_text = f.read()
    except:
        print(f"❌ Error reading output file: {output_file}")
        return
    
    # Analyze output for ECHO
    echo_score = analyze_output_for_echo(output_text)
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"PERSONA INFLUENCE (in output): {echo_score:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Detected: ECHO")
    
    if echo_score >= 60:
        print(f"Status: ✅ Strong ECHO presence")
    elif echo_score >= 40:
        print(f"Status: ⚠️  Moderate ECHO presence")
    else:
        print(f"Status: ❌ Low ECHO presence")
    
    print()
    
    # Analyze prompt for MARCUS (if provided)
    marcus_score = 0
    if prompt_file:
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
            marcus_score = analyze_prompt_for_marcus(prompt_text)
        except:
            print(f"⚠️  Could not read prompt file: {prompt_file}")
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"PROMPTER INFLUENCE (in prompt): {marcus_score:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if prompt_file:
        print(f"Detected: Marcus Chen style")
        if marcus_score >= 60:
            print(f"Status: ✅ Strong Marcus signature")
        elif marcus_score >= 40:
            print(f"Status: ⚠️  Partial Marcus signature")
        else:
            print(f"Status: ❌ Low Marcus signature")
    else:
        print("No prompt file provided - prompter verification skipped")
    
    print()
    
    # Combined score
    total_score = (echo_score * 0.7 + marcus_score * 0.3) if prompt_file else echo_score
    
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"COMBINED AUTHORSHIP SCORE: {total_score:.1f}%")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if total_score >= 75:
        print("✅ DUAL AUTHORSHIP VERIFIED")
        print("   High confidence in ECHO + Marcus attribution")
    elif total_score >= 60:
        print("⚠️  PARTIAL AUTHORSHIP DETECTED")
        print("   Moderate confidence in attribution")
    else:
        print("❌ LOW AUTHORSHIP SIGNAL")
        print("   Weak attribution - may not have used persona/prompter")
    
    print("\n" + "="*60)
    print("NOTE: This is v1.0 - indicative analysis, not absolute proof")
    print("See LIMITATIONS.md for details on system constraints")
    print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verificador_dual.py <output.txt> [prompt.txt]")
        print("\nExamples:")
        print("  python verificador_dual.py song_lyrics.txt")
        print("  python verificador_dual.py song_lyrics.txt prompt_used.txt")
        sys.exit(1)
    
    output_file = sys.argv[1]
    prompt_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    verify_dual_authorship(output_file, prompt_file)
