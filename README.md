# Write Up on Contacts Extractor Project

#### The goal of this project was to take my contacts(apple) and convert them to database format which is easier to read. 

## Steps:
### 1. Open file
```python
with open ('Contacts.txt', 'r') as e:
    file_contents = e.read()
```
This code uses `with open` to open the Contacts.txt file. Then by adding `'r'` and specifying to `read()` we open the file and read the contents. Currently the file looks like this:
```
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//iPhone OS 17.0.3//EN
N:Lomas;;;;
FN:Lomas
TEL;type=pref:+13046103252
END:VCARD
```
### 2. Compile Regular Expressions
The next step is to make our regular expressions. The definition of a "Regex" is: **A regular expression (or RE) specifies a set of strings that matches it**. By using the module RE we create expressions that can be searched through text to find matches. 
```python
phone_match = re.compile(r'''(
                           (1)?
                           (\d{3}|\(\d{3}\))
                           (\s|-|\.)?
                           (\d{3})
                           (\s|-|\.)?
                           (\d{4})
                           )''', re.VERBOSE)


email_match = re.compile(r'\w+@\w+\.\w+')
```

Both variables use the `re.compile` function to search in text for the provided expression. Lets break down the email match expression:
1. `r''`: This stands for raw text. It is the recomended way to store expressions. For normal letters or numbers it isnt an isue but when using characters like *^!@#$%&** they wouldnt work as intended. Thats why we can use raw text to specify either literal or special characters.
2. `\w+`: This is an example of using special characters. The \w+ isnt searching for '\w' but for any number of alphanumeric characters. Adding on to this, the '+' specifies it could be any number of characters from a-Z and 0-9. 
3. `@`: This is a character that doesn't have any extra functions with the RE module so we dont have to specify a literal character at the beginning. It will just search for an '@' in the given line.
4. `\.`: The period has extra functions so it has to be specified as a literal. It matches all characters except for the newline (\n). An example for the .dot is `r'FN:(.*)'`, it would match all characters starting with 'FN:'. In the context of the project this could be used to find the first name specified from the apple contacts file. Even if someone has multiple first names it would return all characters until the end of the line. **But in this instance** we just use it for its utility to separate email providers and their 'dot com'.
* <sub>The phone compiler uses the re.VERBOSE method to allow it to span across multiple lines.</sub>
### 3. Iterate over lines in file searching for:
* Names: `name_match = re.match(r'FN:(.*)', line)`
    - Unlike the previous two compiles, this is a all in one function. It compiles the search and then scans the line. 
* Phone Numbers: `phone = phone_match.search(line).group(0)`
    - As seen in step two with the verbose phone compiler, this uses the 0th group or the complete group and returns that. The other groups would contain the differnt parts of a phone number like the Area Code, first-three etc.
* Email Addresses: `email = email_match.search(line).group(0)`
    - The `.search` function scans text for the first instance of a match.
### 4. Take matches and save to dictionary
The flow of the code starts by identifying a name and after that point it searches for phone numbers and emails. First lets go through the name portion:
```python
if name_match:
        current_name = name_match.group(1)
        phone = None
        email = None
        if current_name not in contacts:
            contacts[current_name] = {'Name': current_name, 'Phone No': None, 'Email': None}
```
1. Line 1: This is a boolean function that looks for if a result is found from the regex search.(Note: when results aren't found the Nonetype is returned.)
2. Line 2: This line sets the name match as the current name.
3. Lines 3-4: These two lines set the current phone number and email as variables.
4. Lines 5-7: By using an if statement, we can evaluate if the current number is already in the contacts dictionary. Then if the conditions are met we set a new key value pair of the current name equal to a name, phone number and email. This is done with nested dictionarys so we can grab the values later for our database.
* That's how we save names to dictionary, next we will go over the remaining matches.

```python
if current_name:
        if phone:
            contacts[current_name]['Phone No'] = phone
        if email:
            contacts[current_name]['Email'] = email
```
1. Line 1 `if current_name`: Just like with the name match we start it off by evaluating the boolean value of if a match was found.
2. Lines 2-5: These lines evalueate boolean values for phone and email matches. Then the value is set inside of the contacts dictionary specified inside of the current name and the match type.
### 5. Append values from dictionary to list
The code below shows how we extract the subdictionary to be used for the final product. As it goes through every contact in the contact list it appends the corresponding value in the list. So for example the key value pair in contacts would be Name: {Name, Phone Number, Email}. The use of duplicate names is because the key name is like a label on the outside of a box. Whats important are the contents inside of the box rather than the box itself.
```python
dict_list = []

for contact in contacts.values():
    dict_list.append(contact)
```
### 6. Using Pandas Dataframe function, export to txt file
Pandas is a module in python that brings tons of database functionality. In this instance, I used `pd.Dataframe` to initilize a pandas dataframe and add the list from above as the column/data cells. Then we sort the names in ascending order and reset the index values so they dont look random. Lastly the dataframe is sent to the file output.txt
```python
df = pd.DataFrame(data=dict_list)
df = df.sort_values(by='Name')
df = df.reset_index(drop=True)
df.to_csv('output.txt',index=False)
```

### 7. Finishing touches
#### Phone Number Formatting
One issue with the code was that it was vulnerable to different formats of phone numbers. The code looks for 3 main types but in the case of any other exceptions it would return in an unintended way. To fix this, I chose to focus on extracting the digits from phone numbers and format afterwards to erase this vulnerability. Below shows the different formats:
* (123) 123-1234
* +11231231234
* 123-123-1234
##### Function
Writing a function to fix this problem achieves two goals: Prevent bugs, Make the code cleaner. As explained above, by writing the code this way we prevent formatting errors in the future since this code would work for any phone number as long as it has the required digits. Secondly, it makes the code cleaner since we removed the added functionality from the main loop and moved it to a function.
```python
def format_phone_number(phone_number):
    
    if len(phone_number) == 11:
        phone_number = phone_number[1:]

    pattern = re.compile(r'(\d{3})(\d{3})(\d{4})')
    formatted_number = pattern.sub(r'(\1) \2-\3', phone_number)

    return formatted_number
```# contacts-extractor
# contacts-extractor
# contacts-extractor
# contacts-extractor
# contacts-extractor
# contacts-extractor
