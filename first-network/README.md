# first-network

first network for HRB-testing

# Installation steps:
1. clone project to directory
2. install a node on localhost and run composer-rest-server on docker
    * configure `rest_server` in `src/main.py` to the rest server address
3. run `python3 src/main.py`

# How to use:
1. On first use, select `Admin` access
    * Create a new Person and new Organization under `Admin` menu

2. As `Person`, start using with your person ID
    * Add/Delete your employer with their organization ID under `Operation` menu
    * Start adding your own resume (entry which will be approved by organization) or update your resume (entry which is approved by organization)

3. As `Organization`, start using with your organization ID
    * Start adding to entry to your person's resume (which will be updated by organization) or approve add request by person
    * Query person's resume by ID under `Operation` menu


# REST METHODS
Function Available

1. `OrganizationAdd` (POST) \n
    description: Organization Add Something to Resume (need to be updated by Person) \n
    parameter : { \n
  "$class": "org.example.firstnetwork.OrganizationAdd", \n
  "resume": "resource:org.example.firstnetwork.Resume#<ID_1>", \n
  "addValue": { \n
    "$class": "org.example.firstnetwork.ResumeValue", \n
    "Value": <STRING>, \n
    "org": "resource:org.example.firstnetwork.Organization#<ID_2>", \n
    "Approved": false \n
  } \n
} \n
where  \n
    ID_1 = resume id (will be same with Person id) \n
    ID_2 = Organization id \n
    STRING = description \n
 \n
 \n
2. `PersonAdd` (POST) \n
    description: Person Add Something to Resume (need to be approved by Organization) \n
    parameter : { \n
  "$class": "org.example.firstnetwork.PersonAdd", \n
  "owner": "resource:org.example.firstnetwork.Person#<ID_1>", \n
  "org": "resource:org.example.firstnetwork.Organization#<ID_2>", \n
  "resume": "resource:org.example.firstnetwork.Resume#<ID_3>", \n
  "addValue": { \n
    "$class": "org.example.firstnetwork.ResumeValue", \n
    "Value": <STRING>, \n
    "org": "resource:org.example.firstnetwork.Organization#<ID_2>", \n
    "Approved": false \n
  } \n
} \n
where  \n
    ID_1 = Person id \n
    ID_2 = Organization id \n
    ID_3 = (ID_1) resume id (will be same with Person id) \n
    STRING = description \n
 \n
 \n
3. `OrganizationApproved` (POST) \n
    description: Organization approved Person's request to add to Resume (need to be updated by Person) \n
    parameter : { \n
  "$class": "org.example.firstnetwork.OrganizationApproved", \n
  "request": "resource:org.example.firstnetwork.requestResume#<ID>" \n
} \n
where  \n
    ID = id for request doc to be add  \n
 \n
 \n
4. `UpdateResume` (POST) \n
    description: Person update it resume with the doc approved by Organization \n
    parameter : { \n
  "$class": "org.example.firstnetwork.UpdateResume", \n
  "approved": "resource:org.example.firstnetwork.approvedResume#<ID>" \n
} \n
where  \n
    ID = id for approved doc to be add  \n
 \n
 \n
5. `AddEmployer` (POST) \n
    description: Person add Organization to resume \n
    parameter : { \n
  "$class": "org.example.firstnetwork.AddEmployer", \n
  "resume": "resource:org.example.firstnetwork.Resume#<ID_1>", \n
  "employer": "resource:org.example.firstnetwork.Organization#<ID_2>" \n
} \n
where  \n
    ID_1 = resume id (will be same with Person id) \n
    ID_2 = organization id \n
 \n
 \n
6. `DeleteEmployer` (POST) \n
    description: Person delete Organization from resume \n
    parameter : { \n
  "$class": "org.example.firstnetwork.AddEmployer", \n
  "resume": "resource:org.example.firstnetwork.Resume#<ID>", \n
  "employer": "resource:org.example.firstnetwork.Organization#<ID>" \n
} \n
where  \n
    ID_1 = resume id (will be same with Person id) \n
    ID_2 = organization id \n
