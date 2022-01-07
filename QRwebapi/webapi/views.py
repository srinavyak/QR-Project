from django.shortcuts import render
import requests
from django.contrib import messages
from django.http import HttpResponse
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import pyodbc
import mammoth
from django.http import JsonResponse
import docx2txt
import json
# Create your views here.
global li
global res


def home(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST["email"]
        password = request.POST["password"]
        print(username)
        print(password)
        str = 'https://localhost:44360/api/login/' + username + '/' + password
        print(str)
        res = requests.get(str, verify=False).json()
        # #r=requests.get('https://localhost:44360/api/login/{username?}/{password?}')
        # # resp = res.json()
        print(res)
        request.session["res"] = res
        li = [item.get('message') for item in res]
        print(li[0])
        usertype=[item.get('userTypeID') for item in res]
        print(usertype[0])
        userID=[item.get('userID') for item in res]
        userid= userID[0]
        request.session['userid']=userid
        if usertype[0]==1:
            if li[0] == 'Invalid Username or Password':
                messages.error(request, 'Invalid Username or Password')
                return render(request, 'login.html')
            else:
                return template(request)
                # return profile(request)
        else:
            if li[0] == 'Invalid Username or Password':
                messages.error(request, 'Invalid Username or Password')
                return render(request, 'login.html')
            else:
                return userform1(request)   
    else:
        return render(request, 'login.html')


def profile(request):
    x = request.session["res"]
    print(x)
    userid = [item.get('userID') for item in x]
    request.session['userID'] = userid[0]
    usertypeid = [item.get('$id') for item in x]
    request.session['$id'] = usertypeid[0]

    firstname = [item.get('firstName') for item in x]
    fn = firstname[0]
    lastname = [item.get('lastName') for item in x]
    ln = lastname[0]
    email = [item.get('username') for item in x]
    eml = email[0]
    qrid = [item.get('qrid') for item in x]
    qid = qrid[0]
    content = {
        'firstname': fn,
        'lastname': ln,
        'email': eml,
        'qrid': qid,
    }
    return render(request, 'Profile.html', content)

def userprofile(request):
    return render(request, 'Profile1.html')
def updateprofile(request):
    if request.method == 'POST':
        userID = request.session['userID']
        ID = "{}".format(userID)
        userTypeID = request.session['$id']
        user = "{}".format(userTypeID)
        QRID = request.POST.get("qrid")
        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        username = request.POST.get("email")
        # print(firstName)
        # print(lastName)
        # print(username)
        # print(QRID)
        # print(user)
        # print(ID)
        # print(userID)
        password = "''"
        mode = '2'
        # print(type(password))
        # print(type(mode))
        # print(type(QRID))
        # print(type(userID))
        # print(type(userTypeID))
        # print(type(firstName))
        # print(type(lastName))
        # print(type(username))
        lnk = 'https://localhost:44360/api/adduser/' + ID + '/' + user + '/' + QRID + \
            '/' + firstName + '/' + lastName + '/'+username + '/' + password + '/' + mode
        # print(lnk)
        res = requests.get(lnk, verify=False).json()
        # print(res)
        return render(request, 'Profile.html', {'firstname': firstName, 'lastname': lastName, 'email': username, 'qrid': QRID})


def template(request):
    mode = '4'
    templateID = "1"
    templateName = "formA"
    str = 'https://localhost:44360/api/template/' + \
        templateID + '/' + templateName + '/' + mode
    # print(str)
    res1 = requests.get(str, verify=False).json()
    # print(res1)
    tempid = [item.get('templateID') for item in res1]
    tempname = [item.get('templateName') for item in res1]
    # print(tempid)
    # print(tempname)
    data = [{'TemplateID': b, 'TemplateName': c}
            for b, c in zip(tempid, tempname)]
    # print(data)
    mode = '6'
    templateID = "1"
    templateName = "AAA"
    str = 'https://localhost:44360/api/template/' + \
        templateID + '/' + templateName + '/' + mode
    print(str)
    res1 = requests.get(str, verify=False).json()
    print("count of template",res1)
    count=[item.get('templateID') for item in res1]
    totalcount=count[0]
    return render(request, 'Templates.html', {'data': data,'count':totalcount})


def templateform(request):
    if request.method == 'POST':
        templateName = request.POST["templatename"]
        print(templateName)
        mode = '1'
        templateID = '8'
        str = 'https://localhost:44360/api/template/' + \
            templateID + '/' + templateName + '/' + mode
        # print(str)
        res1 = requests.get(str, verify=False).json()
        # print(res1)
        tempid = [item.get('templateID') for item in res1]
        tempname = [item.get('templateName') for item in res1]
        # print(tempid)
        # print(tempname)
        data = [{'TemplateID': b, 'TemplateName': c}
                for b, c in zip(tempid, tempname)]
        # print(data)
        request.session["res1"] = res1
        li = [item.get('message') for item in res1]
        # print(li[0])
        if li[0] == 'Template already existed':
            messages.error(request, 'Template already existed')
            # return render(request, 'Templates.html')
            return template(request)

        else:
            # return render(request, 'Templates.html', {'data': data, 'tempname': templateName})
            return template(request)

def gettemid(request):
    if request.method == 'GET':
        x=request.GET["stock"]
        print("ssssssss",x)
        templateName=x
        templateid=1
        id = "{}".format(templateid)
        mode='7'
        str = 'https://localhost:44360/api/template/' + \
            id + '/' + templateName + '/' + mode
        print(str)
        res1 = requests.get(str, verify=False).json()
        print(res1)
        tempid = [item.get('templateID') for item in res1]
        print("template id of template page",tempid[0])
        request.session['tempid']=tempid[0]
        fieldnamelist=x
        controltypelist="''"
        htmltaglist="''"
        mandatoryField='true'
        sortorder="1"
        fieldID = "1"
        mode='4'
        str1 = 'https://localhost:44360/api/templatedetails/' + \
                    id + '/' + fieldnamelist + '/' + controltypelist + '/' + htmltaglist + '/' + mandatoryField + '/' + sortorder + '/' + fieldID + '/' +mode
        # print(str1)
        res = requests.get(str1, verify=False).json()
        # print(res)
        return JsonResponse(res,safe=False)
def tempform(request):
    # templateid=request.session.get('tempid')
    # print("template form----",templateid)
    # id = "{}".format(templateid)
    # fieldnamelist="''"
    # controltypelist="''"
    # htmltaglist="''"
    # mandatoryField='true'
    # sortorder="1"
    # mode='4'
    # str1 = 'https://localhost:44360/api/templatedetails/' + \
    #             id + '/' + fieldnamelist + '/' + controltypelist + '/' + htmltaglist + '/' + mandatoryField + '/' + sortorder + '/' + mode
    # print(str1)
    # res = requests.get(str1, verify=False).json()
    # print(res)
    # print(len(res))
    # # id = "{}".format(templateid)
    # # fieldnamelist="''"
    # # controltypelist="''"
    # # htmltaglist="''"
    # # mandatoryField='true'
    # # sortorder="1"
    # # mode='5'
    # # str2 = 'https://localhost:44360/api/templatedetails/' + \
    # #             id + '/' + fieldnamelist + '/' + controltypelist + '/' + htmltaglist + '/' + mandatoryField + '/' + sortorder + '/' + mode
    # # print(str2)
    # # res1 = requests.get(str2, verify=False).json()
    # # print(res1)
    # if len(res)!=0:
    #     mylist=[]
    #     x=[1,2,3,4]
    #     mylist = zip(x, res)
    #     return render(request, 'TemplateForm1.html', {'formdetails':mylist})
    # else:
    return render(request, 'TemplateForm1.html')


def formdata(request):
    return render(request, 'TemplatesForm.html')


# def generaterow(request):
#     if request.method == 'POST':
#         rowno = request.POST["rowno"]
#         print(rowno)
#         request.session['rowno'] = rowno
#         print(type(rowno))
#         if rowno != '':
#             y = int(rowno)
#             x = []
#             for i in range(1, y+1):
#                 x.append(i)
#                 request.session['x'] = x
#         else:
#             x = ''
        
#     return render(request, 'TemplatesForm.html', {'rowdata': x, 'number': rowno})




def formdetails(request):
    # rowno = request.session['rowno']
    tempid=request.session.get('tempid')
    if request.method == 'POST':
        rowno = request.POST.get('rowno')
        print("rowno",rowno)
        # dropdown=request.POST.get('dropdown')
        # print(dropdown)
        # if dropdown !=None:
        #     drpdata=dropdown.strip(',')
        #     print(drpdata)
        # else:
        #     pass
        y = int(rowno)
        fieldnamelist = []
        controltypelist = []
        mandatoryField = []
        htmltaglist = []
        fieldids = []
        for i in range(1, y+1):
            fieldname = request.POST.get("fieldname"+''+str(i)+'')
            controltype = request.POST.get("hiddenvalue"+''+str(i)+'')
            manadatory = request.POST.get("manadatory"+''+str(i)+'')
            htmltag = request.POST.get("htmltag"+''+str(i)+'')
            fielddata = request.POST.get("fieldid"+''+str(i)+'')
            print(fielddata)
            # dropdownvalue=request.POST.get("dropdowndata"+''+str(i)+'')
            # print(dropdownvalue)
            if controltype == 'Dropdown':
                dropdownvalue=request.POST.get("dropdowndata"+''+str(i)+'')
                print("dropdown vales",dropdownvalue)
                drpdata=dropdownvalue.strip(',')
                s = ''.join([str(elem) for elem in drpdata])
                controltype = controltype + "-"+s
                print(controltype)
                
            else:
                pass
            if manadatory == "Yes":
                mandatoryField.append("True")
            else:
                mandatoryField.append("False")
                
            fieldnamelist.append(fieldname)
            controltypelist.append(controltype)
            htmltaglist.append(htmltag)
            fieldids.append(fielddata)
        # print(dropdown)
        print(fieldnamelist)
        print(controltypelist)
        print(mandatoryField)
        print(htmltaglist)
        # print(fieldids)
        
        templateid = []
        sortorder = []
        id = "{}".format(tempid)
        for i in range(len(fieldnamelist)):
            templateid.append(id)
        for i in range(len(fieldnamelist)):
            sortorder.append('1')
        for n, i in enumerate(fieldids):
            if i == None or i == '':
                fieldids[n] = '1'
        print(fieldids)
        mode = '6'
        for templateId,fieldnamelist,controltypelist,htmltaglist,mandatoryField,sortorder,fieldID in zip(templateid,fieldnamelist,controltypelist,htmltaglist,mandatoryField,sortorder,fieldids):
            
            str1 = 'https://localhost:44360/api/templatedetails/' + \
                templateId + '/' + fieldnamelist + '/' + controltypelist + '/' + htmltaglist + '/' + mandatoryField + '/' + sortorder + '/' + fieldID + '/' + mode
            print(str1)
            res = requests.get(str1, verify=False).json()
            print(res)
        
        return render(request, 'TemplateForm1.html')
def getid(request):
    if request.method == 'GET':
        x=request.GET["stock"]
        print("ssssssss",x)
        mode = '4'
        inUse = 'true'
        templatename = "AAA"
        y = '4'
        id = "{}".format(y)
        str1 = 'https://localhost:44360/api/templatedocument/' + \
            id + '/' + x + '/' + inUse + '/' + templatename + '/' + mode
        # print(str1)
        res = requests.get(str1, verify=False).json()
        print(res)
        userid = [item.get('$id') for item in res]
        tempname = [item.get('templateName') for item in res]
        filename = [item.get('fileName') for item in res]
        fileID = [item.get('fileID') for item in res]
        isActive =  [item.get('isActive') for item in res]
        data=[]
        data = [{'UserID': userid, 'Name': name, 'FileName': file,'FileID':fileID,'isActive':isActive}
                for userid, name, file,fileID,isActive in zip(userid, tempname, filename,fileID,isActive)]
        
        res = [ sub['FileID'] for sub in data]
        print("The values corresponding to key : " + str(res))
        frstdata = res[0]
        print(frstdata)
        for d in data:
            d['FileID'] = frstdata
        print(data)
        for i in range(len(data)):
            if data[i]['UserID'] == '1':
                del data[i]
                break
        print (data)
        return JsonResponse(data,safe=False)
        
def docupload(request):
    return render(request, 'Templates-UploadDoc.html')
        
def fileinsert(request):
    if request.method == 'POST':
        tempname = request.POST["tempid"]
        fileName = request.FILES['customfile']
        fs = FileSystemStorage()
        filename = fs.save(fileName.name, fileName)
        # uploaded_file_url = fs.url(filename)
        # print("---")
        # print(filename)
        # print("---")
        # print(uploaded_file_url)
        # print("---")
        # print(fileName)
      
         
        x = "{}".format(fileName)
        print(type(x))
        mode = '5'
        templateId = '1'
        str = 'https://localhost:44360/api/template/' + templateId + '/' + tempname + '/' + mode
        print(str)
        res1 = requests.get(str, verify=False).json()
        print(res1)
        print("------------------------------------------------------")
        tempid = [item.get('templateID') for item in res1]
        print(tempid)
        y = tempid[0]
        id = "{}".format(y)
        print(id)
        mode = '1'
        templatename="AAA"
        inUse = 'true'
        str1 = 'https://localhost:44360/api/templatedocument/' + id + '/' + x + '/' + inUse + '/' + templatename + '/' + mode
        print(str1)
        res = requests.get(str1, verify=False).json()
        print(res)
        userid = [item.get('$id') for item in res]
        tempname = [item.get('templateName') for item in res]
        filename = [item.get('fileName') for item in res]
        print(tempid)
        print(tempname)
        # data = [{'UserID': userid, 'Name': name, 'FileName': file}
        #         for userid, name, file in zip(userid, tempname, filename)]
        # print(data)
        # return render(request, 'Templates-UploadDoc.html', {'data': data})
        return render(request, 'Templates-UploadDoc.html')

def fileview(request):
    # some_data = request.GET['x']
    # print(some_data)
    if request.method == 'GET':
        x=request.GET["stock"]
        print(x)
        with open(r"E:/QRwebapi/QRwebapi/media/"+ x , "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value # The generated HTML
            print(html)
            messages = result.messages
            print(messages)
        # content={'data':html}
        return JsonResponse(html,safe=False)

    # elif request.method == 'POST':
    #     # x=request.get('data')
    #     x=request.POST.get("stock")
    #     print(x)
    #     return render(request,'UserForm.html')
        
def changepassword(request):
    return render(request, 'ChangePassword.html')

def userchangepassword(request):
    return render(request, 'ChangePassword1.html')

def changepassword1(request):
    if request.method == 'POST':
        userID = request.session['userID']
        ID = "{}".format(userID)
        Currentpassword = request.POST["CurrentPassword3"]
        Newpassword = request.POST["NewPassword3"]
        Confirmpassword = request.POST["ConfirmPassword3"]
        print(Currentpassword)
        print(Newpassword)
        print(Confirmpassword)
        str = 'https://localhost:44360/api/updatepassword/' + \
            ID + '/' + Confirmpassword + '/' + Currentpassword
        print(str)
        res = requests.get(str, verify=False).json()
        # #r=requests.get('https://localhost:44360/api/login/{username?}/{password?}')
        # # resp = res.json()
        print(res)
        # request.session["res"]=res
        li = [item.get('message') for item in res]
        print(li[0])
        if li[0] == 'Password is not matched':
            messages.error(request, 'Current password does not exists')
            return render(request, 'ChangePassword.html')
        else:
            messages.error(request, 'Successfully Updated Password')
            return render(request, 'ChangePassword.html')

def adduser(request):
    userID = '1'
    userTypeID = '1'
    QRID='123'
    # QRID='qr10'
    firstName='sri'
    lastName='navya'
    username='navya@gmail.com'
    password='Sri@1'
    mode = '4'
    lnk = 'https://localhost:44360/api/adduser/' + userID + '/' + userTypeID + '/' + \
        QRID + '/' + firstName + '/' + lastName + \
        '/'+ username + '/' + password + '/' + mode
    print(lnk)
    res = requests.get(lnk, verify=False).json()
    print(res)
    userid = [item.get('$id') for item in res]
    name = [item.get('firstName') for item in res]
    username = [item.get('username') for item in res]
    print(name)
    print(username)
    data = [{'UserID': userid, 'FullName': name, 'Email': email}
            for userid, name, email in zip(userid, name, username)]
    print("''''''''''''''''")
    print(data)
    userID = '1'
    userTypeID = '1'
    QRID='123'
    # QRID='qr10'
    firstName='sri'
    lastName='navya'
    username='navya@gmail.com'
    password='Sri@1'
    mode = '6'
    lnk = 'https://localhost:44360/api/adduser/' + userID + '/' + userTypeID + '/' + \
        QRID + '/' + firstName + '/' + lastName + \
        '/'+ username + '/' + password + '/' + mode
    print(lnk)
    res = requests.get(lnk, verify=False).json()
    print(res)
    userid = [item.get('userID') for item in res]
    totaluser=userid[0]
    request.session['totaluser']=totaluser
    userID = '1'
    userTypeID = '1'
    QRID='123'
    # QRID='qr10'
    firstName='sri'
    lastName='navya'
    username='navya@gmail.com'
    password='Sri@1'
    mode = '7'
    lnk = 'https://localhost:44360/api/adduser/' + userID + '/' + userTypeID + '/' + \
        QRID + '/' + firstName + '/' + lastName + \
        '/'+ username + '/' + password + '/' + mode
    print(lnk)
    res = requests.get(lnk, verify=False).json()
    print(res)
    userid = [item.get('userID') for item in res]
    totaladmin=userid[0]
    request.session['totaladmin']=totaladmin
    userID = '1'
    userTypeID = '1'
    QRID='123'
    # QRID='qr10'
    firstName='sri'
    lastName='navya'
    username='navya@gmail.com'
    password='Sri@1'
    mode = '8'
    lnk = 'https://localhost:44360/api/adduser/' + userID + '/' + userTypeID + '/' + \
        QRID + '/' + firstName + '/' + lastName + \
        '/'+ username + '/' + password + '/' + mode
    print(lnk)
    res = requests.get(lnk, verify=False).json()
    print(res)
    userid = [item.get('userID') for item in res]
    users=userid[0]
    request.session['users']=users
    return render(request, 'AddUser.html', {'userdata':data,'totaluser':totaluser,'totaladmin':totaladmin,'users':users})

def adduser1(request):
    if request.method == 'POST':
        firstName = request.POST.get("firstname")
        lastName = request.POST.get("lastname")
        QRID = request.POST.get("QRID")
        username = request.POST.get("email")
        usertype = request.POST.get("user")
        password = request.POST.get("password")
        print("usertype -----",usertype)
        userID = '1'
        # userTypeID = '1'
        # QRID='qr10'
        mode = '1'
        print(username)
        print(password)
        lnk = 'https://localhost:44360/api/adduser/' + userID + '/' + usertype + '/' + \
            QRID + '/' + firstName + '/' + lastName + \
            '/'+username + '/' + password + '/' + mode
        print(lnk)
        res = requests.get(lnk, verify=False).json()
        # #r=requests.get('https://localhost:44360/api/login/{username?}/{password?}')
        # # resp = res.json()
        print(res)
        userid = [item.get('$id') for item in res]
        name = [item.get('firstName') for item in res]
        username = [item.get('username') for item in res]
        print(name)
        data = [{'UserID': userid, 'FullName': name, 'Email': email}
            for userid, name, email in zip(userid, name, username)]
        
        li = [item.get('message') for item in res]
        print(li[0])
        totaluser=request.session['totaluser']
        totaladmin=request.session['totaladmin']
        users=request.session['users']
        if li[0] == 'Email already existed':
            messages.error(request, 'Email already existed')
            # return render(request, 'AddUser.html', {'userdata':data,'totaluser':totaluser,'totaladmin':totaladmin,'users':users})
            return adduser(request)
        elif li[0] == 'Fail':
            messages.error(request, 'QRID/Email already existed')
            # return render(request, 'AddUser.html', {'userdata':data,'totaluser':totaluser,'totaladmin':totaladmin,'users':users})
            return adduser(request)
        elif li[0] == 'User Added Successful':
            messages.success(request, 'User Added Successfully')
            # return render(request, 'AddUser.html', {'userdata':data,'totaluser':totaluser,'totaladmin':totaladmin,'users':users})
            return adduser(request)
        else:
        #    return render(request, 'AddUser.html', {'userdata':data,'totaluser':totaluser,'totaladmin':totaladmin,'users':users})
            return adduser(request)
        
def getusertypeid(request):
    if request.method == 'GET':
        x=request.GET["stock"]
        print("---name--",x)
        print(type(x))
        userID = '1'
        userTypeID = '1'
        QRID='123'
        # QRID='qr10'
        firstName='sri'
        lastName='navya'
        username=x
        password='Sri@1'
        mode = '9'
        link = 'https://localhost:44360/api/adduser/' + userID + '/' + userTypeID + '/' + \
            QRID + '/' + firstName + '/' + lastName + \
            '/'+ username + '/' + password + '/' + mode
        print(link)
        res = requests.get(link, verify=False).json()
        print(res)
        userid = [item.get('userTypeID') for item in res]
        usertypeid=userid[0]
        return JsonResponse(usertypeid,safe=False)
        
def userform1(request):
    global value
    factID='1'
    userID='1'
    templateID='20'
    fieldID='1'
    textValue='x'
    mode='2'
    request.session['templateID']=templateID
    str = 'https://localhost:44360/api/factdata/' + \
        factID + '/' + userID + '/' + templateID+ '/' + fieldID + '/' + textValue + '/' + mode
    print(str)
    res1 = requests.get(str, verify=False).json()
    print(res1)
    fieldName = [item.get('fieldName') for item in res1]
    request.session['fieldName']=fieldName
    fieldID = [item.get('fieldID') for item in res1]
    request.session['fieldID']=fieldID
    fieldType = [item.get('fieldType') for item in res1]
    mandatoryField = [item.get('mandatoryField') for item in res1]
    htmlTag = [item.get('htmlTag') for item in res1]
    fileName = [item.get('fileName') for item in res1]
    data = [( fieldName, fieldType, mandatoryField, htmlTag)
                for fieldName, fieldType, mandatoryField, htmlTag in zip(fieldName, fieldType, mandatoryField, htmlTag)]
    print(data)
    result =','
    result = result.join(htmlTag)
    print(result)
    with open(r"E:/QRwebapi/QRwebapi/media/"+ fileName[0] , "rb") as docx_file:
        result1 = mammoth.convert_to_html(docx_file)
        html = result1.value # The generated HTML
        print(html)
        messages = result1.messages
        # print(messages)
    # text = docx2txt.process("E:\QRwebapi\QRwebapi\media/"+fileName[0])
    # print(text)
    x=[]
    for i in data:
        for j in i:
            x.append(j)
    print(x)
    mylist=[]
    for s in x:
        try:
            if "Dropdown" in s:
                x=print(s)
                lst = s.split("-")
                print(lst)  
                value=lst[1].split(",")
                print(value)
                mylist.append(value)
                # return render(request, 'UserForm1.html', {'data':res1,'filedata':html,'htmltagdata':result,'value':value})
        except:
            # pass
            value=""
    print(mylist)
    x= len(res1)
    datalen=[]
    for i in range(1,x+1):
        datalen.append(i)
    d=[]
    for i in mylist:
        res =","
        res = res.join(i)
        d.append(res)
    # print(d)
    ln= len(d)
    length = []
    for i in range(1,ln+1):
        length.append(i)
    mydropdown = zip(d,length)
    # json_string = json.dumps(d)
    # print(json_string)

    # data1 = [{'dropdownitem':x} 
    #             for x in d]
    # print(data1)
    mydata= zip(res1,datalen)
    return render(request, 'UserForm.html', {'data':mydata,'filedata':html,'htmltagdata':result,'value':value,'dropdownitem':mydropdown,'droplen':ln})
       
def userform(request):
    global value
    factID='1'
    userID='1'
    templateID='20'
    fieldID='1'
    textValue='x'
    mode='2'
    request.session['templateID']=templateID
    str = 'https://localhost:44360/api/factdata/' + \
        factID + '/' + userID + '/' + templateID+ '/' + fieldID + '/' + textValue + '/' + mode
    print(str)
    res1 = requests.get(str, verify=False).json()
    print(res1)
    fieldName = [item.get('fieldName') for item in res1]
    request.session['fieldName']=fieldName
    fieldID = [item.get('fieldID') for item in res1]
    request.session['fieldID']=fieldID
    fieldType = [item.get('fieldType') for item in res1]
    mandatoryField = [item.get('mandatoryField') for item in res1]
    htmlTag = [item.get('htmlTag') for item in res1]
    fileName = [item.get('fileName') for item in res1]
    data = [( fieldName, fieldType, mandatoryField, htmlTag)
                for fieldName, fieldType, mandatoryField, htmlTag in zip(fieldName, fieldType, mandatoryField, htmlTag)]
    print(data)
    result =','
    result = result.join(htmlTag)
    print(result)
    with open(r"E:/QRwebapi/QRwebapi/media/"+ fileName[0] , "rb") as docx_file:
        result1 = mammoth.convert_to_html(docx_file)
        html = result1.value # The generated HTML
        print(html)
        messages = result1.messages
        # print(messages)
    # text = docx2txt.process("E:\QRwebapi\QRwebapi\media/"+fileName[0])
    # print(text)
    x=[]
    for i in data:
        for j in i:
            x.append(j)
    print(x)
    mylist=[]
    for s in x:
        try:
            if "Dropdown" in s:
                x=print(s)
                lst = s.split("-")
                print(lst)  
                value=lst[1].split(",")
                print(value)
                mylist.append(value)
                # return render(request, 'UserForm1.html', {'data':res1,'filedata':html,'htmltagdata':result,'value':value})
        except:
            # pass
            value=""
    print(mylist)
    x= len(res1)
    datalen=[]
    for i in range(1,x+1):
        datalen.append(i)
    d=[]
    for i in mylist:
        res =","
        res = res.join(i)
        d.append(res)
    # print(d)
    ln= len(d)
    length = []
    for i in range(1,ln+1):
        length.append(i)
    mydropdown = zip(d,length)
    # json_string = json.dumps(d)
    # print(json_string)

    # data1 = [{'dropdownitem':x} 
    #             for x in d]
    # print(data1)
    mydata= zip(res1,datalen)
    return render(request, 'UserForm.html', {'data':mydata,'filedata':html,'htmltagdata':result,'value':value,'dropdownitem':mydropdown,'droplen':ln})
   
def userdetails(request):
    fieldName=request.session.get('fieldName')
    fieldID=request.session.get('fieldID')
    templateid=request.session.get('templateID')
    userID=request.session.get('userid')
    id = "{}".format(userID)
    templateID= "{}".format(templateid)
    print(type(id))
    print(fieldName)
    print(fieldID)
    x=[]
    if request.method == 'POST':
        for i in fieldName:
            print(i)
            firstName = request.POST.get(''+i+'')
            x.append(firstName)
            print(x)
        mode='1'
        factID='1'
        
        for x,fieldID in zip(x,fieldID):
            fieldID1= "{}".format(fieldID)
            print(fieldID1)
            print(type(fieldID1))
            str1 = 'https://localhost:44360/api/factdata/' + \
                factID + '/' + id + '/' + templateID + '/' + fieldID1 + '/' + x + '/' + mode 
            print(str1)
            res = requests.get(str1, verify=False).json()
            print(res)
        return userform(request)
    
def userdetails1(request):
    fieldName=request.session.get('fieldName')
    fieldID=request.session.get('fieldID')
    templateid=request.session.get('templateID')
    userID=request.session.get('userid')
    id = "{}".format(userID)
    templateID= "{}".format(templateid)
    print(type(id))
    print(fieldName)
    print(fieldID)
    x=[]
    if request.method == 'POST':
        for i in fieldName:
            print(i)
            firstName = request.POST.get(''+i+'')
            x.append(firstName)
            print(x)
        mode='1'
        factID='1'
        
        for x,fieldID in zip(x,fieldID):
            fieldID1= "{}".format(fieldID)
            print(fieldID1)
            print(type(fieldID1))
            str1 = 'https://localhost:44360/api/factdata/' + \
                factID + '/' + id + '/' + templateID + '/' + fieldID1 + '/' + x + '/' + mode 
            print(str1)
            res = requests.get(str1, verify=False).json()
            print(res)
        return userform1(request)   
    