# first-network

first network for HRB-testing

# Installation steps:
1. clone project to directory
2. install a node on localhost and run composer-rest-server on docker
2a. configure `rest_server` in `src/main.py` to the rest server address
3. run `python3 src/main.py`

# How to use:
1. On first use, select `Admin` access
1a. Create a new Person and new Organization under `Admin` menu

2. As `Person`, start using with your person ID
2a. Add/Delete your employer with their organization ID under `Operation` menu
2b. Start adding your own resume (entry which will be approved by organization) or update your resume (entry which is approved by organization)

3. As `Organization`, start using with your organization ID
3a. Start adding to entry to your person's resume (which will be updated by organization) or approve add request by person
3b. Query person's resume by ID under `Operation` menu

###
GET FUNCTION 
Person

Function Available

1) OrganizationAdd (POST) 
    description: Organization Add Something to Resume (need to be updated by Person)
    parameter : {
  "$class": "org.example.firstnetwork.OrganizationAdd",
  "resume": "resource:org.example.firstnetwork.Resume#<ID_1>",
  "addValue": {
    "$class": "org.example.firstnetwork.ResumeValue",
    "Value": <STRING>,
    "org": "resource:org.example.firstnetwork.Organization#<ID_2>",
    "Approved": false
  }
}
where 
    ID_1 = resume id (will be same with Person id)
    ID_2 = Organization id
    STRING = description


2) PersonAdd (POST)
    description: Person Add Something to Resume (need to be approved by Organization)
    parameter : {
  "$class": "org.example.firstnetwork.PersonAdd",
  "owner": "resource:org.example.firstnetwork.Person#<ID_1>",
  "org": "resource:org.example.firstnetwork.Organization#<ID_2>",
  "resume": "resource:org.example.firstnetwork.Resume#<ID_3>",
  "addValue": {
    "$class": "org.example.firstnetwork.ResumeValue",
    "Value": <STRING>,
    "org": "resource:org.example.firstnetwork.Organization#<ID_2>",
    "Approved": false
  }
}
where 
    ID_1 = Person id
    ID_2 = Organization id
    ID_3 = (ID_1) resume id (will be same with Person id)
    STRING = description


3) OrganizationApproved (POST)
    description: Organization approved Person's request to add to Resume (need to be updated by Person)
    parameter : {
  "$class": "org.example.firstnetwork.OrganizationApproved",
  "request": "resource:org.example.firstnetwork.requestResume#<ID>"
}
where 
    ID = id for request doc to be add 


4) UpdateResume (POST)
    description: Person update it resume with the doc approved by Organization
    parameter : {
  "$class": "org.example.firstnetwork.UpdateResume",
  "approved": "resource:org.example.firstnetwork.approvedResume#<ID>"
}
where 
    ID = id for approved doc to be add 


5) AddEmployer (POST)
    description: Person add Organization to resume
    parameter : {
  "$class": "org.example.firstnetwork.AddEmployer",
  "resume": "resource:org.example.firstnetwork.Resume#<ID_1>",
  "employer": "resource:org.example.firstnetwork.Organization#<ID_2>"
}
where 
    ID_1 = resume id (will be same with Person id)
    ID_2 = organization id


6) DeleteEmployer (POST)
    description: Person delete Organization from resume
    parameter : {
  "$class": "org.example.firstnetwork.AddEmployer",
  "resume": "resource:org.example.firstnetwork.Resume#<ID>",
  "employer": "resource:org.example.firstnetwork.Organization#<ID>"
}
where 
    ID_1 = resume id (will be same with Person id)
    ID_2 = organization id
