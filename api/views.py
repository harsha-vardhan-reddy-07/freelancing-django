from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, NewProjectForm, BiddingForm, ProjectSubmissionForm
from .models import users_collection, project_collection, application_collection
import bson
import datetime

def landing(request):
    return render(request, 'landing.html')

def login(request):
    error=''
    data = {}
    isLogged = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                data = users_collection.find_one({'email': email})
                if data.get('password') == password:
                    data['userId'] = str(data['_id'])
                    isLogged = True
                
                else:
                    form = LoginForm()
                    error = 'Wrong credientials. Please try again.'
                    
            except:
                form = LoginForm()
                error = 'User not found!! Please try again.'
        else:
            form = LoginForm()
            error = 'Wrong credientials. Please try again.'
    else:
        form = LoginForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'login.html', context)



def register(request):
    error=''
    data = {}
    isLogged = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']

            user = {"username": username, "email": email, "password": password, "usertype": usertype, "currentProjects": [], "completedProjects": [], "applications": [], "funds": 0}
            result = users_collection.insert_one(user)
            isLogged = True
            data = {
            'userId': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'usertype': usertype
            }
            
        else:
            form = RegisterForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = RegisterForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'register.html', context)



def loadFreelancer(request):
    return render(request, 'freelancer/loading/loadFreelancer.html')

def freelancer(request, id):
    objId = bson.ObjectId(id)
    freelancer = users_collection.find_one({"_id": objId})
    freelancer['currProsLen'] = len(freelancer['currentProjects'])
    freelancer['completeProsLen'] = len(freelancer['completedProjects'])
    freelancer['applicationsLen'] = len(freelancer['applications'])
    return render(request, 'freelancer/freelancer.html', {"freelancer": freelancer, "id": id})


def loadAllProjects(request):
    return render(request, 'freelancer/loading/loadAllProjects.html')

def allProjects(request, id):
    projects = [project for project in project_collection.find()]
    for p in projects:
        p['id'] = str(p['_id'])
        p['applicationsLen'] = len(p['bids'])
        sum = 0
        c = 0
        for bid in p['bidAmounts']:
            c += 1
            sum += bid
        
        p['avgBid'] = sum/c if c > 0 else 0

    return render(request, 'freelancer/allProjects.html', {"projects": projects})


def loadMyProjects(request):
    return render(request, "freelancer/loading/loadMyProjects.html")

def myProjects(request, id):
    projects = [p for p in project_collection.find({"freelancerId": id})]
    for p in projects:
        p['id'] = str(p['_id'])
        p['applicationsLen'] = len(p['bids'])
        sum = 0
        c = 0
        for bid in p['bidAmounts']:
            c += 1
            sum += bid
        p['avgBid'] = int(int(sum)/ int(c)) | 0



    return render(request, "freelancer/myProjects.html", {"projects": projects})


def loadMyApplications(request):
    return render(request, "freelancer/loading/loadMyApplications.html")

def myApplications(request, id):

    applications = [application for application in application_collection.find({"freelancerId": id})]
    return render(request, "freelancer/myApplications.html", {"applications": applications, "id": id})


def loadProject(request, proId):
    return render(request, "freelancer/loading/loadProjectData.html", {"proId": proId})

def project(request, proId, userId):
    bidForm = BiddingForm()
    submissionForm = ProjectSubmissionForm();
    project = project_collection.find_one({"_id": bson.ObjectId(proId)})
    project['id'] = str(project['_id'])
    project["bidded"] = userId in project['bids']
    return render(request, "freelancer/projectData.html", {"project": project, "userId": userId, "bidForm": bidForm, "submissionForm": submissionForm})

def submitBid(request, proId, userId):
    success = False

    proObj = bson.ObjectId(proId)
    project = project_collection.find_one({"_id": proObj})

    userObj = bson.ObjectId(userId)
    user = users_collection.find_one({"_id": userObj})


    if request.method == 'POST':
        projectId = str(project['_id'])
        clientId = str(project['clientId'])
        clientName = project['clientName']
        clientEmail = project['clientEmail']

        freelancerId = str(user['_id'])
        freelancerName = user['username']
        freelancerEmail = user['email']

        bidAmount = int(request.POST.get('bidAmount',''))
        estimatedTime = request.POST.get('estimatedTime','')
        skills = request.POST.get('skills','')
        skills = skills.split(",")
        freelancerSkills = [skill.strip() for skill in skills]

        title = project['title']
        description = project['description']
        budget = project['budget']
        requiredSkills = project['skills']
        
        proposal = request.POST.get('proposal','')
        status = "Pending"

        application = {"projectId": projectId, "clientId": clientId, "clientName": clientName,
                       'clientEmail': clientEmail, "freelancerId": freelancerId, "freelancerName": freelancerName,
                        "freelancerEmail": freelancerEmail, "bidAmount": bidAmount, "estimatedTime": estimatedTime,
                         "freelancerSkills": freelancerSkills, "title": title, "description": description, "budget": budget, "requiredSkills": requiredSkills,
                          "proposal": proposal, "status": status }

        res = application_collection.insert_one(application)

        new_application_id = str(res.inserted_id)

        users_collection.update_one({"_id": userObj}, {"$push": {"applications": new_application_id}})

        project_collection.update_one({"_id": proObj}, {"$push": {"bids": new_application_id}})
        project_collection.update_one({"_id": proObj}, {"$push": {"bidAmounts": int(bidAmount)}})
        success = True

    return render(request, "freelancer/submitBid.html", {"success": success})
        

def submitProject(request, id):
    success = False
    if request.method == 'POST':
        projectId = id
        projectLink = request.POST.get('projectLink','')
        manualLink = request.POST.get('manualLink','')
        submissionDescription = request.POST.get('submissionDescription','')

        project_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"submission": True, "projectLink": projectLink, "manualLink": manualLink, "submissionDescription": submissionDescription}})
        success = True
    return render(request, "freelancer/submitProject.html", {"success": success, "id": id})




def loadClient(request):
    return render(request, "client/loading/loadClient.html")

def client(request, id):
    projects = [project for project in project_collection.find({"clientId": id})]
    for p in projects:
        p['id'] = str(p['_id'])
        p['applicationsLen'] = len(p['bids'])

    return render(request, "client/client.html", {"projects": projects, "id": id})


def loadProjectApplications(request):
    return render(request, "client/loading/loadProjectApplications.html")

def projectApplications(request, id):
    applications = [application for application in application_collection.find({"clientId": id})]
    for app in applications:
        app['id'] = str(app['_id'])

    return render(request, "client/projectApplications.html", {"applications": applications})

def approveApplication(request, id):

    success = False
    application = application_collection.find_one({"_id": bson.ObjectId(id)})
    application_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"status": "Approved"}})
    projectId = application['projectId']

    freelancer = users_collection.find_one({"_id": bson.ObjectId(application['freelancerId'])})
    
    project_collection.update_one({"_id": bson.ObjectId(projectId)}, {"$set": {"status": "Assigned", "freelancerId": str(freelancer['_id']), "freelancerName": freelancer['username']}})
    application_collection.update_many({"projectId": projectId,  "status": "Available" }, {"$set": {"status": "Rejected"}})
    users_collection.update_one({"_id": bson.ObjectId(application['freelancerId'])},{"$push": {"currentProjects": id}})
    success = True
    return render(request, "client/approveApplication.html", {"success": success})


def rejectApplication(request, id):

    success = False
    application = application_collection.find_one({"_id": bson.ObjectId(id)})
    application_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"status": "Rejected"}})

    success = True
    return render(request, "client/rejectApplication.html", {"success": success})



def loadNewProject(request):
    return render(request, "client/loading/loadNewProject.html")

def newProject(request, id):
    success = False
    error = ''
    if request.method == 'POST':
        form = NewProjectForm(request.POST)
        objId = bson.ObjectId(id)
        client = users_collection.find_one({"_id": objId})
        if form.is_valid():
            clientId = str(client['_id'])
            clientName = client['username']
            clientEmail = client['email']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            budget = form.cleaned_data['budget']

            skills = form.cleaned_data['skills']
            skills = skills.split(",")

            skills = [skill.strip() for skill in skills]

            bids = []
            bidAmounts = []
            postedDate = datetime.datetime.now()
            status = "Available"

            freelancerId = ""
            freelancerName = ""
            deadline = ""
            submission = False

            submissionAccepted = False

            projectLink = ""
            manualLink = ""
            subissionDescription = ""

            project = {"clientId": clientId, "clientName": clientName, "clientEmail": clientEmail, "title": title,
                          "description": description, "budget": budget, "skills": skills, "bids": bids, "bidAmounts": bidAmounts,
                          "postedDate":postedDate, "status": status, "freelancerId": freelancerId, "freelancerName": freelancerName,
                          "deadline": deadline, "submission": submission, "submissionAccepted": submissionAccepted, "projectLink": projectLink,
                          "manualLink": manualLink, "submissionDescription": subissionDescription}
           
            result = project_collection.insert_one(project)
            success = True
            
        else:
            form = NewProjectForm()
            print("erroruu")
            success = False
            error = 'Invalid form data. Please try again.'
    else:
        form = NewProjectForm()
    
    context = {'form': form, 'success': success, 'error': error}

    return render(request, "client/newProject.html", context)


def loadClientProject(request, proId):
    return render(request, "client/loading/loadProjectWorking.html", {"proId": proId})

def clientProject(request, proId, clientId):

    objId = bson.ObjectId(proId)
    project = project_collection.find_one({"_id": objId})
    project['id'] = str(project['_id'])

    return render(request, "client/projectWorking.html", {"project": project, "clientId": clientId})

def approveSubmission(request, id):
    success = False
    project = project_collection.find_one({"_id": bson.ObjectId(id)})
    project['status'] = "Completed"
    project['submissionAccepted'] = True
    project_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": project})

    user = users_collection.find_one({"_id": bson.ObjectId(project['freelancerId'])})
    user['funds'] += int(project['budget'])
    user['completedProjects'].append(id)
    user['completedProjects'].remove(id)
    
    users_collection.update_one({"_id": bson.ObjectId(project['freelancerId'])}, {"$set": user})
    success = True
    return render(request, 'client/approveSubmission.html', {"proId":id, "clientId":project['clientId'], "success": success})


def rejectSubmission(request, id):
    success = False
    project = project_collection.find_one({"_id": bson.ObjectId(id)})
    project_collection.update_one({"_id": bson.ObjectId(id)}, {"$set": {"submission": False, "projectLink": "", "manualLink": "", "submissionDescription": ""}})
    success = True
    return render(request, 'client/rejectSubmission.html', {"proId":id, "clientId":project['clientId'], "success": success})



def admin(request):
    projects = [project for project in project_collection.find()]
    projectsLen = len(projects)
    completedProLen = 0
    for p in projects:
        if p['status'] == 'Completed':
            completedProLen += 1

    applications = [application for application in application_collection.find()]
    applicationsLen = len(applications)

    users = [user for user in users_collection.find()]
    usersLen = len(users)

    return render(request, "admin/admin.html", {"projectsLen": projectsLen, "completedProLen": completedProLen, "applicationsLen": applicationsLen, "usersLen": usersLen })

def adminProjects(request):
    projects = [project for project in project_collection.find()]
    for p in projects:
        p['id'] = str(p['_id'])
        p['applicationsLen'] = len(p['bids'])
        sum = 0
        c = 0
        for bid in p['bidAmounts']:
            c += 1
            sum += bid
        
        p['avgBid'] = sum/c if c > 0 else 0
    return render(request, "admin/adminProjects.html", {"projects": projects})

def adminApplications(request):
    applications = [application for application in application_collection.find()]
    for app in applications:
        app['id'] = str(app['_id'])
    return render(request, "admin/allApplications.html", {"applications": applications})

def allUsers(request):
    users = [user for user in users_collection.find()]
    for u in users:
        u['id'] = str(u['_id'])
    return render(request, "admin/allUsers.html", {"users": users})