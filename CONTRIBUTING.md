## Contributing guidelines for DweebsEye API repository 
### Here are steps to take to start working on the project code

Before going further, please take time to watch this short video on [best practices for collaboration on GitHub](https://www.coursera.org/lecture/introduction-git-github/best-practices-for-collaboration-6MVzC?utm_source=link&utm_medium=page_share&utm_content=vlp&utm_campaign=top_button)

*Current Python version used is 3.8*

**On your first contribution:**

- [clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) the repo: `git clone https://github.com/Dweebs-Global/DweebsEye-API`
- make sure you have the current Python version installed and used for your virtual environment
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
- to work with Azure Functions make sure you have Visual Studio Code with [Azure Functions extension](https://docs.microsoft.com/en-us/azure/includes/media/functions-install-vs-code-extension/vscode-install-extension.png) and [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools) installed

working:
- to add a new function to the existing project (Function app): after opening the project in VS Code, [click Azure icon](https://docs.microsoft.com/en-us/azure/includes/media/functions-install-vs-code-extension/azure-functions-window-vscode.png) on the Side Bar on the left, choose the corresponding Local Project and click the ["Create Function" button](https://docs.microsoft.com/en-us/azure/azure-functions/media/functions-develop-vs-code/create-function.png)
- when creating Azure functions, add dependencies to requirements.txt (manually, no pip freeze) and install them with `pip install -r requirements.txt`
- try to have many small commits with small changes other than huge ones with many changes
- commit changes with meaningful messages (it helps you and the team in the future)
  - standard message after `git commit -m ` should be up to 50 characters long
  - if you have more information, use simple `git commit` command and add more detailed commit message with your editor as follows: 
  - the first line is usually a short description of changes (<=50 char.) followed by a blank line
  - then goes a detailed description of the changes (under 72 char. in each line)
  - the length is crucial for displaying the messages properly in logs

testing:
- write unit tests in **tests/** folder, test file names starting with **test_** + **function name** + .py ([check this](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#package-management))
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



### Further reference:
- [Getting started with Azure Functions in Python](https://www.scalyr.com/blog/azure-functions-in-python-a-simple-introduction/)
- [official Microsoft guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python) for Azure functions in Python
- [official GitHub documentation](https://docs.github.com/en)
- great [course on Git and GitHub](https://www.coursera.org/learn/introduction-git-github)


