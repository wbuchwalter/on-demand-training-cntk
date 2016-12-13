If you don't already have a VSTS account, you can create one [here](www.visualstudio.com).

### Create a new project
Create a new VSTS project, choosing git as the version control.

### Upload the code
You can choose to host your code on Github, VSTS or any other git provider.  
Just change the remote url (with `git remote set url origin <repo-url>`) or add a new remote (`got remote add <remote-name> <remote-url>`) from your clone of this repository.   
`git push <remote-name> master` to update your new repo.

### Create a new build definition 
A build definition describes the logical steps we want to automate.  
Click on `Builds & Release > Builds > + New`  

1. Choose an empty build definition.
1. Choose the repository source
1. Don't check Continuous Integration (unless you are rich and want to spin up a GPU VM every time there is new commit)
1. If your repository is hosted on Github, go to the `Repository` tab, grand acces to Github, and choose your repo. If your code is hosted on VSTS you shouldn't need to change anything.
