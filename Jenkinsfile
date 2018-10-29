def getEnvVar(String paramName){
    return sh (script: "grep '${paramName} env_vars/project.properties|cut -d'=' -f2", returnStdout: true).trim();
}
pipeline{

environment {
    GIT_HASH = sh (script: "git rev-parse --short HEAD", returnStdout: true)
}

agent any

stages{
    stage('Init'){
        steps{
            //checkout scm;
        script{
        env.BASE_DIR = pwd()
        env.APP_NAME= getEnvVar('APP_NAME')
        env.PROJECT_NAME=getEnvVar('PROJECT_NAME')
        env.DOCKER_REGISTRY_URL=getEnvVar('DOCKER_REGISTRY_URL')
        env.RELEASE_TAG = getEnvVar('RELEASE_TAG')
        env.DOCKER_PROJECT_NAMESPACE = getEnvVar('DOCKER_PROJECT_NAMESPACE')
        env.DOCKER_IMAGE_TAG= "${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_ui:${RELEASE_TAG}"
        env.JENKINS_DOCKER_CREDENTIALS_ID = getEnvVar('JENKINS_DOCKER_CREDENTIALS_ID')
        env.JENKINS_GCLOUD_CRED_ID = getEnvVar('JENKINS_GCLOUD_CRED_ID')
        env.GCLOUD_PROJECT_ID = getEnvVar('GCLOUD_PROJECT_ID')
        env.GCLOUD_K8S_CLUSTER_NAME = getEnvVar('GCLOUD_K8S_CLUSTER_NAME')
        env.JENKINS_GCLOUD_CRED_LOCATION = getEnvVar('JENKINS_GCLOUD_CRED_LOCATION')


        }

        }
    }

    stage('Cleanup'){
        steps{
            sh '''
            docker rmi $(docker images -f 'dangling=true' -q) || true
            docker rmi ($docker images | sed 1,2d | awk '{print $3}') || true
            '''
        }

    }
    stage('Build-api'){
        steps{
            withEnv(["APP_NAME=${APP_NAME}", "PROJECT_NAME=${PROJECT_NAME}"]){
                sh '''
                docker build -t ${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_authapi:${RELEASE_TAG} --build-arg APP_NAME=${APP_NAME}_authapi  -f pyfln-auth/Dockerfile pyfln-auth/.
                '''
            }   
        }
    }
    stage('Build-ui'){
        steps{
            withEnv(["APP_NAME=${APP_NAME}", "PROJECT_NAME=${PROJECT_NAME}"]){
                sh '''
                docker build -t ${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_ui:${RELEASE_TAG} --build-arg APP_NAME=${APP_NAME}-ui  -f pyfln-ui/Dockerfile pyfln-ui/.
                '''
            }   
        }
    }
    stage('Publish'){
        steps{
            withCredentials([usernamePassword(credentialsId: "${env.JENKINS_DOCKER_CREDENTIALS_ID}", userameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWD')]){
            sh '''
            docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWD ${DOCKER_REGISTRY_URL}
            docker push ${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_UI:${RELEASE_TAG}
            docker logout
            '''
        }
        }
    }
    stage('Deploy'){
        steps{
        sh'''
        gcloud auth activate-service-account ${JENKINS_GCLOUD_CRED_LOCATION}
        gcloud container clusters get-credentials ${GCLOUD_K8S_CLUSTER_NAME}
        
        chmod +x $BASE_DIR/k8s/process_files.sh

        cd $BASE_DIR/k8s/.
        ./process_files.sh "$GCLOUD_PROJECT_ID" "${APP_NAME}"-ui "${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_ui:${RELEASE_TAG}" "./pyfln-ui/"
        
        cd $BASE_DIR/k8s/pyfln-auth
        ./process_files.sh "$GCLOUD_PROJECT_ID" "${APP_NAME}-auth" "${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}_authapi:${RELEASE_TAG}" "./pyfln-auth/"

        cd $BASE_DIR/k8s/pyfln-ui/.
        kubectl create -f ./*.yml

        cd $BASE_DIR/k8s/pyfln-auth/.
        kubectl create -f ./*.yml

        gcloud auth revoke --all
        '''
        }
    }
}

post {
    always {
        emailext(attachLog: true,
        mimeType: 'text/html',
        body: '''
        <h2>Build# ${env.BUILD_NUMBER} - Job: ${env.JOB_NUMBER} status is: ${currentBuild.currentResult}</h2>
        <p>Check console output at &QUOT;<a href='${env.BUILD_URL'>${env.JOB_NAME} - [${env.BUILD_NUMBER}]</a>&QUOT;</p>
        ''',
        recipientProviders: [[$class: "FirstFailingBuildSusspectRecipientProvider"]],
        subject: "Build# ${env.BUILD_NUMBER} - Job: ${env.JOB_NUMBER} status is: ${currentBuild.currentResult}",
        to: "e.amitthakur@gmail.com")
    }
}
}