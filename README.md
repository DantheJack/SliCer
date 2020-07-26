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

- Download a clone of the project to your computer (~ 9 MB).
- Extract the files.
- Do not move nor remove any file from the deepest **SliCer-master** folder.

## Running the tests

Prior to any trial of the demo version, I suggest you to run the automated tests that I developped along this project.
This is how to run the automated tests for this system: 

### Using CLI

1. Open Powershell directly in the deepest **SliCer-master** folder (or, if you renamed it, the folder that contains the **README.md** file)
or move to this folder using `cd` command. *Warning : you will need Admin rights into this command-line interface.*

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

If enabled, Windows Defender may have the intuition to warn you about the unknown source of this software. I would like to assure you
that all precautions have been taken to ensure the reliability and harmlessness of this program to your device.

***Windows-only solution***

If you are running this solution on Windows, you can simply double-left-click on **Slicer.bat** file.
It contains a one-line program that serves as a shortcut to launch the executable.
If a message such as *"Windows protected your PC"* appears, you can decide to ignore it by clicking on `More info` then `Run anyway`.

***Another solution***

Manualy move to the folder **src\build\exe.win32-3.7** then use the executable file directly. You can also create a shortcut of
this **SliCer.exe file and place it** anywhere you want to your conveniance.

### Understanding the demo

Once the program is launched, you should be presented with a window containing the main user interface of the system. To the left of this interface is the place to write (or copy and paste) the code you want to slice.

*Don't forget to specify the line and variable you want as slicing criterion in the top right corner of the window!*

Once you click on "**Slice!**", the same code will appear in the right tab. If you have checked the option at the top left of the window, the code will appear in black, with the lines that contain elements belonging to the slice in red. Otherwise, only the relevant lines will appear.

Warning: The lines will be highlighted **ALL IN FULL**. This means that if you code your entire program on one line, the whole line will appear in red.

Highlighted lines are those that **contain elements** of the requested slice. It's up to you not to write everything on one line, or else to know how to differentiate the significant elements from the others.

Finally, the best way to learn how to use this tool is to write a few lines of code in C (*remember not to use IF/ELSE in this demo version!*) and test it by yourself.

Good Luck, and do not hesitate to contact me if you're encountering a problem with SliCer!

## Built With

* [Python](https://www.python.org/downloads/) - Python/Downloads
* [cx-Freeze](https://cx-freeze.readthedocs.io/en/latest/#) - Creation of executable
* [Tkinter](https://wiki.python.org/moin/TkInter) - Used to generate the Graphical User Interface

## Authors

* **Dan Lipskier** - *Thesis MSc Computing Sciences*

## License

~~This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details~~

## Acknowledgments

* Dr. Klaas-Jan Stol, for tutoring this project and guiding me with valuable advice.
* Louis-Paul Gausi, for his cyber-security skills and for giving me hope when all seemed lost.


