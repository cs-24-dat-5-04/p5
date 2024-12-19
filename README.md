# p5
University assignment generator
### Prerequisites
- VSCode
- Git
- Python
##### Install using [winget](https://www.microsoft.com/p/app-installer/9nblggh4nns1#activetab=pivot:overviewtab)
```
winget install Microsoft.VisualStudioCode
```
```
winget install Python.Python.3.12
```
```
winget install Git.Git
```

##### Install using [chocolatey](https://chocolatey.org/install)
```
choco install vscode
```
```
choco install python
```
```
choco install git
```

### Setup guide
1. Open your terminal where you want to install the project.
2. Type in the following command:
 ```git
 git clone https://github.com/cs-24-dat-5-04/p5
 ```
3. Open the **📁p5 folder** in VSCode
4. Install dependencies using `pip install -r requirements.txt`
5. Create the `secrets.json` file in the root of the project folder.
You will need an API key from OpenAI: https://platform.openai.com
The structure of the JSON file is as follows:
```json
{ 
    "csrf_token": "abc123",
    "organization": "org-HASH",
    "project": "proj_HASH",
    "api_key": "sk-proj-HASH"
}
```
6. Run the server using `flask run` and go to http://127.0.0.1:5000/

## Reading database
### Prerequisite
 - DB browser for SQlite
 1. download and install from https://sqlitebrowser.org/dl/.

### Running the database
 - Open DB browser
 - Press `Open database`
 - Navigate to the folder containing the database
 - Select the database file and press `Open`
 - Refresh in DB browser any time you change the DB in the code, in order to see updates
Alternatively, if you're running Linux, simply run this command in the project:
```sqlitebrowser database.db```

