import os
import re
import sys

def find_definitions(filename, search_list):
    with open(filename, 'r') as file:
        lines = file.readlines()

    definitions = []
    for line in lines:
        if any(keyword in line for keyword in search_list):
            definitions.append(line.strip())

    return definitions

def has_documentation(definition_line):
    return '"""' in definition_line

def generate_function_documentation_above(definition_line):
    name_match = re.match(r'\s*def\s+(\w+)', definition_line)
    if name_match:
        name = name_match.group(1)
        indentation = re.match(r'(\s*)', definition_line).group(1)
        
        # Check if 'def' is at the beginning of the line
        if not indentation:
            documentation = f'"""{name} - function module"""\n\n\n'
            return documentation

    return None

def generate_function_documentation_below(definition_line):
    name_match = re.match(r'\s*def\s+(\w+)', definition_line)
    if name_match:
        name = name_match.group(1)
        documentation = f'    """{name} - function module"""\n\n'
        return documentation

def generate_indented_function_documentation_below(definition_line):
    name_match = re.match(r'\s*def\s+(\w+)', definition_line)
    if name_match:
        name = name_match.group(1)
        indentation = re.match(r'(\s*)', definition_line).group(1)
        documentation = f'    {indentation}"""{name} - function module"""\n'
        return documentation

def generate_class_documentation_above(definition_line, first_class):
    name_match = re.match(r'\s*class\s+(\w+)', definition_line)
    if name_match:
        name = name_match.group(1)
        indentation = re.match(r'(\s*)', definition_line).group(1)
        
        # Check if 'class' is at the beginning of the line and it's the first class
        if not indentation and first_class:
            documentation = f'"""{name} - class module"""\n\n\n'
            return documentation

    return None

def generate_class_documentation_below(definition_line):
    name_match = re.match(r'\s*class\s+(\w+)', definition_line)
    if name_match:
        name = name_match.group(1)
        documentation = f'    """{name} - class module"""\n\n\n'
        return documentation


def remove_blank_lines_before_first_import(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the index of the first import line
    first_import_index = next((i for i, line in enumerate(lines) if 'import ' in line or 'from ' in line), None)

    # If the first import line is found, remove two blank lines before it
    if first_import_index is not None and first_import_index >= 2:
        if lines[first_import_index - 1].strip() == '' and lines[first_import_index - 2].strip() == '':
            lines.pop(first_import_index - 2)
            lines.pop(first_import_index - 2)

    # Write the modified lines back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)


def process_file(filename, search_list):
    with open(filename, 'r') as file:
        lines = file.readlines()

    output_lines = []
    in_function_docstring_block = False
    import_lines = []
    first_class = True
    first_import_found = False  # Variable to track if the first import line is found

    for line in lines:
        documentation_above = generate_function_documentation_above(line)
        class_documentation_above = generate_class_documentation_above(line, first_class)
        class_documentation_below = generate_class_documentation_below(line)

        if documentation_above:
            output_lines.append(documentation_above)
        elif class_documentation_above:
            output_lines.append(class_documentation_above)

        if 'import ' in line or 'from ' in line:
            if not first_import_found:
                # If it's the first import line, set first_import_found to True
                first_import_found = True
                import_lines.append(line)
            else:
                import_lines.append(line)
        elif '    def' in line and not has_documentation(line):
            documentation_below = generate_indented_function_documentation_below(line)
            
            output_lines.append(line)  # Add the original '    def' line
            output_lines.append(documentation_below)

            # Trim blank lines before the function body
            while output_lines[-1].strip() == '':
                output_lines.pop()
        elif 'def' in line and not has_documentation(line):
            documentation_below = generate_function_documentation_below(line)
            
            output_lines.append(line)  # Add the original 'def' line
            output_lines.append(documentation_below)

            # Trim blank lines before the function body
            while output_lines[-1].strip() == '':
                output_lines.pop()
        elif class_documentation_below:
            # Move import lines after the documentation above the class module
            import_lines.append('\n\n')
            output_lines.extend(import_lines)
            import_lines = []

            output_lines.append(line)  # Add the original 'class' line
            output_lines.append(class_documentation_below)

            # Trim blank lines before the class body
            while output_lines[-1].strip() == '':
                output_lines.pop()

            first_class = False
        else:
            output_lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(output_lines)
    
    # Remove blank lines before the first import line
    remove_blank_lines_before_first_import(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    file_to_process = sys.argv[1]
    search_list = ['class', 'def', '    def']

    process_file(file_to_process, search_list)
