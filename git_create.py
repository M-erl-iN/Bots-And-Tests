import os

dir_path = input()
dir_path = [i for i in os.listdir() if i.startswith(dir_path)][0]
print(dir_path)
command_list = [
    f"cd {dir_path}" "git init",
    "git add .",
    'git commit "final"',
    f'git remote add origin "{dir_path}"',
    "git branch -M main",
    "git push -u origin main",
]

for command in command_list:
    os.system(command)
