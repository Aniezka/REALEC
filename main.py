import os
import re

folders = 'exam2017_1', 'exam2017_2', 'exam2017_3', 'exam2017_4', \
          'exam2017_5_1', 'exam2017_5_2', 'exam2017_6', 'exam2017_7'

wrong_re = re.compile(r'T\d+\s[a-z_]+\s([0-9]+)\s([0-9]+)\s([a-z\s-]+)', flags=re.IGNORECASE)
correct_re = re.compile(r'#\d+\s+AnnotatorNotes\sT[0-9]+\s([a-z\s-]+)', flags=re.IGNORECASE)

types_map = {'Category_confusion': [],
             'Compound_word': [],
             'Suffix': [],
             'Prefix': [],
             'Formational_affixes': [],
             'Derivation': []}

for folder in folders:

    files = os.listdir(folder)

    for file in files:

        if file.split('.')[1] != 'ann':
            continue

        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            file_content = f.read()

        lines = file_content.split('\n')

        for idx, line in enumerate(lines):

            for now_type in types_map:

                if now_type in line:

                    wrong_line = lines[idx]
                    correct_line = lines[idx + 1]

                    now_wrong = ''
                    now_correct = ''

                    wrong_search = wrong_re.search(wrong_line)
                    correct_search = correct_re.search(correct_line)

                    if wrong_search:

                        wrong_beg = int(wrong_search.group(1))
                        wrong_end = int(wrong_search.group(2))
                        now_wrong = wrong_search.group(3)

                        with open(os.path.join(folder, file.replace('.ann', '.txt')),
                                  'r', encoding='utf-8') as txt_f:
                            txt_file_content = txt_f.read()

                        sentence_beg = re.split(r'[.!?]', txt_file_content[:wrong_beg])[-1]

                        sentence_end = '.'

                        if txt_file_content[wrong_beg + 1] not in ['.', '!', '?']:
                            sentence_end = re.split(r'[.!?]', txt_file_content[wrong_beg:])[0] + sentence_end

                        sentence = sentence_beg + sentence_end

                    if correct_search:
                        now_correct = correct_search.group(1)

                    url = 'http://realec.org/index.xhtml#/exam/' + folder + '/' + file.replace('.ann', '')

                    # result = '; '.join([os.path.join(folder, file), now_type, sentence, now_wrong, now_correct])
                    result = '; '.join([url, now_type, sentence, now_wrong, now_correct])

                    types_map[now_type].append(result)

                    break

for error_type in types_map:

    with open(error_type + '.csv', 'w', encoding='utf-8') as now_file:
        now_file.write('\n'.join(types_map[error_type]))

# http://realec.org/index.xhtml#/exam/exam2017_1/ABl_16_1
