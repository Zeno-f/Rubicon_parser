# Rubicon_parser

Parses most paradox text files.

Designed and tested for Victoria 3

## How to use:

add read_source_files.py to your project.

Public function that should be called is **parse_text_file(arg)**
+ Arg: string containing path
+ Return: nested dictionary

## Unsupported files

All text files are parsed without errors. For other issues see below.

## Other errors

There are other issues that pop-up because the parser was designed around a specific file.

For these limitations check the Issues.

## Future

Something I might try to add is a function to properly write a nested dictionary back.

But first I would like to improve the testing code to detect other files that aren't properly parsed.
