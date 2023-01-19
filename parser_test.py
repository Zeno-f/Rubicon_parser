from read_source_files import parse_text_file
import glob
from pathlib import Path
import concurrent.futures
import json
import os
from time import perf_counter

"""This test the reach of the parser

adjust root dir to point to the root of the files you want to parse
    WARNING: ..\Victoria 3\game\gfx\map\map_object_data\generated 
            contains very big text files
adjust dump dir to point to the directory where all created dictionaries can 
be dumped



"""

root_dir = 'D:\\Games\\SteamLibrary\\steamapps\\common\\Victoria 3\\game\\common\\'
dump_dir = 'D:\\Games\\Modding\\Rubicon Project\\ParserDump\\'

txt_file_list = glob.glob('**/*.txt',
                          root_dir=root_dir,
                          recursive=True)

errors = []


def write_errors():
    with open((dump_dir + 'errors.txt'), 'w') as out_file:
        out_file.write('\n'.join(str(line) for line in errors))


def create_dummies():
    for txt_file in txt_file_list:
        p = Path(dump_dir + txt_file)

        if not os.path.exists(str(p.parent)):
            os.makedirs(str(p.parent))

        with open(str(p), 'w'):
            pass


def dump_dictionary(txt_dict, txt_file):
    p = Path(dump_dir + txt_file)

    if not os.path.exists(str(p.parent)):
        os.makedirs(str(p.parent))

    out_file = open((dump_dir + txt_file), 'w')

    json.dump(txt_dict, out_file, indent=4)

    out_file.close()


def parse_victoria3_test(txt_file):
    # for txt_file in txt_file_list
    try:
        txt_dict = parse_text_file(str(root_dir + txt_file))
        dump_dictionary(txt_dict, txt_file)
    except WindowsError:
        pass
    except Exception as E:
        p = Path(dump_dir + txt_file)
        # errors.append('{0} gives error: {1}'.format(p, E))
        errors.append('{0}'.format(p))
    finally:
        pass


if __name__ == '__main__':

    t1_start = perf_counter()

    create_dummies()

    t2_start = perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(parse_victoria3_test, txt_file_list)

    t_stop = perf_counter()

    write_errors()

    print('done in {0}, parsing took {1}'.format(t_stop-t1_start,
                                                 t_stop-t2_start))
