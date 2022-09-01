# Burprunner

Tool to automate processes using burp professional with Jenkins pipeline.
###### Used technologies
- Burp Professional (version 2022.8.1)
- Django (version 4.1)
- Jenkins (version 2.346.3, Docker Image)

## Installation

### Burp
------------
It is necessary to upload the **burprunner_extension.py** file in the folder to burp as an extension.

Setting up the REST API
**User options -> Misc -> REST API,** then select the checkbox to start the service.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/burp_rest_api.png) </kbd>

Create 2 scan configs in burp for example
- Without Passive&Javascript
- Without Instrusive

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/burp_scan_config.png) </kbd>

### Django
------------
You can set up virtual environment.

    virtualenv venv
	source venv/bin/activate

For package installations.

    pip install -r requirements.txt

Migrate and Runserver.

    python manage.py migrate
	python manage.py runserver

### Jenkins
------------
Run and Pull Jenkins Docker Image

    $ docker run -p 8080:8080 --name jenkins --volume jenkins_data:/var/jenkins_home jenkins/jenkins:lts-jdk11

After running the command, jenkins image file is created.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_output.png) </kbd>

Go to **localhost:8080** and set up your jenkins configurations with the **secret key** given from terminal

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_secret_key.png) </kbd>

A few jenkins plugins need to be installed.

- Blue Ocean
- Http Request Plugin
- Pipeline Utility Steps

Then we create a new pipeline item, select the **This project is parameterized** and define the following fields.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_parameter.png) </kbd>

- **String Parameter** (Name: *host*, Default Value: *http://localhost:5001/*, Description: *Define your scanning host*)

- **String Parameter** (Name: *headers*, Default Value: *Authorization=Bearer TestToken&Cookie=XXX*, Description: *Define your custom headers*

- **Choice Parameter** (Name: *Scan Config*, Choices:*FullScan, Without Passive&Javascript, Without Instrusive*, Description: *Define scan config*)

- **Boolean Parameter** (Name: *keepInJenkins*, Set by Default: *True*, Description: *keep artifact in jenkins*)

- **Boolean Parameter** (Name: *sendTeams*, Set by Default: *False*, Description: *send teams notification*)

- **Boolean Parameter** (Name: *sendSlack*, Set by Default: *False*, Description: *send slack notification*)

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_scripts.png) </kbd>

Copy the contents of the Jenkinsfile to the script in the pipeline and click the Save.

## Usage

Edit the environment variables in the Jenkins script.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_env_fields.png) </kbd>

- SPECIAL_HEADER (parameter name in url of added custom headers)
- CALLBACK_URL (django service for callback)
- TEAMS_HOOK_URL (You can use teams channel for notifications. The webhook url need)
- SLACK_HOOK_URL (You can use slack channel for notifications. The webhook url need)

After the environment variables definitions, we come to the pipeline we created and click Build with Parameters. We define the variables here and click build.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/jenkins_scan_config.png) </kbd>

- host (Target Scan URL)
- burp_host (Burp REST Api Node -> url:port)
- headers (Custom Headers -> Cookie, Authorization etc.)
- keepInJenkins (Keep artifact about scan in jenkins)
- scan_config (Choose active scan configuration)
- sendTeams (Send notify after scan)
- sendSlack (Send notify after scan) -> This 2 fields are parallel in pipeline

While the pipeline is being built, the entered configurations are sent to burp, active scan starts. Later, burp sends the vulnerabilities it finds to django, which we raise, via the callback url.

The system use **blue ocean** to examine the pipeline more easily.

<kbd> ![](https://github.com/sametgenc/burprunner/blob/master/images/blue_ocean.png) </kbd>

We can see the scans started by jenkins on the burp dashboard.

<kbd> ![0](https://github.com/sametgenc/burprunner/blob/master/images/burp_dashboard.png) </kbd>

Also see the scans details at django 

<kbd> ![0](https://github.com/sametgenc/burprunner/blob/master/images/django_scan_details.png) </kbd>

If the send Teams or send Slack variables are selected in the pipeline, the scan result is sent to the relevant channels.

<kbd> ![0](https://github.com/sametgenc/burprunner/blob/master/images/slack_notify.png) </kbd>
<kbd> ![0](https://github.com/sametgenc/burprunner/blob/master/images/teams_notify.png) </kbd>

Html report is created when you go to the /scans/scans/{jenkins_build_id} url from the django interface.

<kbd> ![0](https://github.com/sametgenc/burprunner/blob/master/images/html_report.png) </kbd>


