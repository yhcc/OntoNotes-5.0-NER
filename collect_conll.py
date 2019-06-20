# encoding=utf-8
from __future__ import print_function
import os, glob, itertools
import argparse

def generate_collection(tag, dir_name, domains, lang, version, re):
    results = itertools.chain.from_iterable(glob.iglob(os.path.join(root, re))
                        for root, dirs, files in os.walk(os.path.join('conll-formatted-ontonotes-5.0', version, 'data',
                                                                      tag, 'data', lang)))
    text = ""
    word_count = 0
    sent_count = 0
    for cur_file in results:
        flag = False
        for d in domains:
            if os.path.sep + d + os.path.sep in cur_file:
                flag = True
                break
        if not flag:
            continue
        with open(cur_file, 'r') as f:
            # print(cur_file)
            for line in f.readlines():
                ls = line.split(" ")
                if len(ls) >= 11:
                    text += line
                    word_count += 1
                else:
                    text += '\n'
                    if not line.startswith('#'):
                        sent_count += 1
            text += '\n'
            # break
    if tag == 'development':
        tag = 'dev'

    filepath = os.path.join(dir_name, tag + '.txt')
    with open(filepath, 'w') as f:
        f.write(text)
    print("For file:{}, there are {} sentences, {} tokens.".format(filepath, sent_count, word_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help="Which version of split, v4 or v12.", default='v4')
    parser.add_argument('-l', '--language', help='Which language to collect.', default='english')
    parser.add_argument('-d', '--domain', nargs='*', help="What domains to use. If not specified, all will be used."
                                                          " You can choose from bc bn mz nw tc wb.")

    args = parser.parse_args()
    version = args.version
    language = args.language
    assert version in ('v4', 'v12')
    assert language in ('english', 'chinese', 'arabic')
    _domains = args.domain
    expected_domains = "bc bn mz nw tc wb".split()
    if _domains is None:
        domains = expected_domains
        dir_name = '{}'.format(version)
    else:
        domains = []
        for d in _domains:
            if d in expected_domains:
                domains.append(d)
            else:
                raise ValueError("domain:{} is not allowed, choose from bc bn mz nw tc wb.".format(d))
        dir_name = '{}_{}'.format(version, '_'.join(list(sorted(domains))))
    dir_name = os.path.join(dir_name, language)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    for split in ['train', 'development', 'test']:
        if version=='v4' and split=='test':
            re = '*auto_conll'
        else:
            re = '*gold_conll'
        generate_collection(tag=split, dir_name=dir_name, lang=language, version=version, domains=domains, re=re)