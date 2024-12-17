desc:

given git or folder in the computer, 
1. read it and convert it into txt files.
- we need: problem, project_summary, related classes or functions to the problem, and project_structure.
2. make a summary of the project
3. make rag for all the project. each chunk is separated by empty lines. if theres no empty lines, need to think...



the model will be able to ask for specific file, and to get this file. (using tools)


issues: 
- if i exceed the context length
- if the model stoped to be loading

for tomorrow:
- generate a summary for the hole project, and its include to: 
- organize the files in folder, and 
- be able to read files with tools (because i assume people will enter in errors from the interpreter). 
- each file should have summary, (and divided into chunks?), embedding.


in the future: add more datasets of errors, of global problems, in case of this error.