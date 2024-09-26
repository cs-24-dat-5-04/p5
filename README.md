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
4. Run `server.py` and go to http://127.0.0.1:5000/

## How to set up the Database
1. Open your terminal and head to the **📁database folder**.

2. Run `db_init.py` using Python to initiate and populate the database.

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