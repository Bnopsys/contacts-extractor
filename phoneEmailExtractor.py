# Lesson
import re, pandas as pd

def format_phone_number(phone_number):
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(' ', '')
    
    if phone_number.startswith('1 '):
        phone_number = phone_number[2:]
    
    if phone_number.startswith('1'):
        phone_number = phone_number[1:]

    pattern = re.compile(r'(\d{3})(\d{3})(\d{4})')
    formatted_number = pattern.sub(r'(\1) \2-\3', phone_number)

    return formatted_number


with open ('Contacts.txt', 'r') as e:
    file_contents = e.read()


contacts = {}
current_name = None
phone = None
email = None
df = pd.DataFrame()

lines = file_contents.splitlines()


phone_match = re.compile(r'''(
                           (1)?
                           (\d{3}|\(\d{3}\))
                           (\s|-|\.)?
                           (\d{3})
                           (\s|-|\.)?
                           (\d{4})
                           )''', re.VERBOSE)


email_match = re.compile(r'\w+@\w+\.\w+')

for line in lines:
    name_match = re.match(r'FN:(.*)', line)
    if name_match:
        current_name = name_match.group(1)
        phone = None
        email = None
        if current_name not in contacts:
            contacts[current_name] = {'Name': current_name, 
                                      'Phone No': None, 
                                      'Email': None}
    else:
        if phone_match.search(line):
            phone = phone_match.search(line).group(0) 
            if phone[0] == '1' or '(' not in phone:
                phone = format_phone_number(phone)

        if email_match.search(line):
            email = email_match.search(line).group(0)

    if current_name:
        if phone:
            contacts[current_name]['Phone No'] = phone
        if email:
            contacts[current_name]['Email'] = email

dict_list = []

for contact in contacts.values():
    dict_list.append(contact)
    
df = pd.DataFrame(data=dict_list)
df = df.sort_values(by='Name')
df = df.reset_index(drop=True)
print(df)
df.to_csv('output.txt',index=False)

