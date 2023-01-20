# Rubicon_parser

Parses most paradox text files.

Designed and tested for Victoria 3

## How to use:

add read_source_files.py to your project.

Public function that should be called is **parse_text_file(arg)**
+ Arg: string containing path
+ Return: nested dictionary

## Errors

There are some issues with the parser because it was designed around a specific file. Cases that were not present in that file could break the dictionary generated by this parser. Some issues have been adressed already.

For details on these limitations check the Issues.

## Future

In addition to adress open issues I might add in the future:
+ A function to properly write a nested dictionary back.
+ Improve the testing code to detect other files that aren't properly parsed.
