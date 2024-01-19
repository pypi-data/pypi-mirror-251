import os
import click
import json
from pathlib import Path
import pyperclip


# Create a command line group
@click.group(help='Codarcane - Your go-to repository for code snippets.')
def cli():
    pass


# The path to the JSON file
JSON_FILE_PATH =  Path('snippets/snippets.json')


# Helper function to load snippets from the JSON file
def load_snippets():
    snippets = []
    try:
        with JSON_FILE_PATH.open('r') as f:
            snippets = json.load(f)
    except FileNotFoundError:
        # If the file is not found, create an empty list
        snippets = []
    except json.JSONDecodeError:
        # Handle JSON decoding errors (invalid JSON)
        print('Error: Invalid JSON format in the snippets file.')
    return snippets


# Helper function to save snippets to the JSON file
def save_snippets(snippets):
    try:
        with JSON_FILE_PATH.open('w') as f:
            json.dump(snippets, f, indent=4)
    except FileNotFoundError:
        # If the file is not found, create the necessary directories and then save
        JSON_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with JSON_FILE_PATH.open('w') as f:
            json.dump(snippets, f, indent=4)
    except Exception as e:
        # Handle other exceptions (e.g., permission denied)
        print(f'Error: An error occurred while saving snippets - {e}')


# Helper function to export snippets as Markdown
def export_as_markdown(snippets, output_file):
    for snippet in snippets:
        output_file.write(f"**Title:** {snippet['title']}\n")
        output_file.write(f"**Language:** {snippet['language']}\n")
        output_file.write(f"```\n{snippet['code']}\n```\n\n")


# Helper function to export snippets as plain text
def export_as_text(snippets, output_file):
    for snippet in snippets:
        output_file.write(f"Title: {snippet['title']}\n")
        output_file.write(f"Language: {snippet['language']}\n")
        output_file.write(f"Code:\n{snippet['code']}\n\n")


# Command to add a new code snippet
@click.command(help='Add a new code snippet.')
def add():
    # Prompt the user for snippet details
    title = input('Enter snippet title: ')
    while not title.strip():  # Check for empty input
        print('Title cannot be empty.')
        title = input('Enter snippet title: ')

    # Validate title length (optional)
    max_title_length = 100
    if len(title) > max_title_length:
        print(
            f'Title is too long. Maximum length is {max_title_length} characters.')
        return

    language = input('Enter snippet language: ')
    while not language.strip():  # Check for empty input
        print('Language cannot be empty.')
        language = input('Enter snippet language: ')

    # Validate language length (optional)
    max_language_length = 20
    if len(language) > max_language_length:
        print(
            f'Language is too long. Maximum length is {max_language_length} characters.')
        return

    code = input('Enter the code snippet: ')
    while not code.strip():  # Check for empty input
        print('Code cannot be empty.')
        code = input('Enter the code snippet: ')

    # Load existing snippets from the JSON file
    snippets = load_snippets()

    # Append the new snippet to the list of snippets
    snippets.append({"title": title, "language": language, "code": code})

    # Write the updated list of snippets back to the JSON file
    save_snippets(snippets)

    print('Snippet added successfully!')


# Command to display all code snippets
@click.command(help='Display all code snippets.')
def display():
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    # Display details of each snippet
    for snippet in snippets:
        print(f"Title: {snippet['title']}")
        print(f"Language: {snippet['language']}")
        print(f"Code: {snippet['code']}")


# Command to search for code snippets
@click.command(help='Search for code snippets by keyword.')
@click.argument('keyword')
def search(keyword):
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    # Filter snippets based on the keyword in title or language
    results = [snippet for snippet in snippets if keyword.lower(
    ) in snippet['title'].lower() or keyword.lower() in snippet['language'].lower()]

    if results:
        # Display details of matching snippets
        for result in results:
            print(f"Title: {result['title']}")
            print(f"Language: {result['language']}")
            print(f"Code: {result['code']}")
    else:
        print('No matching snippets found')


# Command to copy a code snippet to the clipboard
@click.command(help='Copy a code snippet to the clipboard.')
def copy():
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    # Display a list of snippets to choose from
    for idx, snippet in enumerate(snippets):
        print(f"{idx + 1}. {snippet['title']} - {snippet['language']}")

    try:
        # Prompt the user to select a snippet by number
        choice = int(input('Enter the number of the snippet to copy: ')) - 1

        if 0 <= choice < len(snippets):
            # Copy the selected snippet's code to the clipboard
            snippet = snippets[choice]
            pyperclip.copy(snippet['code'])
            print('Snippet copied to Clipboard!')
        else:
            print('Invalid choice. Please enter a number within the range of available snippets.')
    except ValueError:
        print('Invalid input. Please enter a valid number.')
        return


# Command to edit a code snippet
@click.command(help='Edit an existing code snippet.')
def edit():
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    # Display a list of snippets to choose from
    for idx, snippet in enumerate(snippets):
        print(f"{idx + 1}. {snippet['title']} - {snippet['language']}")

    # Prompt the user to select a snippet by number for editing
    choice = input('Enter the number of the snippet to edit: ')

    try:
        choice = int(choice)
        if 1 <= choice <= len(snippets):
            choice -= 1  # Adjust for zero-based indexing
        else:
            print('Invalid choice. Please enter a number within the range.')
            return
    except ValueError:
        print('Invalid input. Please enter a valid number.')
        return

    # Display the selected snippet before editing
    print("\nSelected Snippet:")
    print(f"Title: {snippets[choice]['title']}")
    print(f"Language: {snippets[choice]['language']}")
    print(f"Code: {snippets[choice]['code']}")

    # Allow the user to edit each field one by one
    for field in ['title', 'language', 'code']:
        new_value = input(f'Enter the new {field} (hit Enter to skip): ')
        if new_value.strip():  # Update the field only if the user enters a non-empty value
            snippets[choice][field] = new_value

    # Write the updated list of snippets back to the JSON file
    save_snippets(snippets)

    print('\nSnippet edited successfully!')


# Command to delete a code snippet
@click.command(help='Delete an existing code snippet.')
def delete():
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    # Display a list of snippets to choose from
    for idx, snippet in enumerate(snippets):
        print(f"{idx + 1}. {snippet['title']} - {snippet['language']}")

    try:
        # Prompt the user to select a snippet by number for deletion
        choice = int(input('Enter the number of the snippet to delete: ')) - 1

        if 0 <= choice < len(snippets):
            # Delete the selected snippet
            del snippets[choice]

            # Write the updated list of snippets back to the JSON file
            save_snippets(snippets)

            print('Snippet deleted successfully!')

        else:
            print('Invalid choice. Please enter a number within the range of available snippets.')
    except ValueError:
        print('Invalid input. Please enter a valid number.')
        return


# Command to export snippets to a different format
@click.command(help='Export snippets to a different format (markdown or text).')
@click.option('--format', type=click.Choice(['markdown', 'text']), default='markdown',
              help='Export format (markdown or text)')
@click.argument('output_file', type=click.File('w'))
def export(format, output_file):
    # Load existing snippets from the JSON file
    snippets = load_snippets()

    if not snippets:
        print('No snippets available. Add a snippet using the "add" command first.')
        return

    if format == 'markdown':
        export_as_markdown(snippets, output_file)
    elif format == 'text':
        export_as_text(snippets, output_file)

    print(f'Snippets exported to {format} file: {output_file.name}')


# Add the command function to the command group
cli.add_command(add)
cli.add_command(display)
cli.add_command(search)
cli.add_command(copy)
cli.add_command(edit)
cli.add_command(delete)
cli.add_command(export)


if __name__ == '__main__':
    cli()
