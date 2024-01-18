from os import system

def AddLineToText(text, line):
    return text + f"{line}\n"

def ConvBatToPyContents(BatContents: str) -> str:
        IsImportedBools: dict = {
            "os": False,
            "sys": False,
            "subprocess": False,
        }
        PyContents: str = """"""
        Lines = BatContents.splitlines()
    # Stripping down the lines
        Lines = {item.strip() for item in Lines}
        FinalLines: list[str] = []
    # Remove \n from list
        for Line in Lines:
            if Line == "\n":
                continue
            FinalLines.append(Line)

    # Loop through finalized lines
        for line in FinalLines:
        #Imports required modules if not already imported.
            if not IsImportedBools["os"]: PyContents = AddLineToText(PyContents, "import os"); IsImportedBools["os"] = True
            if not IsImportedBools["sys"]: PyContents = AddLineToText(PyContents, "import sys"); IsImportedBools["sys"] = True
            if not IsImportedBools["subprocess"]: PyContents = AddLineToText(PyContents, "import subprocess"); IsImportedBools["subprocess"] = True
            if line == "":
                continue
            # Cd command
            if line.startswith("echo") and not '>>' in line:
                start_index = line.find("echo") + 5
                PyContents = AddLineToText(PyContents, f'print("{line[start_index:]}")')

            elif line.startswith("cd"):
                line = line.replace("/", "\\\\")
                PyContents = AddLineToText(PyContents, f'os.system("{line}")')

            #elif line.startswith("start"):
                #start_index = line.find("start") + 6
                #PyContents = AddLineToText(PyContents, f'subprocess.call(["start", "{line[start_index:]}"])')

            else:
                PyContents = AddLineToText(PyContents, f'os.system("{line}")')

        return PyContents