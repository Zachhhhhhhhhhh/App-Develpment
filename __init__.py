from flask import Flask, render_template, request, redirect, url_for, flash
import shelve, Service, Carservice, os
from Forms import CreateCarserviceForm, CreateServiceForm

app = Flask(__name__)
app.secret_key = 'any_random_string'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def index():
    return render_template('custhome.html')


@app.route('/createService', methods=['GET', 'POST'])
def create_service():
    create_service_form = CreateServiceForm(request.form)
    if request.method == 'POST' and create_service_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

            services_dict = {}
            db = shelve.open('service.db', 'c')

            try:
                services_dict = db['Services']
            except:
                print("Error in creating Service from service.db.")

            service = Service.Service(create_service_form.name.data,
                                      filename,
                                      create_service_form.description.data,
                                      create_service_form.availability.data)

            if len(services_dict) > 0:
                service.set_service_id(list(services_dict)[-1] + 1)
            services_dict[service.get_service_id()] = service
            db['Services'] = services_dict

            db.close()

        return redirect(url_for('retrieve_service1'))
    return render_template('createService.html', form=create_service_form)


@app.route('/createCarservice', methods=['GET', 'POST'])
def create_carservice():
    create_carservice_form = CreateCarserviceForm(request.form)
    carservices_dict = {}
    db = shelve.open('carservice.db', 'c')
    if request.method == 'POST' and create_carservice_form.validate():

        target = os.path.join(APP_ROOT, 'static/images/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("image"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

            try:
                carservices_dict = db['Carservices']
            except:
                print("Error in creating Car Service from carservice.db.")

            carservice = Carservice.Carservice(create_carservice_form.name.data,
                                               filename,
                                               create_carservice_form.description.data,
                                               create_carservice_form.location.data,
                                               create_carservice_form.hotline.data,
                                               create_carservice_form.starting_hour.data,
                                               create_carservice_form.ending_hour.data,
                                               create_carservice_form.opening_days.data,
                                               create_carservice_form.availability.data)
            if len(carservices_dict) > 0:
                carservice.set_carservice_id(list(carservices_dict)[-1] + 1)
            carservices_dict[carservice.get_carservice_id()] = carservice
            db['Carservices'] = carservices_dict

            db.close()
        return redirect(url_for('retrieve_service1'))
    return render_template('createCarservice.html', form=create_carservice_form)


@app.route('/retrieveService1')
def retrieve_service1():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveService1.html', count1=len(services_list), count2=len(carservices_list),
                           services_list=services_list, carservices_list=carservices_list, )


@app.route('/retrieveService')
def retrieve_service():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    return render_template('retrieveService.html', count1=len(services_list), services_list=services_list)


@app.route('/retrieveCarservice')
def retrieve_carservice():
    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveCarservice.html', count2=len(carservices_list), carservices_list=carservices_list)


@app.route('/updateService/<int:id>/', methods=['GET', 'POST'])
def update_service(id):
    update_service_form = CreateServiceForm(request.form)
    if request.method == 'POST' and update_service_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                services_dict = {}
                db = shelve.open('service.db', 'w')
                services_dict = db['Services']

                service = services_dict.get(id)
                service.set_name(update_service_form.name.data)
                service.set_description(update_service_form.description.data)
                service.set_availability(update_service_form.availability.data)

                db['Services'] = services_dict
                db.close()
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)

                services_dict = {}
                db = shelve.open('service.db', 'w')
                services_dict = db['Services']

                service = services_dict.get(id)
                service.set_name(update_service_form.name.data)
                service.set_image(filename)
                service.set_description(update_service_form.description.data)
                service.set_availability(update_service_form.availability.data)

                db['Services'] = services_dict
                db.close()

        return redirect(url_for('retrieve_service1'))
    else:
        services_dict = {}
        db = shelve.open('service.db', 'r')
        services_dict = db['Services']
        db.close()

        service = services_dict.get(id)
        update_service_form.name.data = service.get_name()
        filename = service.get_image()
        update_service_form.description.data = service.get_description()
        update_service_form.availability.data = service.get_availability()

        return render_template('updateService.html', form=update_service_form)


@app.route('/updateCarservice/<int:id>/', methods=['GET', 'POST'])
def update_carservice(id):
    update_carservice_form = CreateCarserviceForm(request.form)
    if request.method == 'POST' and update_carservice_form.validate():
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        for file in request.files.getlist("image"):
            filename = file.filename
            if filename == "":
                carservices_dict = {}
                db = shelve.open('carservice.db', 'w')
                carservices_dict = db['Carservices']

                carservice = carservices_dict.get(id)
                carservice.set_name(update_carservice_form.name.data)
                carservice.set_description(update_carservice_form.description.data)
                carservice.set_location(update_carservice_form.location.data)
                carservice.set_hotline(update_carservice_form.hotline.data)
                carservice.set_starting_hour(update_carservice_form.starting_hour.data)
                carservice.set_ending_hour(update_carservice_form.ending_hour.data)
                carservice.set_opening_days(update_carservice_form.opening_days.data)
                carservice.set_availability(update_carservice_form.availability.data)

                db['Carservices'] = carservices_dict
                db.close()
            elif not filename.lower().endswith(('.tiff', '.png', '.jpg', '.jpeg', '.jfif', '.gif')):
                flash("Only tiff, png, jpg, jpeg, jfif and gif file extensions are allowed!")
                return redirect(request.url)
            else:
                destination = "/".join([target, filename])
                file.save(destination)

                carservices_dict = {}
                db = shelve.open('carservice.db', 'w')
                carservices_dict = db['Carservices']

                carservice = carservices_dict.get(id)
                carservice.set_name(update_carservice_form.name.data)
                carservice.set_image(filename)
                carservice.set_description(update_carservice_form.description.data)
                carservice.set_location(update_carservice_form.location.data)
                carservice.set_hotline(update_carservice_form.hotline.data)
                carservice.set_starting_hour(update_carservice_form.starting_hour.data)
                carservice.set_ending_hour(update_carservice_form.ending_hour.data)
                carservice.set_opening_days(update_carservice_form.opening_days.data)
                carservice.set_availability(update_carservice_form.availability.data)

                db['Carservices'] = carservices_dict
                db.close()

        return redirect(url_for('retrieve_service1'))
    else:
        carservices_dict = {}
        db = shelve.open('carservice.db', 'r')
        carservices_dict = db['Carservices']
        db.close()

        carservice = carservices_dict.get(id)
        update_carservice_form.name.data = carservice.get_name()
        filename = carservice.get_image()
        update_carservice_form.description.data = carservice.get_description()
        update_carservice_form.location.data = carservice.get_location()
        update_carservice_form.hotline.data = carservice.get_hotline()
        update_carservice_form.starting_hour.data = carservice.get_starting_hour()
        update_carservice_form.ending_hour.data = carservice.get_ending_hour()
        update_carservice_form.opening_days.data = carservice.get_opening_days()
        update_carservice_form.availability.data = carservice.get_availability()

        return render_template('updateCarservice.html', form=update_carservice_form)


@app.route('/deleteService/<int:id>', methods=['POST'])
def delete_service(id):
    services_dict = {}
    db = shelve.open('service.db', 'w')
    services_dict = db['Services']

    services_dict.pop(id)

    db['Services'] = services_dict
    db.close()

    return redirect(url_for('retrieve_service1'))


@app.route('/deleteCarservice/<int:id>', methods=['POST'])
def delete_carservice(id):
    carservices_dict = {}
    db = shelve.open('carservice.db', 'w')
    carservices_dict = db['Carservices']

    carservices_dict.pop(id)

    db['Carservices'] = carservices_dict
    db.close()

    return redirect(url_for('retrieve_service1'))


@app.route('/retrieveCustservice1')
def retrieve_custservice1():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveCustservice1.html', count1=len(services_list), count2=len(carservices_list),
                           services_list=services_list, carservices_list=carservices_list, )


@app.route('/retrieveCustservice')
def retrieve_custservice():
    services_dict = {}
    db = shelve.open('service.db', 'r')
    services_dict = db['Services']
    db.close()

    services_list = []
    for key in services_dict:
        service = services_dict.get(key)
        services_list.append(service)

    return render_template('retrieveCustservice.html', count1=len(services_list), services_list=services_list)


@app.route('/retrieveCustcarservice')
def retrieve_custcarservice():
    carservices_dict = {}
    db = shelve.open('carservice.db', 'r')
    carservices_dict = db['Carservices']
    db.close()

    carservices_list = []
    for key in carservices_dict:
        carservice = carservices_dict.get(key)
        carservices_list.append(carservice)

    return render_template('retrieveCustcarservice.html', count2=len(carservices_list),
                           carservices_list=carservices_list)


if __name__ == '__main__':
    app.run(debug=True)
