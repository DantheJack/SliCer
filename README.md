# SliCer
A semantic-based amorphous backward C slicer project

Give a piece of code in C,

Choose your variable,

Indicate a line,

Slice.


Or at least that's the idea... For the moment this project is only a demo version.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for testing purposes.

### Prerequisites

What you need to run this program on your personal computer:

- Windows would be desirable, since I cannot guarantee the proper functioning of the programs under another operating system.
- A recent version of [Python](https://www.python.org/downloads/) is required (version 3.5 or higher is recommended). 

*To check if a current version of Python is currently installed on your device, open Powershell and type `python --version`.*


### Installing

Getting the files

```
Download a clone of the project to your computer (~ 9 MB).
Extract the files.
Do not move nor remove any file from the deepest SliCer-master folder.
```

## Running the tests

Prior to any trial of the demo version, I suggest you to run the automated tests that I developped along this project.
This is how to run the automated tests for this system: 

### Using CLI

1. Open Powershell directly in the deepest SliCer-master folder (or, if you renamed it, the folder that contains the README file)
or move to this folder using `cd` command. Warning : you will need Admin rights into this command-line interface.

2. If you want to run the tests, you will need to download the pytest framework. To download it, run the following command in your CLI :
`pip install -U pytest`, then confirm the proper installation of pytest by typing `pytest --version`.

3. Execute the following command : `python -u ".\src\testLauncher.py"`, then press Enter.

4. You should see the following message :

```diff
+ 15 passed in ... seconds
```

If you see that message, you can then proceed to the next step. Otherwise, I strongly advise you to report to me this problem 
along with the error messages you get (or screenshots) so I can improve my software and solve the issue.

5. If you want to uninstall pytest, simply use the command `pip uninstall pytest`.

## Demo version

### Running the demo

#### Windows-only solution

If you are running this solution on Windows, you can simply double-left-click on Slicer.bat file.
It contains a one-line program that serves as a shortcut to launch the executable.

#### Multi-platform solution

Manualy move to the folder src\build\exe.win32-3.7 then use the executable file directly. You can also create a shortcut of
this .exe file and place it anywhere you want to your conveniance.

#### CLI-only solution

Open Powershell directly in the deepest SliCer-master folder (or, if you renamed it, the folder that contains the README file)
or move to this folder using `cd` command. Then executes the following command : `python -u ".\src\SliCer.py"`

### Understanding the demo



## Built With

* [Python](https://www.python.org/downloads/) - Python/Downloads
* [cx-Freeze](https://cx-freeze.readthedocs.io/en/latest/#) - Creation of executable
* [Tkinter](https://wiki.python.org/moin/TkInter) - Used to generate the Graphical User Interface

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Dan Lipskier** - *Thesis MSc Computing Sciences*

## License

~~This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details~~

## Acknowledgments

* Dr. Klaas-Jan Stol, for tutoring this project and guiding me with valuable advice.
* Louis-Paul Gausi, for his cyber-security skills and for giving me hope when all seemed lost.


