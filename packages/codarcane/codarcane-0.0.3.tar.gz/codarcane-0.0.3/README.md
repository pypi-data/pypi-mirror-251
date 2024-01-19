# Codarcane

***Your go-to repository for code snippets.***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

Codarcane is a simple Python command-line tool that allows you to manage and organize your code snippets. You can add, display, search, delete, and copy your code snippets to the clipboard with ease. This tool is built with Click, a Python package for creating command line interfaces. 

If you prefer a visual walkthrough, I've created a YouTube tutorial where I explain the package and its features. You can watch it here:

[Building a CLI Code Snippet Manager with Python Click](https://www.youtube.com/watch?v=zxSOiFhjrhc)

## Quick Setup

Install the package as follows:

```bash
pip install codarcane
```

## Usage

### Adding a Snippet

To add a new code snippet, use the `add` command:

```bash
codarcane add
```

You will prompted to enter the snippet title, language, and the code itself.

### Displaying Snippets

To display all your code snippets, use the `display` command:

```bash
codarcane display
```

This command will list all your snippets with their titles, languages, and code.

### Searching for Snippets

You can search for specific snippets using the `search` command. Provide a keyword as an argument to find matching snippets by title or language:

```bash
codarcane search keyword
```

### Editing a Snippet

To edit an existing code snippet, use the `edit` command:

```bash
codarcane edit
```
You will be presented with a list of snippets to choose from. Enter the number corresponding to the snippet you want to edit. You can then choose to edit the title, language, or code.

### Copying a Snippet to Clipboard

If you want to copy a snippet's code to your clipboard, use the `copy` command:

```bash
codarcane copy
```

You will be presented with a list of snippets to choose from. Enter the number corresponding to the snippet you 
want to copy.

### Deleting a Snippet

To delete a snippet, use the `delete` command:

```bash
codarcane delete
```

You will be presented with a list of snippets to choose from. Enter the number correspoding to the snippet you want to delete.

### Exporting a Snippet

You can export your code snippets to different format for sharing or backup purposes using the `export` command. Choose the export format (markdown or text) and specify the output file.

Markdown:

```bash
codarcane export output.md
```
Or, text:

```bash
codarcane export output.txt
```

## Data Storage

Your code snippets are stored in a JSON file named `snippets.json` within the **snippet** folder. This folder is automatically created on your computer. Make sure not to delete or modify this file manually, as it may lead to data loss.

## Contributing

If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. I welcome any improvements or bug fixes. You can also submit issues on [GitLab](https://gitlab.com/rochdikhalid/codarcane/-/issues) for bug reports or feature requests.
