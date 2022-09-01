pipeline {
    agent any

    environment {
        SCAN_NUMBER = sh(script: "echo `date +%Y%m%d%H%M`", returnStdout: true).trim()
        SCAN_URL = "${params.host}"
        SPECIAL_HEADER = "custom_headers"
        BURP_HOST = "${params.burp_host}"
        CALLBACK_URL = "http://localhost:8000/scans/scans/$BUILD_NUMBER"
        SCAN_LOCATION = ""
        SLEEP_TIME = "5"
        SCAN_CONFIG = "${params.scan_config}"
        TEAMS_HOOK_URL = "https://teams.webhook.office.com/webhookb2/"
        SLACK_HOOK_URL = "https://hooks.slack.com/services/"
    }

    stages {
        stage('Generate Scan URL') {
            steps {
                script {
                    if (params.headers) {
                        String ENCODED_HEADERS = sh(script: "echo -n \"${params.headers}\" | base64", returnStdout: true).trim()

                        if (SCAN_URL.contains("?")) {
                            SCAN_URL = "${SCAN_URL}&${SPECIAL_HEADER}=${ENCODED_HEADERS}"
                        } else {
                            SCAN_URL = "${SCAN_URL}?${SPECIAL_HEADER}=${ENCODED_HEADERS}"
                        }

                    }
                    println("${SCAN_URL}")
                }
                sh "echo -n \"${params.headers}\" | base64"
            }
        }

        stage('Run Active Scan') {

            environment {
                def body = "{\"scan_callback\":{\"url\":\"${CALLBACK_URL}\"}, \"scan_configurations\":[{\"name\":\"${SCAN_CONFIG}\",\"type\":\"NamedConfiguration\"}], \"urls\":[\"${SCAN_URL}\"]}"
            }

            steps {
                script {
                    println(body)
                    def response = httpRequest consoleLogResponseBody: true, acceptType: 'APPLICATION_JSON', contentType: 'APPLICATION_JSON', httpMode: 'POST', requestBody: body, url: "${BURP_HOST}/v0.1/scan"
                    SCAN_LOCATION = response.headers['Location'][0]
                    // SCAN_LOCATION = sh(script: "curl --silent -igw '\n' -X POST '${BURP_HOST}/v0.1/scan' -d '{\"urls\":[\"${SCAN_URL}\"]}' | grep -i location | sed -r 's/[lL]ocation: //'", returnStdout: true).trim()
                }
            }
        }

        stage('Wait Until To Succeed') {
            when {
                expression {
                    params.keepInJenkins == true
                }

            }

            steps {
                script {
                    while (true) {
                        def response = httpRequest url: "${BURP_HOST}/v0.1/scan/${SCAN_LOCATION}"
                        def content = readJSON text: response.content
                        if(content['scan_status'] == "succeeded") {
                            break
                        }
                        sh "sleep ${SLEEP_TIME}"
                    }

                    def response = httpRequest url: "${BURP_HOST}/v0.1/scan/${SCAN_LOCATION}"
                    writeFile(file: "burp-${SCAN_NUMBER}-${SCAN_LOCATION}.json", text: response.content)
                }
            }
        }

        stage('Send notifications'){
            parallel{
                stage('Send Teams Notifications'){
                    when {
                        expression {
                            params.sendTeams == true
                        }
                    }
                    steps{
                        script{
                            httpRequest url: "${TEAMS_HOOK_URL}", httpMode:"POST", requestBody:"{\"text\":\"Pipeline is completed. You can check with $BUILD_NUMBER build number.\"}"
                        }
                    }
                }
                stage('Send Slack Notifications'){
                    when {
                        expression {
                            params.sendSlack == true
                        }
                    }
                    steps{
                        script{
                            httpRequest url: "${SLACK_HOOK_URL}", httpMode:"POST", requestBody:"{\"text\":\"Pipeline is completed. You can check with $BUILD_NUMBER build number.\"}"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                if (params.keepInJenkins) {
                    archiveArtifacts artifacts: "burp-${SCAN_NUMBER}-${SCAN_LOCATION}.json", onlyIfSuccessful: true
                }
            }

        }
    }
}