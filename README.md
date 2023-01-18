# Rubicon_parser

Parses most paradox text files.

Designed and tested for Victoria 3

## How to use:

add read_source_files.py to your project.

Public function that should be called is **parse_text_file(arg)**
+ Arg: string containing path
+ Return: nested dictionary

## Unsupported files

See unsupported files.txt for all files in ..\Victoria 3\game\ that don't work with this parser yet.

Other files may be improperly parsed without causing errors. Please check if the function returns a proper dictionary.

## Other errors

There are other issues that pop-up because the parser was designed around a specific file.

For these limitations check the Issues.

## Future

If this method of parsing seems to be feasable I would like to improve the parsing logic so it won't break on the files in the unsupported files list.

Something I might try to add is a function to properly write a nested dictionary back.

But first I would like to improve the testing code to detect other files that aren't properly parsed.
