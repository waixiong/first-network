# first-network

first network for HRB-testing

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
    

2) PersonAdd (POST)
    description: Person Add Something to Resume (need to be approved by Organization)
    parameter : {
  "$class": "org.example.firstnetwork.PersonAdd",
  "requestId": "",
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