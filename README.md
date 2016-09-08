# WebHawk - A Webhook Microframework

## What is WebHawk?
WebHawk is a simple micro-framework which helps you create webhooks for Continuous Deployment of your Bitbucket/Github hosted projects.


## What's in the box?
WebHawk comes with:

1. A RESTful API which exposes the WebHook Endpoints
2. Command line tool to trigger Build-Tasks manually
3. Support for git Repositories
4. Support for [Bitbucket WebHooks](https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html)


WebHawk **does not** come with:

1. WebUI to create the build descriptions (called Recipes).
2. Support for svn, mercurial, or other VCS.
3. Support for git events other than PUSH.


WebHawk also comes with a few _secondary features_:

1. It's easy to extend; with a bit of coding you can add support to other VCS systems and/or WebBased VCS hosting services.
2. It can run the builds on a different server than the one it runs on.


## How does it work?

WebHawk implements a RESTful API which is capable of reading POST payloads from BitBuckt (and soon Github).

Then:

1. Translates the payload into a build task and spawns a builder.
2. Reads a corresponding build recipe.
3. Checks out your git project.
4. Launches the build command.
5. That's it really.

## What do I need to get started?

You need:

1. The project you want to build hosted on Bitbucket (and soon Github)
2. A public-facing server with the following pre-installed:
    1. Python 2.7
    2. [pip](https://pypi.python.org/pypi/pip)
    3. (optionally) SSH
3. A tiny bit of configuration


## How do I get started?

You basically need to perform three major actions:

1. Prepare your Recipe file
2. Start WebHawk
3. Create your webhooks on Bitcubket or Github  


### 1. Prepare your recipe file

The recipe file is a [yaml](http://yaml.org/) file that contains information on what should WebHawk do when it receives a payload.

Here's an example:

```
#
# WebHawk Recipies Configuration File
#
myapp-dev:
  repository:
    name: myapp
    branch: dev
    url: "git@bitbucket.org:stek.io/website.git"
    vcs: git
  command: "python ./bin/fabfile.py -f -s -a build"
```

The example above contains 1 Recipes with ID "myapp-develop" which specifies the details of a **Repository** and the build command.
Few things you need to consider:

* The Repository defines 4 properties: name, branch, url and the vcs (Version Control System)
* The Name, the Branch and the URL must be the same as your project in Bitbucket.
* You do not specify an SSH Key in the Recipe, but **you must configure your ~/.ssh/config** if the Repository is exposed via SSH.
Read [this article](https://confluence.atlassian.com/bitbucket/configure-multiple-ssh-identities-for-gitbash-mac-osx-linux-271943168.html) for more details.

A very important configuration is the `command`. As you may have guessed, this is the command that will be executed on a shell **after** your project is checked out.
The command always runs from inside the root directory of your project. This means that you can either choose to invoke a script that comes with your project,
or a script that you have placed somewhere else on the build server.

For example, you could upload a script on `/home/steve/scripts/build_website.sh` and setup a recipe like this:
```
mywebsite:
  repository:
    name: acme-website
    branch: master
    url: "git@bitbucket.org:acme.online/acme-website.git"
    vcs: git
  command: "/home/steve/scripts/build_website.sh ./"
```

Although the directory which WebHawk checks out your project is different everytime
(WebHawk creates a directory with a random name before checking out code), it ensures that the build command will run from within your project's directory.

After you have created your Recipe file with your Recipes, proceed to the next step.

### 2. Start WebHawk

Before you start WebHawk, you need to bootstrap the environment. The following command will setup a Python Virtual Environment and install all python libraries:
```
$ ./bin/bootstrap.sh
```

To activate this environment on your console, run:
```
$ source webhawk-venv/bin/activate
```

When the virtual env is active, you will see your prompt changing into something like this:
```
(webhawk-venv)dimi@Neutron~/workspaces/webhawk$ 
```

Tip: You can always exit the virtual environment by typing the command ```deactivate``` on your console.


Now you can start WebHawk with two ways:

1. Using the `start.py` script which starts a single threaded WebServer. This should be enough for a single project and a small team.
2. Using [gunicorn](http://gunicorn.org/) which scales much better when you have many Recipes and many triggers via webhooks.
 
#### 2.1 Using start.py

If you have your **webhawk-venv** Python Environment activated, simply run: ```$ ./webhawk/start.py``` within the project root directory.

You will see something like this on your console:
```
2016-09-08 16:46:53,780 - webhawk         - 19407 - INFO   - === WebHawk Services Starting ===
2016-09-08 16:46:53,789 - webhawk         - 19407 - INFO   - Loading Recipes from file 'config/recipes.yaml'
2016-09-08 16:46:53,789 - webhawk         - 19407 - INFO   - Initializing Git VCS Managers
2016-09-08 16:46:53,789 - webhawk         - 19407 - INFO   - Initializing Builder
2016-09-08 16:46:53,791 - webhawk         - 19407 - INFO   - WebHawk RESTful API Initiated
2016-09-08 16:46:53,796 - werkzeug        - 19407 - INFO   -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

#### 2.2 Using gunicorn
TBD

### 3. Setup Webhooks on your Project hosting service.
TBD

# License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.