from read_source_files import parse_text_file
import glob
from pathlib import Path
import concurrent.futures
import json
import os


root_dir = 'D:\\Games\\SteamLibrary\\steamapps\\common\\Victoria 3\\game\\common\\'
dump_dir = 'D:\\Games\\Modding\\Rubicon Project\\ParserDump\\'
txt_file_list = glob.glob('**/*.txt',
                          root_dir=root_dir,
                          recursive=True)

errors = []


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
        errors.append('{0} gives error: {1}'.format(p, E))
    finally:
        pass


if __name__ == '__main__':

    create_dummies()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(parse_victoria3_test, txt_file_list)

    print('done')
