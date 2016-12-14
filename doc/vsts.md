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
1. If your repository is hosted on Github, go to the *Repository* tab, grand acces to your Github account, and choose your repository. If your code is hosted on VSTS you shouldn't need to change anything.

Here is what the build definition will look like:  
![](/doc/images/04.png)

### Provision and Train    

In this step we want to create a new resource group based on our ARM template and captured VM image. The ARM template contains a custom extension which will call our [extension.sh script](https://github.com/wbuchwalter/on-demand-training-cntk/blob/master/env/extension.sh). This script will install some dependencies, build a docker image, train our model, and upload the result to azure blob storage.
Create a new step *Azure Resource Group Deployment*. Set `Training-$(Build.BuildId)` as resrouce group name, this will allow to have multiple training in parallel. Choose a location with access to N-Series (South Central US for example). The template should be `env/template.json`, and override the template parameters with `-buildId $(Build.BuildId)`.


### Download Artifacts   

Next we want to download and publish our build artifacts (the result of our training) inside VSTS, that way we can easily find the results of every training that occured without having to dig in our Azure Blob Storage container.  
Create a *Powershell* step to download the artifacts.  
*Arguments*: `-buildId $(Build.BuildId)`  
*Script*: 
```Powershell
Param(
 [string]$buildId
)

$baseUri = "https://<your storage account>.blob.core.windows.net/output/"
$files = "model", "metrics.txt" , "model.ckp" 

New-Item -ItemType directory -Path .\out

Foreach($f in $files){
    $fileName = $baseUri + $buildId + "-" + $f
    $outFile = ".\out\" + $f 
   
    Invoke-WebRequest -Uri $fileName -OutFile $outFile
}
```

### Publish Artifacts  
Add a *Copy and Publish Build Artifacts* step.  
*Copy Root*: `out`  
*Contents*: `*`  
*Artifact Name*: `drop`  
*Type*: `Server`  

### Delete Resource Group  
We want to automatically delete our resource group once the training is done.  
Create a new *Azure Resource Group Deployment* step.  
*Action*: `Delete Resource Group`  
*Resource Group*: `Training-$(Build.BuildId)`


Finally, click on `Queue new build`.  
The build should take around 20 minutes to complete, you should then be able to see the result from the `artifact` tab of the build:  
![](/doc/images/05.png)
