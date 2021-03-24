## Contributing guidelines for DweebsEye API repository 
###Here are steps to take to start working on the project code

Before going further, please take time to watch this short video on [best practices for collaboration on GitHub](https://www.coursera.org/lecture/introduction-git-github/best-practices-for-collaboration-6MVzC?utm_source=link&utm_medium=page_share&utm_content=vlp&utm_campaign=top_button)

**On your first contribution:**

- [clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) the repo: `git clone https://github.com/Dweebs-Global/DweebsEye-API`
- create a virtual environment (.venv/) and activate it
- in your virtual environment install the project requirements:
`pip install -r requirements.txt`
  
**Always:**

setting up:
- make sure you have the latest code from the *origin/main* branch in your *main* branch with `git pull origin main`
- create a [new branch](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-branches) for a new feature/issue locally with a name related to the feature/issue: `git checkout -b <your-branch-name>`
- if there were changes on the remote *main branch* in GitHub while you're working on your new branch, follow these steps:
  - pull remote changes to your *main branch*:
    - `git checkout main`
    - `git pull origin main`
  - merge those changes onto your current branch like this:
    - `git checkout <your-branch>`
    - `git merge main`
- make sure to have **.github/workflows/main.yml** in the root folder on your new branch (to trigger GitHub Action which runs the workflow)

working:
- commit changes with meaningful messages, try to have many small commits other than a huge one
- add dependencies to requirements.txt (manually, no pip freeze) and install them with `pip install -r requirements.txt`

testing:
- write unit tests in **tests/** folder, test file names starting with **test_** + **function name** + .py
- create empty **__init__.py** in **tests/** for tests to run correctly
- use [unittest](https://docs.python.org/3/library/unittest.html) or [pytest](https://docs.pytest.org/en/stable/) to run the tests (install with `pip install pytest`; run with `pytest` command)

committing:
- if tests run successfully, push changes to a new remote branch (never to the main branch!), call it like your local one:
`git push origin <your-branch-name>`
- in GitHub repo push the green button **Compare and pull request**; if there are no merge conflicts, open a [Pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests); otherwise try to [resolve conflicts](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/addressing-merge-conflicts)
- in the pull request description add **fixes #1** with the corresponding issue number instead of **1** (this way the issue will be automatically closed once the PR is merged)

following up:
- after your PR is merged, checkout your main branch and pull the changes from the origin/main to have the latest code
- next time you want to contribute, create a new branch from the *main* branch (again, first make sure you have the latest code from the *origin/main* branch in your *main* branch)



**Further reference:** 
- [official GitHub documentation](https://docs.github.com/en)
- great [course on Git and GitHub](https://www.coursera.org/learn/introduction-git-github)
- [official Microsoft guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python) for Azure functions in Python

