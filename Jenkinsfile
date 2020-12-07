pipeline {
    agent any 
    
    stages {
        // Clone the repo and check out to master branch 
        stage('Checkout') {
      steps {
        script { 
            git branch: 'master',
                credentialsId: '87eb1ecd-3cda-4eb7-9c1b-bca7df1460ea',
                url: 'https://github.com/kerencarmelwedel/covid-19-assignment.git'            
          }
      //start the python service
       stage('build') {
    steps {
        sh 'python covid19.py'
    }
}
         stage("test") {
        
            steps {
                echo 'testing the application... '
            
            }
        }
         stage("deploy") {
        
            steps {
                echo 'deploying the application... '

            
            }
        }
    }
}
   
