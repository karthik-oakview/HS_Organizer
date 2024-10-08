from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
import os
from azure.storage.blob import BlobServiceClient
from . import db
import json
from .models import User, Credit, Honors, Volunteering, Job, Recommendation
from datetime import datetime
from datetime import date, datetime
from .keys import connect_str, account_key


container_name = "volunteerinfo"

views = Blueprint('views', __name__)

ROWS_PER_PAGE = 5

#******************************** Home  *************************************************************
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    hours=0
   # maxid = db.session.query(func.max(Volunteering.volunteer_seq))
    
    volunteerings = Volunteering.query.filter_by(user_id=current_user.id)

    for volunteering in volunteerings:
        hours+=volunteering.hours
    awardnum =0
    creditnum=0

    awards = Honors.query.filter_by(user_id=current_user.id)
    credits= Credit.query.filter_by(user_id=current_user.id)
    for award in awards:
        awardnum+=1
    for credit in credits:
        creditnum+=credit.credit_unit
    
    return render_template("home.html", user=current_user, hours=hours, creditnum=creditnum, awardnum=awardnum)
    

#********************************Display Function for Volunteering ***************************************** 
@views.route('/volunteering', methods=['GET','POST'])
@login_required
def volunteering():   
# this function is to display volunteering information. It selects all data from Volunteer table 
# for the logged in user
    try:                                                                                                 
        page = request.args.get('page', 1, type=int)
        print("hello")
        print(current_user.id)
        
        volunteerings = Volunteering.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=ROWS_PER_PAGE)
        print('rendering job')
        return render_template("volunteering.html", user=current_user, volunteerings=volunteerings)
        
    except Exception as exc:
        print(exc)        
    except:
        flash("An error has occured", category="error")

#********************************Display Function for jobs ********************************************
@views.route('/job', methods=['GET','POST'])
@login_required
def job():   
# this function is to display Job information. It selects all data from Job table 
# for the logged in user
    try:                                                                                                 
        page = request.args.get('page', 1, type=int)
        print("hello")
        print(current_user.id)
        
        jobs = Job.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=ROWS_PER_PAGE)
        print('rendering job')
        return render_template("job.html", user=current_user, jobs=jobs)
        
    except Exception as exc:
        print(exc)        
    except:
        flash("An error has occured", category="error")

#********************************Display Function for Recommendation ********************************************

@views.route('/recommendation', methods=['GET','POST'])
@login_required
def recommendation():   
# this function is to display Recommendation information. It selects all data from Recommendation table 
# for the logged in user

    try:                                                                                                 
        page = request.args.get('page', 1, type=int)
        print("hello")
        print(current_user.id)

        recommendations = Recommendation.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=ROWS_PER_PAGE)
        print('rendering recommendation')
        return render_template("recommendations.html", user=current_user, recommendations=recommendations)
        
    except Exception as exc:
        print(exc)        
    except:
        flash("An error has occured", category="error")

#********************************Display Method for Awards ********************************************
@views.route("/awards", methods=['GET', 'POST'])
@login_required
def showawards():
# this function is to display Awards information. It selects all data from Awards table 
# for the logged in user

    page = request.args.get('page', 1, type=int)
    print("hello")
    print(current_user.id)
        
    awards = Honors.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=ROWS_PER_PAGE)
        
    return render_template("awards.html", user=current_user,awards=awards)

#********************************Display Function for Credits ********************************************
@views.route("/show-credit", methods=['GET', 'POST'])
@login_required
def showcredit():
# this function is to display Credits information. It selects all data from Credits table 
# for the logged in user

    page = request.args.get('page', 1, type=int)
    print("hello")
    print(current_user.id)
        
    credits = Credit.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=ROWS_PER_PAGE)
    return render_template("showcredit.html", user=current_user,credits=credits)


#********************************Delete Function for Volunteering ********************************************
@views.route('/delete-volunteering', methods=['GET','POST'])
@login_required
def delete_volunteering():
# this function is to delete volunteering information. It deletes the selected row from Volunteering table 
# for the logged in user

    try:
        print('inside delete_volunteering')
        volunteeringid = request.args.get('volunteeringid')
        print(volunteeringid)
        volunteerings = Volunteering.query.get(volunteeringid)
        if volunteerings.user_id == current_user.id:
                print('success 2')
                db.session.delete(volunteerings)
                db.session.commit()
                print('deleted')
                return redirect(url_for('views.volunteering')) 
        
        return redirect(url_for('views.volunteering')) 
    except:
        flash("An error has occured", category="error") 

#********************************Delete Function for Jobs ********************************************
@views.route('/delete-job', methods=['GET','POST'])
@login_required
def delete_job():
# this function is to delete Job information. It deletes the selected row from Job table 
# for the logged in user

    try:
        print('inside delete_job')
        jobid = request.args.get('jobid')
        print(jobid)
        jobs = Job.query.get(jobid)
        if jobs.user_id == current_user.id:
                print('success 2')
                db.session.delete(jobs)
                db.session.commit()
                print('deleted')
                return redirect(url_for('views.job')) 
        
        return redirect(url_for('views.job')) 
    except:
        flash("An error has occured", category="error") 

#********************************Delete Function for Recommendation ********************************************

@views.route('/delete-recommendation', methods=['GET','POST'])
@login_required
def delete_recommendation():
# this function is to delete Recommendation information. It deletes the selected row from Recommendation table 
# for the logged in user

    try:
        print('inside delete_recommendation')
        recommendationid = request.args.get('recommendationid')
        print(recommendationid)
        recommends = Recommendation.query.get(recommendationid)
        if recommends.user_id == current_user.id:
                print('success 2')
                db.session.delete(recommends)
                db.session.commit()
                print('deleted')
                return redirect(url_for('views.recommendation')) 
        
        return redirect(url_for('views.recommendation')) 
    except:
        flash("An error has occured", category="error") 

#********************************Delete Function for Credits ********************************************
@views.route('/delete-credit', methods=['GET','POST'])
@login_required
def delete_credit():
# this function is to delete Credit information. It deletes the selected row from Credit table 
# for the logged in user

    try:
        print('inside delete_credit')
        creditid = request.args.get('creditid')
        print(creditid)
        credits = Credit.query.get(creditid)
        if credits.user_id == current_user.id:
                print('success 2')
                db.session.delete(credits)
                db.session.commit()
                print('deleted')
                return redirect(url_for('views.showcredit')) 
        
        return redirect(url_for('views.showcredit')) 
               # return render_template("volunteering.html", user=current_user, volunteerings=volunteerings)
        #return jsonify({}
        #return render_template("volunteering.html", user=current_user, volunteerings=volunteerings)
    except:
        flash("An error has occured", category="error") 


#********************************Delete Function for Awards ********************************************
@views.route('/delete-award', methods=['GET','POST'])
@login_required
def delete_award():
# this function is to delete Award information. It deletes the selected row from Awards table 
# for the logged in user

    try:
        print('inside delete_award')
        awardid = request.args.get('awardid')
        print(awardid)
        honors = Honors.query.get(awardid)
        if honors.user_id == current_user.id:
                print('success 2')
                db.session.delete(honors)
                db.session.commit()
                print('deleted')
                return redirect(url_for('views.showawards')) 
        
        return redirect(url_for('views.showawards')) 
               # return render_template("volunteering.html", user=current_user, volunteerings=volunteerings)
        #return jsonify({}
        #return render_template("volunteering.html", user=current_user, volunteerings=volunteerings)
    except:
        flash("An error has occured", category="error") 

#********************************Update Function for Volunteering ********************************************

@views.route('/update-volunteering', methods=['GET','POST'])
@login_required
def update_volunteering():
# this function is to update Volunteering information. It updates the selected row in Volunteering table
# for the logged in user

        if request.method == 'POST':
            orgName = request.form.get('orgName')
            orgEmail = request.form.get('orgEmail')
            hours = request.form.get('hours')
            activity =  request.form.get('activity')
            approver =request.form.get('approver')
            #date = datetime.strptime(request.form.get('date'),"%m-%d-%Y" )
            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            description= request.form.get('description')
        
            volunteeringid = request.args.get('volunteeringid')
            volunteering = Volunteering.query.get(volunteeringid)
            print(volunteeringid)
            print('update')
            volunteering.org_name=orgName
            volunteering.org_email=orgEmail
            volunteering.hours=hours 
            volunteering.activity=activity 
            volunteering.approver=approver 
            volunteering.date=date 
            volunteering.description=description
            db.session.commit()
            flash('Info updated!', category='success') 
            return redirect(url_for('views.volunteering')) 
   
        volunteeringid = request.args.get('volunteeringid')
        volunteering = Volunteering.query.get(volunteeringid)
        print('initial')
        print(volunteering.org_name)
        return render_template("update_volunteering.html", user=current_user, volunteering=volunteering)

#********************************Update Function for Jobs  ********************************************

@views.route('/update-job', methods=['GET','POST'])
@login_required
def update_job():
# This function is to update Job information. It updates the selected row in Jobs table
# for the logged in user

        if request.method == 'POST':
            orgName = request.form.get('orgName')
            orgEmail = request.form.get('orgEmail')
            hours = request.form.get('hours')
            role =  request.form.get('role')
            approver =request.form.get('approver')
            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            description= request.form.get('description')
        
            jobid = request.args.get('jobid')
            job = Job.query.get(jobid)
            print(jobid)
            print('update')
            job.org_name=orgName
            job.org_email=orgEmail
            job.hours=hours 
            job.role=role
            job.approver=approver 
            job.date=date 
            job.description=description
            db.session.commit()
            flash('Info updated!', category='success') 
            return redirect(url_for('views.job')) 
   
        jobid = request.args.get('jobid')
        job= Job.query.get(jobid)
        print('initial')
        print(job.org_name)
        return render_template("update_jobs.html", user=current_user, job=job)

#********************************Update Function for Recommendation  ********************************************

@views.route('/update-recommendation', methods=['GET','POST'])
@login_required
def update_recommendation():
# This function is to update Recommendation information. It updates the selected row in Recommendation table
# for the logged in user

        if request.method == 'POST':
            recommendName = request.form.get('recommendName')
            recommendEmail = request.form.get('recommendEmail')
            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            description= request.form.get('description')
        
            recommendationid = request.args.get('recommendationid')
            recommendation = Recommendation.query.get(recommendationid)
            print(recommendationid)
            print('update')
            recommendation.recommend_name=recommendName
            recommendation.recommend_email=recommendEmail
            recommendation.date=date 
            recommendation.description=description
            db.session.commit()
            flash('Info updated!', category='success') 
            return redirect(url_for('views.recommendation')) 
   
        recommendationid = request.args.get('recommendationid')
        recommendation = Recommendation.query.get(recommendationid)
        print('initial')
        print(recommendation.recommend_name)
        return render_template("update_recommendations.html", user=current_user, recommendation=recommendation)

#********************************Update function for Awards  ********************************************

@views.route('/update-award', methods=['GET','POST'])
@login_required
def update_award():
# This function is to update Awards information. It updates the selected row in Awards table
# for the logged in user

    if request.method == 'POST':
        org_name = request.form.get('orgName')
        award_name = request.form.get('honorName')
        date = datetime.strptime(request.form.get('receivedDate'),"%Y-%m-%d" )
        level = request.form.get('level')
        description = request.form.get('description')
    
        honor_seq = request.args.get('awardid')
        honor = Honors.query.get(honor_seq)

        honor.org_name=org_name    
        honor.award_name=award_name 
        honor.date=date 
        honor.level=level 
        honor.description=description
        
        db.session.commit()
        flash('Info updated!', category='success') 
        return redirect(url_for('views.showawards')) 

    honor_seq = request.args.get('awardid')
    honor = Honors.query.get(honor_seq)

    return render_template("updateaward.html", user=current_user, honor=honor)

#********************************Update Function for Credits  ********************************************


@views.route('/update-credit', methods=['GET','POST'])
@login_required
def update_credit():
# This function is to update Credits information. It updates the selected row in Credits table
# for the logged in user

    if request.method == 'POST':
        course_name = request.form.get('courseName')

        credit_unit= request.form.get('creditUnit')
        weightage = request.form.get('weightage')
        provider = request.form.get('provider')
        classification = request.form.get('classification')
        score = request.form.get('score')
        grade = request.form.get('grade')
    
        creditid = request.args.get('creditid')
        credit = Credit.query.get(creditid)

        credit.course_name=course_name
        credit.credit_unit=credit_unit
        credit.weightage=weightage
        credit.provider=provider
        credit.classification=classification
        credit.score=score
        credit.grade=grade
            
        db.session.commit()
        flash('Credit updated!', category='success') 
        return redirect(url_for('views.showcredit')) 

    creditid = request.args.get('creditid')
    credit = Credit.query.get(creditid)

    return render_template("updatecredit.html", user=current_user, credit=credit)


from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta


#******************************** Upload and download function for Volunteering  ********************************************

@views.route('/attach-volunteering', methods=['GET','POST'])
@login_required

def attach_volunteering():
# This function is to upload/download volunteering information. It uploads and downloads volunteering
# document from Azure Blob Storage.


    container_name = "volunteerinfo"
    volunteeringid = request.args.get('volunteeringid')
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
    try:
       container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored          container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
    print(volunteeringid)
    volunteering = Volunteering.query.get(volunteeringid)

    if request.method =='POST':
       print(request.form.get('Delete'))
             
       if request.form.get('Delete') == "Delete" :
          print("deleted")
          container_client.delete_blob(volunteering.docref)  
          volunteering.docref = ''
          db.session.commit()
       #print(request.args.get("submit"))
       #if request.form.get("submit") == "submit":
       else:
          print ("not delete")
          filenames = ""

          for file in request.files.getlist("document"):
           try:
             #file.filename  = 'volunteerdoc' + volunteeringid + '.pdf'
             print(file.filename)
             full_file_name = volunteeringid + '/' + file.filename
             print(full_file_name)
             container_client.upload_blob(full_file_name, file) # upload the file to the container using the filename as the blob name
             volunteering.docref =  full_file_name
             db.session.commit()
             filenames += file.filename + "<br /> "
             print('document loaded')

           except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
          flash('Document uploaded!', category='success') 
#         return "<p>Uploaded: <br />{}</p>".format(filenames)
    
    blob_name=volunteering.docref
    blob_url_with_blob_sas_token=''
    print(volunteering.docref)
    if volunteering.docref is not None and volunteering.docref != '':
        blob_sas_token = generate_blob_sas(
        account_name='studenthelpblob',
        container_name='volunteerinfo',
        blob_name=volunteering.docref,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1))
    
        blob_url_with_blob_sas_token = f"https://studenthelpblob.blob.core.windows.net/volunteerinfo/{blob_name}?{blob_sas_token}"
    
    print(blob_url_with_blob_sas_token)
    return render_template("upload_volunteering.html", user=current_user, volunteeringid=volunteeringid,blob_url_with_blob_sas_token=blob_url_with_blob_sas_token)

#******************************** Upload and download function for Awards ********************************************

@views.route('/attach-award', methods=['GET','POST'])
@login_required

def attach_award():
# This function is to upload/download Award information. It uploads and downloads Awards
# document from Azure Blob Storage.

    container_name = "awards"
    awardid = request.args.get('awardid')
    print('award id 1')
    print(awardid)
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
    try:
       container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored          container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
    honor = Honors.query.get(awardid)
    print(honor)
    if request.method =='POST':
       print(request.form.get('Delete'))
             
       if request.form.get('Delete') == "Delete" :
          print("deleted")
          container_client.delete_blob(honor.docref)  
          honor.docref = ''
          db.session.commit()
       #print(request.args.get("submit"))
       #if request.form.get("submit") == "submit":
       else:
          print ("not delete")
          filenames = ""

          for file in request.files.getlist("document"):
           try:
             #file.filename  = 'volunteerdoc' + volunteeringid + '.pdf'
             print(file.filename)
             full_file_name = awardid + '/' + file.filename
             print(full_file_name)
             container_client.upload_blob(full_file_name, file) # upload the file to the container using the filename as the blob name
             honor.docref =  full_file_name
             db.session.commit()
             filenames += file.filename + "<br /> "
             print('document loaded')

           except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
          flash('Document uploaded!', category='success') 
#         return "<p>Uploaded: <br />{}</p>".format(filenames)
    
    blob_name=honor.docref
    blob_url_with_blob_sas_token=''
    print(honor.docref)
    if honor.docref is not None and honor.docref != '':
        blob_sas_token = generate_blob_sas(
        account_name='studenthelpblob',
        container_name='awards',
        blob_name=honor.docref,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1))
    
        blob_url_with_blob_sas_token = f"https://studenthelpblob.blob.core.windows.net/awards/{blob_name}?{blob_sas_token}"
    
    print(blob_url_with_blob_sas_token)
    print('returning')
    print(awardid)
    return render_template("upload_awards.html", user=current_user, awardid=awardid,blob_url_with_blob_sas_token=blob_url_with_blob_sas_token)

#******************************** Upload and download function for Credits  ********************************************

@views.route('/attach-credit', methods=['GET','POST'])
@login_required

def attach_credit():
# This function is to upload/download Credit information. It uploads and downloads Credits
# document from Azure Blob Storage.

    container_name = "credits"
    creditid = request.args.get('creditid')
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
    try:
       container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored          container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
    print('credit id first')    
    print(creditid)
    credit = Credit.query.get(creditid)
    print(credit)
    if request.method =='POST':
       print(request.form.get('Delete'))
             
       if request.form.get('Delete') == "Delete" :
          print("deleted")
          container_client.delete_blob(credit.docref)  
          credit.docref = ''
          db.session.commit()
       #print(request.args.get("submit"))
       #if request.form.get("submit") == "submit":
       else:
          print ("not delete")
          filenames = ""

          for file in request.files.getlist("document"):
           try:
             #file.filename  = 'volunteerdoc' + volunteeringid + '.pdf'
             print(file.filename)
             full_file_name = creditid + '/' + file.filename
             print(full_file_name)
             container_client.upload_blob(full_file_name, file) # upload the file to the container using the filename as the blob name
             credit.docref =  full_file_name
             db.session.commit()
             filenames += file.filename + "<br /> "
             print('document loaded')

           except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
          flash('Document uploaded!', category='success') 
#         return "<p>Uploaded: <br />{}</p>".format(filenames)
    
    blob_name=credit.docref
    blob_url_with_blob_sas_token=''
    print(credit.docref)
    if credit.docref is not None and credit.docref != '':
        blob_sas_token = generate_blob_sas(
        account_name='studenthelpblob',
        container_name='credits',
        blob_name=credit.docref,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1))
    
        blob_url_with_blob_sas_token = f"https://studenthelpblob.blob.core.windows.net/credits/{blob_name}?{blob_sas_token}"
    
    print('creditid after')
    print(creditid)
    print(blob_url_with_blob_sas_token)
    return render_template("upload_credit.html", user=current_user, creditid=creditid,blob_url_with_blob_sas_token=blob_url_with_blob_sas_token)


#******************************** Upload and download function for Jobs  ********************************************

@views.route('/attach-job', methods=['GET','POST'])
@login_required
def attach_job():
# This function is to upload/download Job information. It uploads and downloads Job
# document from Azure Blob Storage.

    container_name = "jobs"
    jobid = request.args.get('jobid')
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
    try:
       container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored          container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
    print('job id first')    
    print(jobid)
    job= Job.query.get(jobid)
    print(job)
    if request.method =='POST':
       print(request.form.get('Delete'))
             
       if request.form.get('Delete') == "Delete" :
          print("deleted")
          container_client.delete_blob(job.docref)  
          job.docref = ''
          db.session.commit()
       #print(request.args.get("submit"))
       #if request.form.get("submit") == "submit":
       else:
          print ("not delete")
          filenames = ""

          for file in request.files.getlist("document"):
           try:
             #file.filename  = 'volunteerdoc' + volunteeringid + '.pdf'
             print(file.filename)
             full_file_name = jobid + '/' + file.filename
             print(full_file_name)
             container_client.upload_blob(full_file_name, file) # upload the file to the container using the filename as the blob name
             job.docref =  full_file_name
             db.session.commit()
             filenames += file.filename + "<br /> "
             print('document loaded')

           except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
          flash('Document uploaded!', category='success') 
#         return "<p>Uploaded: <br />{}</p>".format(filenames)
    
    blob_name=job.docref
    blob_url_with_blob_sas_token=''
    print(job.docref)
    if job.docref is not None and job.docref != '':
        blob_sas_token = generate_blob_sas(
        account_name='studenthelpblob',
        container_name='jobs',
        blob_name=job.docref,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1))
    
        blob_url_with_blob_sas_token = f"https://studenthelpblob.blob.core.windows.net/jobs/{blob_name}?{blob_sas_token}"
    
    print('jobid after')
    print(jobid)
    print(blob_url_with_blob_sas_token)
    return render_template("upload_jobs.html", user=current_user, jobid=jobid,blob_url_with_blob_sas_token=blob_url_with_blob_sas_token)

#******************************** Upload and download function for Recommendation ********************************************

@views.route('/attach-recommendation', methods=['GET','POST'])
@login_required
def attach_recommendation():

# This function is to upload/download Recommendation information. It uploads and downloads recommendation
# document from Azure Blob Storage.

    container_name = "recommendations"
    recommendationid = request.args.get('recommendationid')
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account
    try:
       container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored          container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
    except Exception as e:
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist
    print('recommendation id first')    
    print(recommendationid)
    recommendation= Recommendation.query.get(recommendationid)
    print(recommendation)
    if request.method =='POST':
       print(request.form.get('Delete'))
             
       if request.form.get('Delete') == "Delete" :
          print("deleted")
          container_client.delete_blob(recommendation.docref)  
          recommendation.docref = ''
          db.session.commit()
       #print(request.args.get("submit"))
       #if request.form.get("submit") == "submit":
       else:
          print ("not delete")
          filenames = ""

          for file in request.files.getlist("document"):
           try:
             #file.filename  = 'volunteerdoc' + volunteeringid + '.pdf'
             print(file.filename)
             full_file_name = recommendationid + '/' + file.filename
             print(full_file_name)
             container_client.upload_blob(full_file_name, file) # upload the file to the container using the filename as the blob name
             recommendation.docref =  full_file_name
             db.session.commit()
             filenames += file.filename + "<br /> "
             print('document loaded')

           except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
          flash('Document uploaded!', category='success') 
#         return "<p>Uploaded: <br />{}</p>".format(filenames)
    
    blob_name=recommendation.docref
    blob_url_with_blob_sas_token=''
    print(recommendation.docref)
    if recommendation.docref is not None and recommendation.docref != '':
        blob_sas_token = generate_blob_sas(
        account_name='studenthelpblob',
        container_name='recommendations',
        blob_name=recommendation.docref,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1))
    
        blob_url_with_blob_sas_token = f"https://studenthelpblob.blob.core.windows.net/recommendations/{blob_name}?{blob_sas_token}"
    
    print('recommendation ID after')
    print(recommendationid)
    print(blob_url_with_blob_sas_token)
    return render_template("upload_recommendations.html", user=current_user, recommendationid=recommendationid,blob_url_with_blob_sas_token=blob_url_with_blob_sas_token)


#******************************** Add function for Volunteering  ********************************************
@views.route('/add-volunteering', methods=['GET','POST'])
@login_required
def add_volunteering():

# This function is to add Volunteering information. It saves the new row to the Volunteer table.

    try:
        print(request.method)
        if request.method == 'POST':
            orgName = request.form.get('orgName')
            orgEmail= request.form.get('orgEmail')
            hours = request.form.get('hours')
            activity =  request.form.get('activity')
            approver =request.form.get('approver')

            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            #date = datetime.strptime(request.form.get('date'),"%m-%d-%Y" )
            description= request.form.get('description')
            maxid = db.session.query(func.max(Volunteering.volunteer_seq))
            print(maxid)
         
            if (maxid.scalar() is not None): 
                id  =  maxid.scalar() + 1
            else:
                id = 1
            print(current_user)
            usera  = str(current_user).split(' ')
            print(usera[1])
            userid = str(usera[1]).split('>')                

            new_volunteering = Volunteering(volunteer_seq=id,org_name=orgName,org_email=orgEmail, activity=activity, approver=approver, date=date, description=description, hours=hours,user_id=userid[0])
            db.session.add(new_volunteering)
            db.session.commit()
            flash('Volunteering info added!', category='success')
            
            return redirect(url_for('views.volunteering')) 

        return render_template("addvolunteer.html", user=current_user)
    except Exception as exc:
        print(exc)
    except:
        flash("An error has occured", category="error")

#******************************** Add function for Jobs  ********************************************

@views.route('/add-job', methods=['GET','POST'])
@login_required
def add_job():
# This function is to add Job information. It saves the new row to the Job table.
    try:
        print(request.method)
        if request.method == 'POST':
            orgName = request.form.get('orgName')
            orgEmail= request.form.get('orgEmail')
            hours = request.form.get('hours')
            role =  request.form.get('role')
            approver =request.form.get('approver')
            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            description= request.form.get('description')
            maxid = db.session.query(func.max(Job.job_seq))
            print(maxid)
         
            if (maxid.scalar() is not None): 
                id  =  maxid.scalar() + 1
            else:
                id = 1
            print(current_user)
            usera  = str(current_user).split(' ')
            print(usera[1])
            userid = str(usera[1]).split('>')                

            new_job = Job(job_seq=id,org_name=orgName,org_email=orgEmail, role=role, approver=approver, date=date, description=description, hours=hours,user_id=userid[0])
            db.session.add(new_job)
            db.session.commit()
            flash('Job info added!', category='success')
            
            return redirect(url_for('views.job')) 

        return render_template("addjob.html", user=current_user)
    except Exception as exc:
        print(exc)
    except:
        flash("An error has occured", category="error")

#******************************** Add function for Recommendations  ********************************************

@views.route('/add-recommendation', methods=['GET','POST'])
@login_required
def add_recommendation():
# This function is to add Recommendation information. It saves the new row to the Recommendation table.

    try:
        print(request.method)
        if request.method == 'POST':
            recommendName = request.form.get('recommendName')
            recommendEmail= request.form.get('recommendEmail')
            date = datetime.strptime(request.form.get('date'),"%Y-%m-%d" )
            description= request.form.get('description')
            maxid = db.session.query(func.max(Recommendation.recommend_seq))
            print(maxid)
         
            if (maxid.scalar() is not None): 
                id  =  maxid.scalar() + 1
            else:
                id = 1
            print(current_user)
            usera  = str(current_user).split(' ')
            print(usera[1])
            userid = str(usera[1]).split('>')                

            new_recommendation = Recommendation(recommend_seq=id,recommend_name=recommendName,recommend_email=recommendEmail,  date=date, description=description,user_id=userid[0])
            db.session.add(new_recommendation)
            db.session.commit()
            flash('Recommendation info added!', category='success')
            
            return redirect(url_for('views.recommendation')) 

        return render_template("addrecommendations.html", user=current_user)
    except Exception as exc:
        print(exc)
    except:
        flash("An error has occured", category="error")

#******************************** Add function for Credits ********************************************

@views.route("/add-credit", methods=['GET', 'POST'])
@login_required
def addcredit():
# This function is to add Credit information. It saves the new row to the Credits table.
    print(request.method)
    if request.method == 'POST':
        course_name = request.form.get('courseName')
        credit_unit= request.form.get('creditUnit')
        weightage = request.form.get('weightage')
        provider = request.form.get('provider')
        classification = request.form.get('classification')
        score = request.form.get('score')
        grade = request.form.get('grade')

        maxid = db.session.query(func.max(Credit.creditid))
         
        if (maxid.scalar() is not None): 
            id  =  maxid.scalar() + 1
        else:
            id = 1
        creditid=id
        print(creditid)
        print(current_user)
        usera  = str(current_user).split(' ')
        print(usera[1])
        user_id = str(usera[1]).split('>')                
        print(usera[1])
        print(user_id)

        credit = Credit(creditid=creditid,course_name=course_name, credit_unit=credit_unit, weightage=weightage,provider=provider,classification=classification,score=score,grade=grade,user_id=user_id[0])
        db.session.add(credit)
        db.session.commit()
        flash('Credit added!', category='success')
        return redirect(url_for('views.showcredit'))

    return render_template("addcredit.html", user=current_user)

#******************************** Add function for Awards ********************************************

@views.route("/add-award", methods=['GET', 'POST'])
@login_required
def addaward():
# This function is to add Award information. It saves the new row to the Awards table.
    print(request.method)
    if request.method == 'POST':
        org_name = request.form.get('orgName')
        award_name = request.form.get('honorName')
        date = datetime.strptime(request.form.get('receivedDate'),"%Y-%m-%d" )
        level = request.form.get('level')
        description = request.form.get('description')

        maxid = db.session.query(func.max(Honors.honors_seq))
         
        if (maxid.scalar() is not None): 
            id  =  maxid.scalar() + 1
        else:
            id = 1
        honors_seq=id
        print(current_user)
        usera  = str(current_user).split(' ')
        print(usera[1])
        user_id = str(usera[1]).split('>')                
        print(usera[1])
        print(user_id)

        honor = Honors(honors_seq=honors_seq,org_name=org_name, award_name=award_name, date=date, level=level, description=description,user_id=user_id[0])
        db.session.add(honor)
        db.session.commit()
        flash('Award added!', category='success')
        return redirect(url_for('views.showawards'))

    return render_template("addaward.html", user=current_user)


