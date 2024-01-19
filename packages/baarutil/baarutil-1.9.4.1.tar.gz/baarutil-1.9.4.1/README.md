# BAARUtil

**Version: 1.9.4.1**

Minor Update - Contains enhancement.

Details: generate_password() function now has a new argument "include_chars" where the user can provide the list of characters among which at leas one must be included in the final password.

**This Custom Library is specifically created for the developers/users who use BAAR. Which is a product of [BAAR Technologies](https://www.baar.ai/) aka [Allied Media Inc](https://www.alliedmedia.com/).**

<h2>
Primary Author and Contributor:
</h2>

**Souvik Roy  [sroy-2019](https://github.com/sroy-2019)**

<h3>
Co-contributors:
</h3>

**Saikat Dey,**
**Debapriya Palai,**
**Avignan Nag**

<h2>
Installation:
</h2>

~~~
pip install baarutil
~~~

<h2>
Importing:
</h2>

~~~
import baarutil as bu
~~~

<h2>
Additional Info:
</h2>

The string structure that follows is a streamlined structure that the developers/users follow throughout an automation workflow designed in BAAR:
~~~
"Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h2>
Checking version:
</h2>

~~~
import baarutil as bu

version = bu.version()
~~~

<h2>
Table of Contents:
</h2>

1. [read_convert](#read_convert)
2. [write_convert](#write_convert)
3. [string_to_df](#string_to_df)
4. [df_to_string](#df_to_string)
5. [df_to_listdict](#df_to_listdict)
6. [decrypt_vault](#decrypt_vault)
7. [generate_password](#generate_password)
8. [generate_report](#generate_report)
9. [string_to_report](#string_to_report)
10. [clean_directory](#clean_directory)
11. [archive](#archive)
12. [download_chromedriver](#download_chromedriver)
13. [baarlocker](#baarlocker)
    1. [encrypt](#baarlocker_encrypt)
    2. [decrypt](#baarlocker_decrypt)
    3. [update](#baarlocker_update)
    4. [delete](#baarlocker_delete)


<h2>
Available functions and the examples are listed below:
</h2>

<h3>
</div id="read_convert">
1.  Function: read_convert(string), Output Data Type: list of dictionary<a name="read_convert"></a>
</h3>

**Attributes:**

  *i.  **string:** Input String, Data Type = String*

~~~
Input:  "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
Output: [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
~~~

<h3>
</div id="write_convert">
2.  Function: write_convert(input_list), Output Data Type: string<a name="write_convert"></a>
</h3>

**Attributes:**

  *i.  **input_list:** List that contains the Dictionaries of Data, Data Type = List*

~~~
Input:  [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
Output: "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h3>
</div id="string_to_df">
3.  Function: string_to_df(string, rename_cols, drop_dupes), Output Data Type: pandas DataFrame<a name="string_to_df"></a>
</h3>

**Attributes:**

  *i.  **string:** Input String, Data Type = String*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii.  **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

~~~
Input:  "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

Output:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>

<h3>
</div id="df_to_string">
4.  Function: df_to_string(input_df, rename_cols, drop_dupes), Output Data Type: string<a name="df_to_string"></a>
</h3>

**Attributes:**

  *i. **input_df:** Input DataFrame, Data Type = pandas DataFrame*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii. **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

Input:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>
  
~~~
Output: "Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world"
~~~

<h3>
</div id="df_to_listdict">
5.  Function: df_to_listdict(input_df, rename_cols, drop_dupes), Output Data Type: list<a name="df_to_listdict"></a>
</h3>

**Attributes:**

  *i. **input_df:** Input DataFrame, Data Type = pandas DataFrame*

  *ii. **rename_cols:**  Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *iii. **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

Input:
<table>
  <thead>
    <tr>
      <th>Column_1</th>
      <th>Column_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>abc</td>
      <td>def</td>
    </tr>
    <tr>
      <td>hello</td>
      <td>world</td>
    </tr>
  </tbody>
</table>

~~~
Output: [{"Column_1":"abc", "Column_2":"def"}, {"Column_1":"hello", "Column_2":"world"}]
~~~

<h3>
</div id="decrypt_vault">
6.  Function: decrypt_vault(encrypted_message, config_file), Output Data Type: string<a name="decrypt_vault"></a>
</h3>

**Attributes:**

  *i. **encrypted_message:** Encrypted Baar Vault Data, Data Type = string*

  *ii. **config_file:**  Keys, that need to be provided by [Allied Media](https://www.alliedmedia.com/).*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using the Decrypt Vault keyword. Upon initiation of this function, this will set the Log Level of the Robot Framework script to NONE for security reasons. The Developers have to use *Set Log Level    INFO* in the robot script in order to restart the Log.

~~~
Input:  <<Encrypted Text>>
Output: <<Decrypted Text>>
~~~

<h3>
</div id="generate_password">
7.  Function: generate_password(password_size, upper, lower, digits, symbols, exclude_chars, include_chars), Output Data Type: string<a name="generate_password"></a>
</h3>

**Attributes:**

  *i. **password_size:** Password Length, Data Type = int, Default Value = 10, (Should be greater than 4)*

  *ii. **upper:**  Are Uppercase characters required?, Data Type = Bool (True/False), Default Value = True*

  *iii. **lower:**  Are Lowercase characters required?, Data Type = Bool (True/False), Default Value = True*

  *iv. **digits:**  Are Digits characters required?, Data Type = Bool (True/False), Default Value = True*

  *v. **symbols:**  Are Symbols/ Special characters required?, Data Type = Bool (True/False), Default Value = True, Built-in available values: ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '\*', '(', ')', '<']*

  *vi. **exclude_chars:**  List of characters to be excluded from the final password, Data Type = List, Default Value = []*

  *vii. **include_chars:**  List of characters from which at least one must be included in the final password, Data Type = List, Default Value = []*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using Generate Password keyword. Upon initiation of this function, this will set the Log Level of the Robot Framework script to NONE for security reasons. The Developers have to use *Set Log Level    INFO* in the robot script in order to restart the Log.

~~~
Input (Optional):  <<Password Length>>, <<Uppercase Required?>>, <<Lowercase Required?>>, <<Digits Required?>>, <<Symbols Required?>>
Output: <<Password String>>
~~~

<h3>
</div id="generate_report">
8.  Function: generate_report(data_df, file_name, path, file_type, detailed_report, replace_old_file, final_file_name_case, time_stamp, encoding, index, engine, max_new_files_count, sheet_name), Output Data Type: Bool or, Dictionary (based on the input value of detailed_report)<a name="generate_report"></a>
</h3>

**Attributes:**

  *i. **data_df:** Input Dataframe, Data Type = pandas.DataFrame()*

  *ii. **file_name:** Final file name, Data Type = str*

  *iii. **path:** Final file path, Data Type = str, Default Value = Current working directory*

  *iv. **file_type:** Final file extension/ file type, Data Type = str, Default Value = 'csv', Available Options = 'csv' or, 'xlsx'*

  *v. **detailed_report:** Is detailed status of the run required?, Data Type = Bool (True/False), Default Value = False*

  *vi. **replace_old_file:** Should the program replace the old files after each run? or keep creating new files (only works if the final file name is the same each time), Data Type = Bool (True/False)*

  *vii. **final_file_name_case:** Font case of the final file name, Data Type = str, Default Value = 'unchanged', Available Options = 'upper' or, 'lower' or, 'unchanged'*

  *viii. **time_stamp:** Time stamp at the end of the filename to make each file unique, Data Type = Bool (True/False), Default Value = False*

  *ix. **encoding:** Encoding of the file, Data Type = str, Default Value = 'utf-8'*

  *x. **index:** Dataframe index in the final file, Data Type = Bool (True/False), Default Value = False*

  *xi. **engine:** Engine of the excelwriter for pandas to_excel function, Data Type = str, Default Value = 'openpyxl'*

  *xii. **max_new_files_count:** Count of maximum new files if the replace_old_file is False, Data Type = int, Default Value = 100*

  *xiii. **sheet_name:** Sheet name in the final excel, Data Type = str, Default Value = 'Sheet1'*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using Generate Report.

~~~
Input:  Mandetory arguments ->  data_df, file_name
Output (if detailed_report==False):  True/ False
Output (if detailed_report==True):  {'file_path': <<Absolute path of the newly generated file>>, 'file_generation_status': True/ False, 'message': <<Detailed message>>, 'start_time': <<Start time when the function was initiated>>, 'end_time': <<End time when the function was completed>>} 
~~~

<h3>
</div id="string_to_report">
9.  Function: string_to_report(data, file_name, path, file_type, detailed_report, replace_old_file, final_file_name_case, time_stamp, encoding, index, engine, max_new_files_count, sheet_name), Output Data Type: Bool or, Dictionary (based on the input value of detailed_report, rename_cols, drop_dupes)<a name="string_to_report"></a>
</h3>

**Attributes:**

  *i. **data:** Input BAAR string, Data Type = str*

  *ii. **file_name:** Final file name, Data Type = str*

  *iii. **path:** Final file path, Data Type = str, Default Value = Current working directory*

  *iv. **file_type:** Final file extension/ file type, Data Type = str, Default Value = 'csv', Available Options = 'csv' or, 'xlsx'*

  *v. **detailed_report:** Is detailed status of the run required?, Data Type = Bool (True/False), Default Value = False*

  *vi. **replace_old_file:** Should the program replace the old files after each run? or keep creating new files (only works if the final file name is the same each time), Data Type = Bool (True/False)*

  *vii. **final_file_name_case:** Font case of the final file name, Data Type = str, Default Value = 'unchanged', Available Options = 'upper' or, 'lower' or, 'unchanged'*

  *viii. **time_stamp:** Time stamp at the end of the filename to make each file unique, Data Type = Bool (True/False), Default Value = False*

  *ix. **encoding:** Encoding of the file, Data Type = str, Default Value = 'utf-8'*

  *x. **index:** Dataframe index in the final file, Data Type = Bool (True/False), Default Value = False*

  *xi. **engine:** Engine of the excelwriter for pandas to_excel function, Data Type = str, Default Value = 'openpyxl'*

  *xii. **max_new_files_count:** Count of maximum new files if the replace_old_file is False, Data Type = int, Default Value = 100*

  *xiii. **sheet_name:** Sheet name in the final excel, Data Type = str, Default Value = 'Sheet1'*

  *xiv. **rename_cols:** Dictionary that contains old column names and new column names mapping, Data Type = Dictionary, Default Value = {}*

  *xv. **drop_dupes:** Drop duplicate rows from the final dataframe, Data Type = Bool, Default Value = False*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using String To Report.

~~~
Input:  Mandetory arguments ->  data (BAAR String: Column_1__=__abc__$$__Column_2__=__def__::__Column_1__=__hello__$$__Column_2__=__world), file_name
Output (if detailed_report==False):  True/ False
Output (if detailed_report==True):  {'file_path': <<Absolute path of the newly generated file>>, 'file_generation_status': True/ False, 'message': <<Detailed message>>, 'start_time': <<Start time when the function was initiated>>, 'end_time': <<End time when the function was completed>>} 
~~~

<h3>
</div id="clean_directory">
10.  Function: clean_directory(path, remove_directory), Output Data Type: boolean<a name="clean_directory"></a>
</h3>

**Attributes:**

  *i. **path:** Absolute paths of the target directories separated by "|", Data Type = str*

  *ii. **remove_directory:**  Should the nested directories be deleted?, Data Type = Bool (True/False), Default Value = False*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using the Clean Directory keyword.

~~~
Input:  "C:/Path1|C:/Path2|C:/Path3"
Output: True/False
~~~

<h3>
</div id="archive">
11.  Function: archive(source, destination, operation_type, dynamic_folder, dynamic_filename, custom_folder_name_prefix, timestamp_format), Output Data Type: boolean & string<a name="archive"></a>
</h3>

**Attributes:**

  *i. **source:** Absolute source path, Data Type = str*

  *ii. **destination:** Absolute destination path, Data Type = str*

  *iii. **operation_type:** What type of operation?, Data Type = str, Default Value = 'cut', Available Options = 'cut' or, 'copy'*

  *iv. **dynamic_folder:** Should there be a folder created within the destination folder in which the archived files will be placed?, Data Type = Bool (True/False), Default Value = 'True'*

  *v. **dynamic_filename:** Should the files be renamed after being archived with a Timestamp as a Postfix?, Data Type = str, Data Type = Bool (True/False), Default Value = 'False'*

  *vi. **custom_folder_name_prefix:** What should be the name of the dynamic custom folder if the dynaimc_folder = True?, Data Type = str, Default Value = 'Archive'*

  *vii. **timestamp_format:** Format of the timestamp for the folder name/ file name postfixes, Data Type = str, Default Value = '%d-%m-%Y_%H.%M.%S', Available Options = any python datetime formats*

  This function can also be called from a Robot Framework Script by importing the baarutil library and using Archive keyword.

~~~
Input:  source="C:/Path1", destination="C:/Path2"
Output1 (completion_flag), Output2 (final_destination): True/False, "C:/Path2/Archive_24-02-2022_17.44.07"
~~~

<h3>
</div id="download_chromedriver">
12.  Function: download_chromedriver(path, version_number, base_url, file_name, connection_check_sub_url), Output Data Type: boolean<a name="download_chromedriver"></a>
</h3>

**Attributes:**

  *i. **path:** Target download directory for the Chromedriver executable, Data Type = str*

  *ii. **version_number:** The Version number of the Google Chrome installed in the target system, Data Type = str, Available Option = 'Latest' - (This will download the latest version of the Chromedriver), Default Value = 'Latest'*

  *iii. **base_url:** Base URL of Chromedriver repository, Data Type = str, Default Value = 'https://chromedriver.storage.googleapis.com'*

  *iv. **file_name:** Target Filename to Download, Data Type = str, Default Value = 'chromedriver_win32.zip'*

  *v. **connection_check_sub_url:** Sub-set of the URL that will be concatenated with the base_url to get the version of the latest available Chromedriver, Data Type = str, Default Value = 'LATEST_RELEASE'*

~~~
Input:  path="C:/Path1"
Output: True/False
Console Log (For successful operation):
Connection to the server Successful!

Chromedriver executable from Zip extracted!
Chromedriver of version XXXX Downloaded Successfully, in path: C:/Path1
~~~

<h3>
</div id="baarlocker">
13.   Class: baarutil.baarlocker.BaarLocker(tenant, api_key, username, env_var, custom_url_dict)<a name="baarlocker"></a>
</h3>

**Importing:**

~~~
import baarutil.baarlocker as baarlocker
~~~

**Attributes:**

  *i. **tenant:** BAAR Tenant Name, Data Type = str*

  *ii. **api_key:** The API Key to Communicate with BAAR API, Data Type = str*

  *iii. **username:** BAAR Username, Data Type = str*

  *iv. **env_var:** Environment Variable Name that contains BAAR Installation Path, Data Type = str, Default Value = 'BAAR_PATH'*

  *v. **custom_url_dict:** Dictionary that contains the custom set of URLs if not provided a fixed set of URLs will be used to connect to BAAR APIs, Data Type = str, Default Value = {}, supported keys: "create_url" => for encryption, "get_url" => for decrypt, "update_url" => for update, "delete_url" => for delete*

~~~
import baarutil.baarlocker as baarlocker

locker = baarlocker.BaarLocker(tenant="main_tenant", api_key="XXXXXXXX", username="john22", env_var="BAAR_PATH", custom_url_dict={})
~~~

<h4>
</div id="baarlocker_encrypt">
13.1 Function: locker.encrypt(data)<a name="baarlocker_encrypt"></a>
</h4>

**Attributes:**

  *i. **data:** Data that needs to be encrypted, Data Type = str*

~~~
Input: data="Test123"
Output: final_unique_id=<<Decryption ID/ Unique ID that can be later used to Fetch/Decrypt the same value i.e. "Test123">>, operation_status=True/False, detailed_message="Successfully Added !!"
~~~

<h4>
</div id="baarlocker_decrypt">
13.2 Function: locker.decrypt(id)<a name="baarlocker_decrypt"></a>
</h4>

**Attributes:**

  *i. **id:** Decryption ID or the UUID that was generated after using encrypt() function (final_unique_id), Data Type = str*

~~~
Input: id="XXXXXXXXXXXX"
Output: final_data=<<Decrypted Data>>, operation_status=True/False, detailed_message="Successfully Retrieved !!"
~~~

<h4>
</div id="baarlocker_update">
13.3 Function: locker.update(id, data)<a name="baarlocker_update"></a>
</h4>

**Attributes:**

  *i. **id:** Decryption ID or the UUID that was generated after using encrypt() function (final_unique_id), Data Type = str*

  *ii. **data:** Data that needs to be encrypted and replaced with the value with respect to the given Decryption ID, Data Type = str*

~~~
Input: id="XXXXXXXXXXXX", data="Secret123"
Output: final_unique_id=<<Decryption ID/ Unique ID that can be later used to Fetch/Decrypt the same value i.e. "Secret123">>, operation_status=True/False, detailed_message="Successfully Updated !!"
~~~

<h4>
</div id="baarlocker_delete">
13.4 Function: locker.delete(id)<a name="baarlocker_delete"></a>
</h4>

**Attributes:**

  *i. **id:** Decryption ID or the UUID that was generated after using encrypt() function (final_unique_id), Data Type = str*

~~~
Input: id="XXXXXXXXXXXX"
Output: final_unique_id=<<Decryption ID/ Unique ID using which the data got deleted and this id will become invalid>>, operation_status=True/False, detailed_message="Deleted Successfully !!"
~~~
