import csv
# open .tsv file(s)

# DEBUG
# probably need to rename all the agency specific elements to something generic

#nih_initial = open('NIH_testing.tsv', encoding='utf-8').read().split('\n')
input2_initial = open('C:\GitHub\markXLIX.github.io\MGT\SSA English-Spanish.tsv',
                      encoding='utf-8').read().split('\n')
input1_initial = open('C:\GitHub\markXLIX.github.io\MGT\CDC_testing.tsv',
                      encoding='utf-8').read().split('\n')
# Pandas caused type errors due to identifying some content as integer rather than string.
# Obviously can fix this but decided to just get it working as a normal list
# Probably just required encoding on read.  will have to test if time permits.
# Might be able to use the Google API to do this all within Google Sheets (without manual TSV export/import)
#cdc_list = pd.read_csv('CDC_testing.tsv', sep='\t', header=None)
#nih_list = pd.read_csv('NIH_testing.tsv', sep='\t', header=None)

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
input1_counter = 0
input2_counter = 0

# loop through each row in list1
for input1_item in input1_list:
    nih_counter = 0
    # assign value to last_english_term_cdc if current cdc value is non-empty.
    # otherwise do not change value of last_english_term_cdc
    if input1_item[0] != '':
        last_english_term_input1_item = input1_item[0]
    else:
        input1_item[0] = last_english_term_input1_item
    match_found = False
    # loop through each row in list2
    for input2_item in input2_list:
        # assign value to last_english_term_nih if current nih value is non-empty.
        # otherwise do not change value of last_english_term_nih
        if input2_item[0] != '':
            last_english_term_input2_item = input2_item[0]
        else:
            input2_item[0] = last_english_term_input2_item
        match_found = False
        # check if the first item in the row matches
        if input1_item[0] == input2_item[0]:
            # check if the second item in the row matches
            if input1_item[1] == input2_item[1]:
                # if there is a match, add the row to the match_list variable
                a = [input1_item[0], input1_item[1],
                     input2_item[0], input2_item[1]]
                terms_match.append(a)
                # break out of the loop through list2
                match_found = True
                del input2_list[input2_counter]
                break
            else:
                a = [input1_item[0], input1_item[1],
                     input2_item[0], input2_item[1]]
                english_term_exists.append(a)
                match_found = True
                del input2_list[input2_counter]
                break
        input2_counter += 1
    # if no match was found, add the row to the no_match_list variable
    if not match_found:
        a = [input1_item[0], input1_item[1], input2_item[0], input2_item[1]]
        no_match_list_input1_item.append(a)
    input1_counter += 1

# Check for NIH terms that do not exist in CDC list
for input2_item in input2_list:
    match_found = False
    for input1_item in input1_list:
        if input2_item[0] == input1_item[0]:
            match_found = True
            break
    if not match_found:
        a = ["", "", input2_item[0], input2_item[1]]
        no_match_list_input2_item.append(a)

# count of each output variable
count_english_term_exists = len(english_term_exists)
count_no_match_list_input1 = len(no_match_list_input1_item)
count_no_match_list_input2 = len(no_match_list_input2_item)
count_terms_match = len(terms_match)

# print the results to screen
print("\nCDC English Terms Exists, Spanish Does Not Match:")
for row in english_term_exists:
    print(row)
print("Match count:", len(english_term_exists))

print("\nCDC English Term does not exist in NIH:")
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

# names of files to write to
English_Not_Spanish = 'EnglishNotSpanish.tsv'
CDC_English_Not_NIH_Spanish = 'CDCEnglishNotNIHSpanish.tsv'
CNIH_English_Not_CDC_Spanish = 'CNIHEnglishNotCDCSpanish.tsv'
Terms_Match = 'TermsMatch.tsv'
MGT_Diff_Single_Sheet = 'MGTDiffSingleSheet.tsv'

# write the TSV files
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
