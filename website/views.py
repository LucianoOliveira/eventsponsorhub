from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Flask, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from .models import Users, Events, Packages, UserRequests
from . import db
import json, os, threading
from datetime import datetime, date, timedelta
from sqlalchemy import and_, func, cast, String, text, desc, case, literal_column
from PIL import Image
from io import BytesIO
import shutil

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    try:
        result_data = Events.query.order_by(Events.ev_date.desc()).all()
    except Exception as e:
        print(f"Error: {e}")
    return render_template("index.html", user=current_user, result=result_data)

@views.route('/userInfo/<int:user_id>', methods=['GET', 'POST'])
@login_required
def userInfo(p_user_id):
    pass_user = Users.query.get_or_404(p_user_id)
    return render_template("user_info.html", user=current_user, p_user=pass_user)

@views.route('/userOwnInfo', methods=['GET', 'POST'])
@login_required
def userOwnInfo():
    return render_template("user_own_info.html", user=current_user)

# management
@views.route('/managementEvents', methods=['GET', 'POST'])
@login_required
def managementEvents():
    result_data = Events.query.filter_by(ev_user_id=current_user.us_id).order_by(Events.ev_date.desc()).all()
    return render_template("managementEvents.html", user=current_user, result=result_data)

@views.route('/managementUsersSU', methods=['GET', 'POST'])
@login_required
def managementUsersSU():
    result_data = Users.query.order_by(Users.us_id.desc()).all()
    return render_template("managementUsersSU.html", user=current_user, result=result_data)

@views.route('/managementUsersAdmin', methods=['GET', 'POST'])
@login_required
def managementUsersAdmin():
    result_data = Users.query.filter(Users.us_is_admin == 0, Users.us_is_superuser == 0).order_by(Users.us_id.desc()).all()
    return render_template("managementUsersAdmin.html", user=current_user, result=result_data)

# current user management
@views.route('/updateOwnUser', methods=['GET', 'POST'])
@login_required
def updateOwnUser():
    user_id = current_user.us_id
    user_Name = request.form.get('user_name')
    user_Email = request.form.get('user_email')
    user_birthday = request.form.get('user_birthday')
    
    if request.form.get('user_active') == 'on':
        user_is_active = 1
    else:
        user_is_active = 0

    if request.form.get('user_buyer') == 'on':
        user_is_buyer = 1
    else:
        user_is_buyer = 0

    if request.form.get('user_seller') == 'on':
        user_is_seller = 1
    else:
        user_is_seller = 0

    if request.form.get('user_admin') == 'on':
        user_is_admin = 1
    else:
        user_is_admin = 0

    if request.form.get('user_superuser') == 'on':
        user_is_superuser = 1
    else:
        user_is_superuser = 0
    # user_Photo = request.form.get('user_photo')
    
    # Update User
    try:
        db.session.execute(
        text(f"UPDATE tb_users SET us_name=:user_Name, us_email=:user_Email, us_birthday=:user_birthday, us_is_active=:user_is_active, us_is_buyer=:user_is_buyer, us_is_seller=:user_is_seller, us_is_admin=:user_is_admin, us_is_superuser=:user_is_superuser WHERE us_id=:user_id"),
            {"user_Name": user_Name, "user_Email": user_Email, "user_id": user_id, "user_birthday": user_birthday, "user_is_active": user_is_active, "user_is_buyer": user_is_buyer, "user_is_seller": user_is_seller, "user_is_admin": user_is_admin, "user_is_superuser": user_is_superuser}
        )
        db.session.commit()
    except Exception as e:
        print("Error: " + str(e))

    # Insert photo of user
    image = request.files['user_photo']
    if image and user_id>0:
        #image is found")
        # path = 'website/static/photos/users/'+str(user_id)+'/'
        path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(user_id)+'/'
        pathRelative = 'static\\photos\\users\\'+str(user_id)+'\\'
        filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(user_id)+'/main.jpg'
                
        # Check if directory exists, if not, create it.
        if os.path.exists(path) == False:
            #print('Dir path not found')
            os.mkdir(path)
        # Check if main.jpg exists, if exists delete it
        if os.path.exists(filePath) == True:
            os.remove(filePath)
        
        # Upload image to directory
        fileName = 'main.jpg'
        basedir = os.path.abspath(os.path.dirname(__file__))
        #print(f"basedir: {basedir}")
        #print(f"filePath: {filePath}")
        newPath = os.path.join(basedir, pathRelative, fileName)
        # image.save(newPath)
        image.save(filePath)
        #print("image saved")


    return render_template("user_own_info.html", user=current_user)


# user management by id
@views.route('/updateUser/<int:userID>', methods=['GET', 'POST'])
@login_required
def updateUser(userID):
    user_id = userID
    pass_user = Users.query.get_or_404(userID)
    user_Name = request.form.get('user_name')
    user_Email = request.form.get('user_email')
    user_birthday = request.form.get('user_birthday')
    
    if request.form.get('user_active') == 'on':
        user_is_active = 1
    else:
        user_is_active = 0

    if request.form.get('user_buyer') == 'on':
        user_is_buyer = 1
    else:
        user_is_buyer = 0

    if request.form.get('user_seller') == 'on':
        user_is_seller = 1
    else:
        user_is_seller = 0

    if request.form.get('user_admin') == 'on':
        user_is_admin = 1
    else:
        user_is_admin = 0

    if request.form.get('user_superuser') == 'on':
        user_is_superuser = 1
    else:
        user_is_superuser = 0
    # Update User
    try:
        db.session.execute(
        text(f"UPDATE tb_users SET us_name=:user_Name, us_email=:user_Email, us_birthday=:user_birthday, us_is_active=:user_is_active, us_is_buyer=:user_is_buyer, us_is_seller=:user_is_seller, us_is_admin=:user_is_admin, us_is_superuser=:user_is_superuser WHERE us_id=:user_id"),
            {"user_Name": user_Name, "user_Email": user_Email, "user_id": user_id, "user_birthday": user_birthday, "user_is_active": user_is_active, "user_is_buyer": user_is_buyer, "user_is_seller": user_is_seller, "user_is_admin": user_is_admin, "user_is_superuser": user_is_superuser}
        )
        db.session.commit()
    except Exception as e:
        print("Error: " + str(e))

    # Insert photo of user
    image = request.files['user_photo']
    if image and user_id>0:
        #image is found")
        # path = 'website/static/photos/users/'+str(user_id)+'/'
        path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(user_id)+'/'
        pathRelative = 'static\\photos\\users\\'+str(user_id)+'\\'
        filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(user_id)+'/main.jpg'
                
        # Check if directory exists, if not, create it.
        if os.path.exists(path) == False:
            #print('Dir path not found')
            os.mkdir(path)
        # Check if main.jpg exists, if exists delete it
        if os.path.exists(filePath) == True:
            os.remove(filePath)
        
        # Upload image to directory
        fileName = 'main.jpg'
        basedir = os.path.abspath(os.path.dirname(__file__))
        #print(f"basedir: {basedir}")
        #print(f"filePath: {filePath}")
        newPath = os.path.join(basedir, pathRelative, fileName)
        # image.save(newPath)
        image.save(filePath)
        #print("image saved")


    # return render_template("user_info.html", user=current_user, p_user=pass_user)
    return redirect(url_for('views.managementUsersSU'))


@views.route('/saveUserChanges', methods=['POST'])
@login_required
def saveUserChanges():
    for user in Users.query.all():
        user.us_is_buyer = 'us_is_buyer_' + str(user.us_id) in request.form
        user.us_is_seller = 'us_is_seller_' + str(user.us_id) in request.form
        user.us_is_admin = 'us_is_admin_' + str(user.us_id) in request.form
        user.us_is_active = 'us_is_active_' + str(user.us_id) in request.form
        user.us_is_superuser = 'us_is_superuser_' + str(user.us_id) in request.form
    db.session.commit()
    return redirect(url_for('views.managementUsersSU'))

@views.route('/editUser/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editUser(user_id):
    p_user = Users.query.get_or_404(user_id)
    
    return render_template('user_info.html', user=current_user, p_user=p_user)

#tools
def crop_image_in_memory(filePath):
    img = Image.open(filePath)
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) / 2
    top = (height - min_dim) / 2
    right = (width + min_dim) / 2
    bottom = (height + min_dim) / 2
    img = img.crop((left, top, right, bottom))
    return img

@views.route('/display_user_image/<userID>')
def display_user_image(userID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(userID)+'/main.jpg'
    if os.path.isfile(filePath):
        img = crop_image_in_memory(filePath)
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='photos/users/nophoto.jpg'), code=301)

@views.route('/display_event_main_image/<eventID>')
def display_event_main_image(eventID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(eventID)+'/main.jpg'
    if os.path.isfile(filePath):
        img = crop_image_in_memory(filePath)
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='photos/01_events/nophoto.jpg'), code=301)
    
@views.route('/display_event_second_image/<eventID>')
def display_event_second_image(eventID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(eventID)+'/secondary/1.jpg'
    if os.path.isfile(filePath):
        img = crop_image_in_memory(filePath)
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='photos/01_events/nophoto.jpg'), code=301)

@views.route('/display_package_main_image/<int:eventID>/<int:packageID>')
def display_package_main_image(eventID, packageID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(eventID)+'/packages/'+str(packageID)+'/main.jpg'
    if os.path.isfile(filePath):
        img = crop_image_in_memory(filePath)
        img_io = BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('static', filename='photos/01_events/nophoto.jpg'), code=301)

@views.route('/events', methods=['GET'])
def list_events():
    events = Events.query.filter(Events.ev_date >= datetime.now()).order_by(Events.ev_date).all()
    return render_template('events.html', events=events)

@views.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        ev_date = request.form.get('ev_date')
        ev_date = datetime.strptime(ev_date, '%Y-%m-%d')
        ev_expected_attendance = request.form.get('ev_expected_attendance')
        ev_instagram = request.form.get('ev_instagram')
        ev_facebook = request.form.get('ev_facebook')
        ev_youtube = request.form.get('ev_youtube')
        ev_tiktok = request.form.get('ev_tiktok')
        user_id = current_user.us_id  # Get the ID of the currently logged-in user

        new_event = Events(
            ev_title=title,
            ev_description=description,
            ev_location=location,
            ev_date=ev_date,
            ev_expected_attendance=ev_expected_attendance,
            ev_instagram=ev_instagram,
            ev_facebook=ev_facebook,
            ev_youtube=ev_youtube,
            ev_tiktok=ev_tiktok,
            ev_user_id=user_id
        )
        db.session.add(new_event)
        db.session.commit()
        ev_id = new_event.ev_id

        # register main photo
        image = request.files['ev_main_photo']
        if image and ev_id>0:
            #image is found")
            # path = 'website/static/photos/01_events/'+str(ev_id)+'/'
            path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(ev_id)+'/'
            pathRelative = 'static\\photos\\01_events\\'+str(ev_id)+'\\'
            filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(ev_id)+'/main.jpg'
                    
            # Check if directory exists, if not, create it.
            if os.path.exists(path) == False:
                #print('Dir path not found')
                os.mkdir(path)
            # Check if main.jpg exists, if exists delete it
            if os.path.exists(filePath) == True:
                os.remove(filePath)
            
            # Upload image to directory
            fileName = 'main.jpg'
            basedir = os.path.abspath(os.path.dirname(__file__))
            #print(f"basedir: {basedir}")
            #print(f"filePath: {filePath}")
            newPath = os.path.join(basedir, pathRelative, fileName)
            # image.save(newPath)
            image.save(filePath)
            #print("image saved")

        # register secondary photos
        secondary_photos = request.files.getlist('ev_secondary_photos')
        secondary_path = os.path.join(path, 'secondary')
        if not os.path.exists(secondary_path):
            os.mkdir(secondary_path)
        for idx, photo in enumerate(secondary_photos, start=1):
            photo_path = os.path.join(secondary_path, f'{idx}.jpg')
            photo.save(photo_path)

        return redirect(url_for('views.managementEvents'))
    return render_template('create_event.html', user=current_user)

@views.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Events.query.get_or_404(event_id)
    if request.method == 'POST':
        event.ev_title = request.form.get('ev_title')
        event.ev_description = request.form.get('ev_description')
        event.ev_location = request.form.get('ev_location')
        if request.form.get('ev_date'):
            event.ev_date = datetime.strptime(request.form.get('ev_date'), '%Y-%m-%d')
        event.ev_expected_attendance = request.form.get('ev_expected_attendance')
        event.ev_instagram = request.form.get('ev_instagram')
        event.ev_facebook = request.form.get('ev_facebook')
        event.ev_youtube = request.form.get('ev_youtube')
        event.ev_tiktok = request.form.get('ev_tiktok')

        # Update main photo if a new one is provided
        image = request.files['ev_main_photo']
        if image:
            path = str(os.path.abspath(os.path.dirname(__file__))) + '/static/photos/01_events/' + str(event.ev_id) + '/'
            filePath = path + 'main.jpg'
            if os.path.exists(filePath):
                os.remove(filePath)
            image.save(filePath)

        # Update secondary photos if new ones are provided
        secondary_photos = request.files.getlist('ev_secondary_photos')
        if secondary_photos:
            secondary_path = str(os.path.abspath(os.path.dirname(__file__))) + '/static/photos/01_events/' + str(event.ev_id) + '/secondary/'
            if not os.path.exists(secondary_path):
                os.mkdir(secondary_path)
            else:
                for file in os.listdir(secondary_path):
                    file_path = os.path.join(secondary_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            for idx, photo in enumerate(secondary_photos, start=1):
                photo_path = os.path.join(secondary_path, f'{idx}.jpg')
                photo.save(photo_path)

        db.session.commit()
        return redirect(url_for('views.managementEvents'))
    # Format the date to YYYY-MM-DD
    if event.ev_date:
        event_date = event.ev_date.strftime('%Y-%m-%d')
    #     event.ev_date = event.ev_date.strftime('%Y-%m-%d')
    # Fetch secondary photos
    secondary_photos_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(event.ev_id), 'secondary')
    if os.path.exists(secondary_photos_path):
        secondary_photos = [photo for photo in os.listdir(secondary_photos_path) if photo.endswith('.jpg')]
    else:
        secondary_photos = []
    # load existing packages
    with db.session.no_autoflush:
        packages = Packages.query.filter_by(pk_event_id=event_id).all()
    return render_template('edit_event.html', user=current_user, event=event, secondary_photos=secondary_photos, result_packages=packages, event_date=event_date)

@views.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Events.query.get_or_404(event_id)
    packages = Packages.query.filter_by(pk_event_id=event_id).all()
    if packages:
        flash("Delete not allowed, there are still packages associated with the event!", "error")
        return redirect(url_for('views.edit_event', event_id=event_id))
    db.session.delete(event)
    db.session.commit()
    # Delete event folder and its contents
    event_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(event_id))
    if os.path.exists(event_folder):
        shutil.rmtree(event_folder)
    return redirect(url_for('views.managementEvents'))

@views.route('/create_package/<int:event_id>', methods=['GET', 'POST'])
@login_required
def create_package(event_id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        allow_requests = request.form.get('allow_requests') == 'on'
        user_id = current_user.us_id  # Get the ID of the currently logged-in user
        new_package = Packages(pk_event_id=event_id, pk_title=title, pk_description=description, pk_price=price, pk_allow_requests=allow_requests, pk_user_id=user_id)
        db.session.add(new_package)
        db.session.commit()
        pk_new_id = new_package.pk_id
        
        # Increase the package count in the event table
        event = Events.query.get_or_404(event_id)
        event.ev_package_count = event.ev_package_count + 1 if event.ev_package_count else 1
        db.session.commit()

        # register main photo
        image = request.files['pk_main_photo']
        if image and pk_new_id>0:
            #image is found")
            # path = 'website/static/photos/01_events/'+str(ev_id)+'/'
            path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(event_id)+'/packages/'+str(pk_new_id)+'/'
            pathRelative = 'static\\photos\\01_events\\'+str(event_id)+'\\packages\\'+str(pk_new_id)+'\\'
            filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/01_events/'+str(event_id)+'/packages/'+str(pk_new_id)+'/main.jpg'
                    
            # Check if directory exists, if not, create it.
            if not os.path.exists(path):
                os.makedirs(path)
            # Check if main.jpg exists, if exists delete it
            if os.path.exists(filePath):
                os.remove(filePath)
            
            # Upload image to directory
            fileName = 'main.jpg'
            basedir = os.path.abspath(os.path.dirname(__file__))
            #print(f"basedir: {basedir}")
            #print(f"filePath: {filePath}")
            newPath = os.path.join(basedir, pathRelative, fileName)
            # image.save(newPath)
            image.save(filePath)
            #print("image saved")

        # register secondary photos
        secondary_photos = request.files.getlist('pk_secondary_photos')
        secondary_path = os.path.join(path, 'secondary')
        if not os.path.exists(secondary_path):
            os.makedirs(secondary_path)
        for idx, photo in enumerate(secondary_photos, start=1):
            photo_path = os.path.join(secondary_path, f'{idx}.jpg')
            photo.save(photo_path)

        # Fetch secondary event photos
        secondary_event_photos_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(event_id), 'secondary')
        if os.path.exists(secondary_event_photos_path):
            secondary_event_photos = [photo for photo in os.listdir(secondary_event_photos_path) if photo.endswith('.jpg')]
        else:
            secondary_event_photos = []
        return redirect(url_for('views.edit_event', user=current_user, event_id=event_id, secondary_photos=secondary_event_photos))
    return render_template('create_package.html', user=current_user, event_id=event_id)

@views.route('/edit_package/<int:package_id>', methods=['GET', 'POST'])
@login_required
def edit_package(package_id):
    package = Packages.query.get_or_404(package_id)
    if request.method == 'POST':
        package.pk_title = request.form.get('title')
        package.pk_description = request.form.get('description')
        package.pk_price = request.form.get('price')
        package.pk_allow_requests = request.form.get('allow_requests') == 'on'
        db.session.commit()
        return redirect(url_for('views.edit_event', event_id=package.pk_event_id))
    # Fetch secondary package photos
    secondary_package_photos_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(package.pk_event_id), 'packages', str(package.pk_id), 'secondary')
    if os.path.exists(secondary_package_photos_path):
        secondary_package_photos = [photo for photo in os.listdir(secondary_package_photos_path) if photo.endswith('.jpg')]
    else:
        secondary_package_photos = []
    return render_template('edit_package.html', user=current_user, package=package, secondary_photos=secondary_package_photos)

@views.route('/delete_package/<int:package_id>', methods=['POST'])
@login_required
def delete_package(package_id):
    package = Packages.query.get_or_404(package_id)
    event_id = package.pk_event_id
    db.session.delete(package)
    db.session.commit()

    # Decrease the package count in the event table
    event = Events.query.get_or_404(event_id)
    if event.ev_package_count and event.ev_package_count > 0:
        event.ev_package_count -= 1
    db.session.commit()

    # Delete package folder and its contents
    package_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(package.pk_event_id), 'packages', str(package.pk_id))
    if os.path.exists(package_folder):
        shutil.rmtree(package_folder)

    return redirect(url_for('views.edit_event', event_id=event_id))


@views.route('/detail_event/<int:event_id>', methods=['GET'])
def detail_event(event_id):
    event = Events.query.get_or_404(event_id)
    # Format the date to YYYY-MM-DD
    # if event.ev_date:
    #     event.ev_date = event.ev_date.strftime('%Y-%m-%d')
    # Fetch secondary photos
    secondary_photos_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(event.ev_id), 'secondary')
    if os.path.exists(secondary_photos_path):
        secondary_photos = [photo for photo in os.listdir(secondary_photos_path) if photo.endswith('.jpg')]
    else:
        secondary_photos = []
    # load existing packages
    with db.session.no_autoflush:
        packages = Packages.query.filter_by(pk_event_id=event_id).all()
    return render_template('detail_event.html', user=current_user, event=event, secondary_photos=secondary_photos, result_packages=packages)

@views.route('/detail_package/<int:package_id>', methods=['GET'])
def detail_package(package_id):
    package = Packages.query.get_or_404(package_id)

    # Fetch secondary photos
    secondary_package_photos_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos/01_events', str(package.pk_event_id), 'packages', str(package.pk_id), 'secondary')
    if os.path.exists(secondary_package_photos_path):
        secondary_photos = [photo for photo in os.listdir(secondary_package_photos_path) if photo.endswith('.jpg')]
    else:
        secondary_photos = []
    
    return render_template('detail_package.html', user=current_user, package=package, secondary_photos=secondary_photos)



@views.route('/add_to_cart/<int:package_id>', methods=['GET', 'POST'])
# @login_required
def add_to_cart(package_id):
    # Add package to cart (session or database)
    package = Packages.query.get_or_404(package_id)
    cart = session.get('cart', [])  
    cart.append({
        'id': package.pk_id,
        'title': package.pk_title,
        'description': package.pk_description,
        'price': package.pk_price,
        'event_id': package.pk_event_id
    })
    session['cart'] = cart
    flash(f'Package {package.pk_title} added to cart', 'success')
    # return jsonify({'success': True})

    return redirect(url_for('views.detail_package', package_id=package_id))

@views.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    # Remove item from cart (session or database)
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = cart
    return redirect(url_for('views.cart'))

@views.route('/checkout', methods=['POST'])
@login_required
def checkout():
    # Handle checkout process
    cart = session.get('cart', [])
    # Process the cart items (e.g., create orders, charge payment, etc.)
    session.pop('cart', None)
    return redirect(url_for('views.home'))

@views.route('/cart', methods=['GET'])
@login_required
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart, user=current_user)

@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    users = Users.query.filter(Users.us_name.like(f'{query}%')).all()
    events = Events.query.filter(Events.ev_title.like(f'{query}%')).all()
    packages = Packages.query.filter(Packages.pk_title.like(f'{query}%')).all()
    return jsonify({
        'users': [{'id': user.us_id, 'name': user.us_name} for user in users],
        'events': [{'id': event.ev_id, 'title': event.ev_title} for event in events],
        'packages': [{'id': package.pk_id, 'title': package.pk_title} for package in packages]
    })

@views.route('/request_seller', methods=['POST'])
@login_required
def request_seller():
    if not current_user.us_is_seller:
        new_request = UserRequests(
            ur_user_id=current_user.us_id,
            ur_request_type='seller'
        )
        db.session.add(new_request)
        db.session.commit()
        flash('Your request to become a seller has been submitted.', 'success')
    else:
        flash('You are already a seller.', 'info')
    return redirect(url_for('views.userOwnInfo'))

@views.route('/manage_requests', methods=['GET', 'POST'])
@login_required
def manage_requests():
    if not current_user.us_is_superuser:
        flash('Access denied.', 'error')
        return redirect(url_for('views.home'))
    requests = UserRequests.query.filter_by(ur_responded=False).all()
    return render_template('manage_requests.html', user=current_user, requests=requests)

@views.route('/respond_request/<int:request_id>', methods=['POST'])
@login_required
def respond_request(request_id):
    if not current_user.us_is_superuser:
        flash('Access denied.', 'error')
        return redirect(url_for('views.home'))
    user_request = UserRequests.query.get_or_404(request_id)
    response = request.form.get('response')
    reason = request.form.get('reason')
    user_request.ur_responded = True
    user_request.ur_accepted = (response == 'accept')
    user_request.ur_response_time = func.now()
    user_request.ur_response_user_id = current_user.us_id
    user_request.ur_response_reason = reason
    if response == 'accept' and user_request.ur_request_type == 'seller':
        user = Users.query.get(user_request.ur_user_id)
        user.us_is_seller = 1
    db.session.commit()
    flash('Request has been responded to.', 'success')
    return redirect(url_for('views.manage_requests'))

@views.context_processor
def inject_unresponded_requests_count():
    if current_user.is_authenticated and current_user.us_is_superuser:
        unresponded_requests_count = UserRequests.query.filter_by(ur_responded=False).count()
    else:
        unresponded_requests_count = 0
    return dict(unresponded_requests_count=unresponded_requests_count)