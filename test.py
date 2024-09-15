import git

repo = git.Repo('/home/tony/Expense_tracker')
print(repo.branches)

# print(result.git.status())

print(repo.untracked_files)

files = [file.a_path for file in repo.index.diff(None)]

print(files)

repo.close()
