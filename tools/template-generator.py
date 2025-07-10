#!/usr/bin/env python3
"""
Prompt Template Generator

Generates customizable prompt templates based on task type and requirements.
"""

import json
import argparse
from typing import Dict, List


class TemplateGenerator:
    def __init__(self):
        self.templates = {
            'analysis': {
                'structure': [
                    'Analyze {content} and provide:',
                    '1. **Summary**: {summary_instruction}',
                    '2. **Key Findings**: {findings_instruction}',
                    '3. **Implications**: {implications_instruction}',
                    '4. **Recommendations**: {recommendations_instruction}',
                    '',
                    '**Context**: {context}',
                    '**Audience**: {audience}',
                    '**Format**: {format_requirements}'
                ],
                'variables': {
                    'content': 'Content to analyze',
                    'summary_instruction': 'Brief overview requirement',
                    'findings_instruction': 'Key findings requirement',
                    'implications_instruction': 'Implications description',
                    'recommendations_instruction': 'Recommendations requirement',
                    'context': 'Relevant background information',
                    'audience': 'Target audience',
                    'format_requirements': 'Output format specifications'
                }
            },
            'writing': {
                'structure': [
                    'Write a {content_type} about {topic} that:',
                    '- {requirement_1}',
                    '- {requirement_2}',
                    '- {requirement_3}',
                    '',
                    '**Target Audience**: {audience}',
                    '**Tone**: {tone}',
                    '**Length**: {length}',
                    '**Format**: {format}',
                    '',
                    '**Additional Requirements**:',
                    '{additional_requirements}'
                ],
                'variables': {
                    'content_type': 'Type of content (article, email, etc.)',
                    'topic': 'Main topic or subject',
                    'requirement_1': 'First key requirement',
                    'requirement_2': 'Second key requirement',
                    'requirement_3': 'Third key requirement',
                    'audience': 'Target audience description',
                    'tone': 'Desired tone (professional, casual, etc.)',
                    'length': 'Content length specification',
                    'format': 'Output format requirements',
                    'additional_requirements': 'Any additional specifications'
                }
            },
            'coding': {
                'structure': [
                    'Write a {language} {code_type} that {functionality}.',
                    '',
                    '**Requirements**:',
                    '- {requirement_1}',
                    '- {requirement_2}',
                    '- {requirement_3}',
                    '',
                    '**Input**: {input_description}',
                    '**Output**: {output_description}',
                    '**Constraints**: {constraints}',
                    '',
                    '**Additional Notes**:',
                    '- Include error handling',
                    '- Add appropriate comments',
                    '- Follow {language} best practices',
                    '- {additional_notes}'
                ],
                'variables': {
                    'language': 'Programming language',
                    'code_type': 'Type of code (function, class, script, etc.)',
                    'functionality': 'What the code should do',
                    'requirement_1': 'First technical requirement',
                    'requirement_2': 'Second technical requirement',
                    'requirement_3': 'Third technical requirement',
                    'input_description': 'Expected input format/type',
                    'output_description': 'Expected output format/type',
                    'constraints': 'Any limitations or constraints',
                    'additional_notes': 'Additional implementation notes'
                }
            },
            'creative': {
                'structure': [
                    'Create a {creative_type} with the following elements:',
                    '',
                    '**Theme**: {theme}',
                    '**Style**: {style}',
                    '**Mood**: {mood}',
                    '**Setting**: {setting}',
                    '',
                    '**Key Elements to Include**:',
                    '- {element_1}',
                    '- {element_2}',
                    '- {element_3}',
                    '',
                    '**Length**: {length}',
                    '**Target Audience**: {audience}',
                    '**Additional Instructions**: {additional_instructions}'
                ],
                'variables': {
                    'creative_type': 'Type of creative content',
                    'theme': 'Main theme or concept',
                    'style': 'Writing or artistic style',
                    'mood': 'Desired mood or atmosphere',
                    'setting': 'Setting or context',
                    'element_1': 'First key element to include',
                    'element_2': 'Second key element to include',
                    'element_3': 'Third key element to include',
                    'length': 'Content length',
                    'audience': 'Target audience',
                    'additional_instructions': 'Any additional creative directions'
                }
            }
        }
    
    def generate_template(self, template_type: str, custom_vars: Dict = None) -> str:
        """Generate a template with optional custom variables."""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        template = self.templates[template_type]
        structure = template['structure']
        variables = template['variables'].copy()
        
        # Update with custom variables if provided
        if custom_vars:
            variables.update(custom_vars)
        
        # Create the template string
        template_str = '\n'.join(structure)
        
        # Replace variables with placeholders
        for var, description in variables.items():
            placeholder = f'[{var.upper()}: {description}]'
            template_str = template_str.replace(f'{{{var}}}', placeholder)
        
        return template_str
    
    def list_templates(self) -> List[str]:
        """List available template types."""
        return list(self.templates.keys())
    
    def get_template_variables(self, template_type: str) -> Dict:
        """Get variables for a specific template type."""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        return self.templates[template_type]['variables']
    
    def save_template(self, template_type: str, filename: str, custom_vars: Dict = None):
        """Save a generated template to a file."""
        template = self.generate_template(template_type, custom_vars)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {template_type.title()} Prompt Template\n\n")
            f.write(template)
            f.write("\n\n# Usage Instructions\n")
            f.write("Replace the bracketed placeholders with your specific content.\n")
            f.write("Remove any sections that don't apply to your use case.\n")


def main():
    parser = argparse.ArgumentParser(description='Generate prompt templates')
    parser.add_argument('type', nargs='?', help='Template type')
    parser.add_argument('-l', '--list', action='store_true', help='List available templates')
    parser.add_argument('-v', '--variables', help='Show variables for template type')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('--custom', help='JSON string with custom variables')
    
    args = parser.parse_args()
    
    generator = TemplateGenerator()
    
    if args.list:
        print("Available template types:")
        for template_type in generator.list_templates():
            print(f"  - {template_type}")
        return 0
    
    if args.variables:
        try:
            variables = generator.get_template_variables(args.variables)
            print(f"Variables for '{args.variables}' template:")
            for var, desc in variables.items():
                print(f"  {var}: {desc}")
        except ValueError as e:
            print(f"Error: {e}")
            return 1
        return 0
    
    if not args.type:
        print("Please specify a template type or use --list to see available types")
        return 1
    
    # Parse custom variables if provided
    custom_vars = None
    if args.custom:
        try:
            custom_vars = json.loads(args.custom)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in --custom argument")
            return 1
    
    try:
        if args.output:
            generator.save_template(args.type, args.output, custom_vars)
            print(f"Template saved to {args.output}")
        else:
            template = generator.generate_template(args.type, custom_vars)
            print(template)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
