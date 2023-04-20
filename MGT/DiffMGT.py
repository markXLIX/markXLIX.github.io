import csv

# ADJUST for source documents
# Define source of input files
input1_source = "CDC"
input2_source = "SSA"

# Define output file directory (relative to main script)
output_dir = 'MGT/Outputs/'

# open .tsv file(s)
#nih_initial = open('NIH_testing.tsv', encoding='utf-8').read().split('\n')
input1_initial = open('C:\GitHub\markXLIX.github.io\MGT\CDC_testing.tsv',
                      encoding='utf-8').read().split('\n')
input2_initial = open('C:\GitHub\markXLIX.github.io\MGT\A_SSA English-Spanish.tsv',
                      encoding='utf-8').read().split('\n')
# END ADJUST for source documents

# COMMENTS
# Pandas caused type errors due to identifying some content as integer rather than string.
# Obviously can fix this but decided to just get it working as a normal list
# Probably just required encoding on read.  will have to test if time permits.
# Might be able to use the Google API to do this all within Google Sheets (without manual TSV export/import)
#cdc_list = pd.read_csv('CDC_testing.tsv', sep='\t', header=None)
#nih_list = pd.read_csv('NIH_testing.tsv', sep='\t', header=None)
# END COMMENTS


def single_sheet_html(english_term_exists, no_match_list_input1_item, no_match_list_input2_item, terms_match,
                      english_count, input1_count, input2_count, match_count):
    html_start = f"""<html lang='en'>
            <meta charset='UTF-8'>
            <title>Page Title</title>
            <meta name='viewport' content='width=device-width,initial-scale=1'>
            <body>
                <h1>TEST</h1>
                """
    html_counter = single_sheet_html_count(
        english_count, input1_count, input2_count, match_count)
    html_body = single_sheet_html_body(
        english_term_exists, no_match_list_input1_item, no_match_list_input2_item, terms_match)
    html_end = f"""
            </body>
        </html>"""
    return html_start + html_end


def single_sheet_html_count(english_count, input1_count, input2_count, match_count):
    html = f"""<div>
        <p>
                <ul>
                    <li>{input1_count}: Count of No Match - First Input</li>
                    <li>{input2_count}: Count of No Match - Second Input</li>
                    <li>{english_count}: Count of English Match - No Spanish Match</li>
                    <li>{match_count}: Count of English and Spanish Terms Match</li>
                </ul>
            </p>
    </div>"""
    return html

#DEBUG - This is not working


def single_sheet_html_body(english_term_exists, no_match_list_input1_item, no_match_list_input2_item, terms_match):
    table = "<table><tr><th>Input1-English</th><th>Input1-Spanish</th><th>Input2-English</th><th>Input-Spanish</th></tr>"
    for row in english_term_exists:
        term_row = f"""<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"""
        table = table + term_row
    table = table + "</table>"
    return table


def count_output_rows(output):
    return len(output)


input2_list = []
input1_list = []

for i in input1_initial:
    input1_list.append(i.split('\t'))
for i in input2_initial:
    input2_list.append(i.split('\t'))

# create empty variables to store results
terms_match = []
no_match_list_input1_item = []
no_match_list_input2_item = []
english_term_exists = []
last_english_term_input1_item = ''
last_english_term_input2_item = ''

# loop through each row in list1
for input1_item in input1_list:
    # assign value to last_english_term_cdc if current cdc value is non-empty.
    # otherwise do not change value of last_english_term_cdc
    if input1_item[0] != '':
        last_english_term_input1_item = input1_item[0]
    else:
        input1_item[0] = last_english_term_input1_item
    match_found = False
    # loop through each row in list2
    for input2_item in input2_list:
        # assign value to last_english_term_input2_item if current input2_item value is non-empty.
        # otherwise do not change value of last_english_term_input2_item
        if input2_item[0] != '':
            last_english_term_input2_item = input2_item[0]
        else:
            input2_item[0] = last_english_term_input2_item
        match_found = False
        # check if the first item in the row matches (this means there is a matching English term in each list)
        if input1_item[0] == input2_item[0]:
            # check if the second item in the row matches (This means there is a matching Spanish term in each list)
            if input1_item[1] == input2_item[1]:
                # if there is a match, add the row to the terms_match variable
                terms_match.append([input1_item[0], input1_item[1],
                                    input2_item[0], input2_item[1]])
                # break out of the loop through list2
                match_found = True
                break
            # else:
                # a = [input1_item[0], input1_item[1],
                #     input2_item[0], input2_item[1]]
                # english_term_exists.append(a)
                #match_found = True
                # break

    # if no match was found, add the row to the no_match_list variable
    if not match_found:
        a = [input1_item[0], input1_item[1], None, None]
        no_match_list_input1_item.append(a)

# Check for NIH terms that do not exist in CDC list
for input2_item in input2_list:
    match_found = False
    for input1_item in input1_list:
        if input1_item[0] != '':
            last_english_term_input1_item = input1_item[0]
        else:
            input1_item[0] = last_english_term_input1_item
        match_found = False
        # check if the first item in the row matches (this means there is a matching English term in each list)
        if input2_item[0] == input1_item[0]:
            # check if the second item in the row matches (This means there is a matching Spanish term in each list)
            if input2_item[1] == input1_item[1]:
                # Do not output this value as it has already been found in the first loop (compare input1 to input2)
                match_found = True
                break
    if not match_found:
        a = [None, None, input2_item[0], input2_item[1]]
        no_match_list_input2_item.append(a)

# count of each output variable
count_english_term_exists = len(english_term_exists)
count_no_match_list_input1 = len(no_match_list_input1_item)
count_no_match_list_input2 = len(no_match_list_input2_item)
count_terms_match = len(terms_match)

# print the results to screen
print("\n", "English Terms Exists In Both, Spanish Does Not Match:")
for row in english_term_exists:
    print(row)
print("Match count:", count_english_term_exists)

print("\n", input1_source, "English Term does not exist in", input2_source, ": ")
for row in no_match_list_input1_item:
    print(row)
print("No match count:", count_no_match_list_input1)

print("\nNIH English Term does not exist in CDC:")
for row in no_match_list_input2_item:
    print(row)
print("No match count:", count_no_match_list_input2)

print("\nEnglish and Spanish Terms Match:")
for row in terms_match:
    print(row)
print("Match count:", count_terms_match)

# headers
headers = ['CDC English', 'CDC Spanish', 'NIH English', 'NIH Spanish']

# names of files to write
English_Not_Spanish = output_dir + input1_source + '_' + \
    input2_source + '__' + 'EnglishMatchesNotSpanish.tsv'
CDC_English_Not_NIH_Spanish = output_dir + input1_source + '_' + input2_source + \
    '__' + input2_source + 'EnglishNot' + input1_source + 'Spanish.tsv'
CNIH_English_Not_CDC_Spanish = output_dir + input1_source + '_' + input2_source + \
    '__' + input1_source + 'EnglishNot' + input2_source + 'Spanish.tsv'
Terms_Match = output_dir + input1_source + \
    '_' + input2_source + '__' + 'TermsMatch.tsv'
MGT_Diff_Single_Sheet = output_dir + input1_source + '_' + \
    input2_source + '__' + 'MGTDiffSingleSheet.tsv'
MGT_Diff_Single_Sheet_HTML = output_dir + input1_source + '_' + \
    input2_source + '__' + 'MGTDiffSingleSheet.html'

# write the files
with open(MGT_Diff_Single_Sheet, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(
        ["Count of CDC English matches NIH English but not Spanish: ", count_english_term_exists])
    tsv_writer.writerow(
        ["Count of CDC English has no NIH English Match: ", count_no_match_list_input1])
    tsv_writer.writerow(
        ["Count of NIH English has no CDC English Match: ", count_no_match_list_input2])
    tsv_writer.writerow(
        ["Count CDC and NIH Terms that match Both English and Spanish: ", count_terms_match])
    for i in english_term_exists:
        a = ['1'] + i
        tsv_writer.writerow(a)
    for j in no_match_list_input1_item:
        b = ['2'] + j
        tsv_writer.writerow(b)
    for k in no_match_list_input2_item:
        c = ['3'] + k
        tsv_writer.writerow(c)
    for l in terms_match:
        d = ['4'] + l
        tsv_writer.writerow(d)

with open(English_Not_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_english_term_exists])
    for i in english_term_exists:
        tsv_writer.writerow(i)

with open(CDC_English_Not_NIH_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_no_match_list_input1])
    for i in no_match_list_input2_item:
        tsv_writer.writerow(i)

with open(CNIH_English_Not_CDC_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_no_match_list_input2])
    for i in no_match_list_input2_item:
        tsv_writer.writerow(i)

with open(Terms_Match, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_terms_match])
    for i in terms_match:
        tsv_writer.writerow(i)


with open(MGT_Diff_Single_Sheet_HTML, 'wt', encoding='utf-8', newline='') as file_out:
    html = single_sheet_html(english_term_exists, no_match_list_input1_item, no_match_list_input2_item, terms_match,
                             count_english_term_exists, count_no_match_list_input1, count_no_match_list_input2, count_terms_match)
    file_out.write(html)
