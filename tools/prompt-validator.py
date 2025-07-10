#!/usr/bin/env python3
"""
Prompt Validator Tool

A simple tool to validate prompt structure and quality.
Checks for common issues and provides improvement suggestions.
"""

import re
import argparse
from typing import List, Dict, Tuple


class PromptValidator:
    def __init__(self):
        self.issues = []
        self.suggestions = []
        
    def validate(self, prompt: str) -> Dict:
        """Validate a prompt and return analysis results."""
        self.issues = []
        self.suggestions = []
        
        # Run all validation checks
        self._check_length(prompt)
        self._check_clarity(prompt)
        self._check_structure(prompt)
        self._check_specificity(prompt)
        self._check_context(prompt)
        
        return {
            'prompt': prompt,
            'score': self._calculate_score(),
            'issues': self.issues,
            'suggestions': self.suggestions,
            'word_count': len(prompt.split()),
            'character_count': len(prompt)
        }
    
    def _check_length(self, prompt: str):
        """Check if prompt length is appropriate."""
        word_count = len(prompt.split())
        
        if word_count < 5:
            self.issues.append("Prompt is too short - may lack necessary detail")
            self.suggestions.append("Add more context and specific instructions")
        elif word_count > 500:
            self.issues.append("Prompt is very long - may be overwhelming")
            self.suggestions.append("Consider breaking into smaller, focused prompts")
    
    def _check_clarity(self, prompt: str):
        """Check for clarity issues."""
        # Check for vague words
        vague_words = ['thing', 'stuff', 'something', 'anything', 'everything']
        found_vague = [word for word in vague_words if word.lower() in prompt.lower()]
        
        if found_vague:
            self.issues.append(f"Contains vague words: {', '.join(found_vague)}")
            self.suggestions.append("Replace vague words with specific terms")
        
        # Check for unclear pronouns
        pronouns = re.findall(r'\b(it|this|that|they|them)\b', prompt.lower())
        if len(pronouns) > 3:
            self.issues.append("Many unclear pronouns - may cause confusion")
            self.suggestions.append("Replace pronouns with specific nouns")
    
    def _check_structure(self, prompt: str):
        """Check prompt structure."""
        # Check for clear instructions
        instruction_words = ['write', 'create', 'analyze', 'explain', 'describe', 
                           'generate', 'summarize', 'translate', 'compare']
        
        has_instruction = any(word in prompt.lower() for word in instruction_words)
        if not has_instruction:
            self.issues.append("No clear instruction verb found")
            self.suggestions.append("Start with a clear action verb (write, create, analyze, etc.)")
        
        # Check for output format specification
        format_indicators = ['format', 'structure', 'bullet points', 'numbered list', 
                           'paragraph', 'json', 'table', 'markdown']
        
        has_format = any(indicator in prompt.lower() for indicator in format_indicators)
        if not has_format and len(prompt.split()) > 20:
            self.suggestions.append("Consider specifying the desired output format")
    
    def _check_specificity(self, prompt: str):
        """Check for specificity."""
        # Check for specific constraints
        constraint_words = ['word', 'sentence', 'paragraph', 'page', 'minute', 
                          'example', 'step', 'point', 'item']
        
        has_constraints = any(word in prompt.lower() for word in constraint_words)
        if not has_constraints:
            self.suggestions.append("Add specific constraints (length, format, examples)")
        
        # Check for audience specification
        audience_words = ['audience', 'reader', 'user', 'customer', 'student', 
                         'professional', 'beginner', 'expert']
        
        has_audience = any(word in prompt.lower() for word in audience_words)
        if not has_audience and len(prompt.split()) > 15:
            self.suggestions.append("Consider specifying the target audience")
    
    def _check_context(self, prompt: str):
        """Check for context provision."""
        context_indicators = ['context', 'background', 'situation', 'scenario', 
                            'for', 'about', 'regarding']
        
        has_context = any(indicator in prompt.lower() for indicator in context_indicators)
        if not has_context and len(prompt.split()) > 10:
            self.suggestions.append("Provide relevant context or background information")
    
    def _calculate_score(self) -> int:
        """Calculate overall prompt quality score (0-100)."""
        base_score = 100
        
        # Deduct points for issues
        score_deduction = len(self.issues) * 15
        
        # Bonus for having suggestions implemented
        if len(self.suggestions) == 0:
            base_score += 10
        
        return max(0, min(100, base_score - score_deduction))


def main():
    parser = argparse.ArgumentParser(description='Validate prompt quality')
    parser.add_argument('prompt', nargs='?', help='Prompt to validate')
    parser.add_argument('-f', '--file', help='File containing prompt to validate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Get prompt text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prompt_text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            return 1
    elif args.prompt:
        prompt_text = args.prompt
    else:
        print("Please provide a prompt either as argument or via --file option")
        return 1
    
    # Validate prompt
    validator = PromptValidator()
    result = validator.validate(prompt_text)
    
    # Display results
    print(f"\\n{'='*50}")
    print("PROMPT VALIDATION RESULTS")
    print(f"{'='*50}")
    print(f"Score: {result['score']}/100")
    print(f"Word Count: {result['word_count']}")
    print(f"Character Count: {result['character_count']}")
    
    if result['issues']:
        print(f"\\n🚨 ISSUES FOUND ({len(result['issues'])}):")
        for i, issue in enumerate(result['issues'], 1):
            print(f"  {i}. {issue}")
    
    if result['suggestions']:
        print(f"\\n💡 SUGGESTIONS ({len(result['suggestions'])}):")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    
    if not result['issues'] and not result['suggestions']:
        print("\\n✅ Great! No issues found.")
    
    if args.verbose:
        print(f"\\n📝 ORIGINAL PROMPT:")
        print(f"'{prompt_text}'")
    
    print(f"\\n{'='*50}")
    
    return 0


if __name__ == "__main__":
    exit(main())