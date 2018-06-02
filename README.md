# Latex_dia
Dia is free software to create diagram. Its striking feature are 1) having layer 2) access to various shapes 3) ability to export to many picture format, and 3) easy creation of custom shapes. However, it does not support text in superscript and subscript.

This is a python plugin for Dia to generates text with superscript and subscripts as images and places them in Dia sheet. The text can be modified and managed seamlessly. Additonally, it can be used to generate any math equation.

Requirements:
1) Dia with pyGtk (more information on how to cofigure is http://dia-installer.de/howto/python_win32/)
2) Latex installation

How to use:
1) Go to Dia > Dialogues > Python console
2) change the path in the code at line 153 to the location of your latex installation. For example:
      self.Miktex_path="C:\\"+""""Program Files"\\"MiKTeX 2.9"\\miktex\\bin\\x64\\"""
   if you are using linux
      change the binaries (latex.exe and dvipng.exe) in the lines 57-59 to the appropriate ones
    os.system(Miktex_path+"latex.exe -output-directory \""""+os.path.normpath(build_d)+"\" \""+os.path.realpath(out_file)+"\"")
    os.system(Miktex_path+"latex.exe -output-directory \""""+os.path.normpath(build_d)+"\" \""+os.path.realpath(out_file)+"\"")
    os.system(Miktex_path+"dvipng.exe -D 900 -bg Transparent -o \""""+os.path.realpath(out_file+".png")+"\" \""+os.path.realpath(out_file+".dvi")+"\"")

3) Copy the code in this python file and paste it in the command line of console and hit 'enter'.
4) Paste the following in commandline of console and hit enter
      dlg=LatexObjectDialog(dia.active_display().diagram, dia.active_display().diagram)

Help:
Add button to add a new text object to the plugin GUI
Preview button in the text object creates the typed text(as image) in the Dia
Delete button delete the text object from the plugin GUI and the corresponding text from Dia
Caution: You must delete the images created using this plugin using this plugin only. Otherwise it will corrupt the database


The code is tested on window 10 with latex compiler Miktex 2.9. But it should run on linux as well.

I am planning to add font size as well.
I would be working on this code. So, the development will be very slow.
I am not a programmer :). Excuse me for the shabby coding.

Hope you enjoy it and find it useful :)

