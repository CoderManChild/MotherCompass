import json
from flask import Flask, request
from backend.db import db, Mother, Provider, create_hardcoded
from flask_sqlalchemy import SQLAlchemy

# define db filename
app = Flask(__name__) #make a Flask instance

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = '' # FIX WITH POSTGRESQL LINK
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True



# initialize app
db.init_app(app)
with app.app_context():
    db.create_all() #Makes all predefined datbase tables
    create_hardcoded() #makes default providers and mothers

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# your routes here

@app.route("/")
def hello_world():
    return "Hello, World!"




#--------MOTHERS--------#


"""
Route to create the mother. Returns error code 400 if fields not provided, otherwise makes the new Mother, commits it to the database, and
returns a 201 success code along with the serialization.
"""
@app.route("/api/mothers/", methods=["POST"])
def create_mother():
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')
    full_name = body.get('full_name')
    email = body.get('email')
    public_or_private = body.get('public_or_private', False) #default is private
    opt_in_ads = body.get('opt_in_ads', False) #default is no ads
    prev_children = body.get('prev_children', 0)
    deliver_yet = body.get('deliver_yet', False) #default is expecting mother
    DOB = body.get('DOB')  # This should be in the format 'YYYY-MM-DD'
    provider_names = body.get('providers', [])  # List of provider IDs

    # Check for required fields, and non-duplicates for user-name or full-name.
    if username is None and Mother.query.filter_by(username=username).first() is not None:
        return failure_response("No username provided or duplicate username", 400)
    if password is None:
        return failure_response("No password provided", 400)
    if full_name is None and Mother.query.filter_by(full_name=full_name).first() is not None:
        return failure_response("No full name provided or duplicate full-name", 400)
    if email is None:
        return failure_response("No email provided", 400)

    # Create new Mother object
    new_mother = Mother(
        username=username,
        password=password,
        full_name=full_name,
        email=email,
        public_or_private=public_or_private, #NOTE -- nothing has been done to filter by this yet 
        opt_in_ads=opt_in_ads,
        prev_children=prev_children,
        deliver_yet=deliver_yet,
        DOB=DOB,
    )

    # Add providers if any
    for provider_fullname in provider_names:
        provider = Provider.query.filter_by(full_name=provider_fullname).first() 

        #NOTE -- Due to this syntax, we must ensure no duplicates in name, and probably username.

        if provider:
            new_mother.providers.append(provider) #for the field that is list of providers, append all registered providers

    # Add new mother to the session and commit
    db.session.add(new_mother)
    db.session.commit()

    return success_response(new_mother.serialize(), 201)

"""
Returns serialization of all mothers in Mother table
"""
@app.route("/api/mothers/", methods=["GET"])
def get_mothers():
    #note query.all() returns every value in this query as a list. 
    mothers = [c.serialize() for c in Mother.query.all()] 
    return success_response(mothers)


"""
Deletes a mother given id. If mother is not found, returns 404 error code.
"""
@app.route("/api/mothers/<int:id>/", methods=["DELETE"])
def delete_mother(id):
    mother = Mother.query.get(id)
    if mother is None:
        return failure_response("Mother not found")
    db.session.delete(mother)
    db.session.commit()
    return success_response(mother.serialize())



#NOTE: Functionality to change information -- tbd whether implmeneted on frontend

# """
# Returns serialization of an updated user who changed their password
# """
# @app.route("/api/users/<int:user_id>/update/", methods=["POST"])
# def change_password(user_id):
#     body = json.loads(request.data)
#     password = body.get('password')
#     if password is None:
#         return failure_response("No new password provided", 400)
#     user = User.query.get(user_id)
#     if user is None:
#         return failure_response("User not found")
#     user.password = password
#     db.session.commit()
#     return success_response(user.serialize())

"""
Check if a mother with provided username and password exists. I
If does, then returns serialized form in success response 200, else "No valid mother" message with 400 code.
"""
@app.route("/api/mothers/login/", methods=["POST"])
def get_spec_mother():
    #assuming the data is being passed in through login fields
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')

    #these checks are in case front-end doesn't handle clicking without filling a field.
    if username is None:
        return failure_response("No username provided", 400)
    if password is None:
        return failure_response("No password provided", 400)
    mother_val = Mother.query.filter(Mother.username==username, Mother.password==password).first()
    if mother_val is None:
        return failure_response("No Valid mother", 400)
    
    return success_response(Mother.serialize(mother_val)) #return serialized with all fields

"""
Returns the list of providers for logged-in mother. Non-recursive serialization for mothers associated to each provider.
"""
@app.route("/api/mothers/<int:mother_id>/providers/", methods=["GET"])
def get_mother_providers(mother_id):
    mother = Mother.query.get(mother_id)
    if mother is None:
        return failure_response("Mother not found")
    providers = mother.providers
    providers_data = [Provider.serialize(provider, include_mothers=False) for provider in providers] #don't want to return list of mothers of a doctor
    return success_response({"providers": providers_data})


"""
Add a provider to a logged-in mother, by fullname
"""
@app.route("/api/mothers/<int:mother_id>/providers/", methods=["POST"])
def add_provider_to_mother(mother_id):
    mother = Mother.query.get(mother_id)
    if mother is None:
        return failure_response("Mother not found")
    body = json.loads(request.data)
    full_name = body.get('full_name')
    if full_name is None:
        return failure_response("No Full Name added", 400)
    provider_val = Provider.query.filter(Provider.full_name==full_name).first()
    if provider_val is None or provider_val in mother.providers:
        return failure_response("No Valid provider or Already associated", 400)
    mother.providers.append(provider_val) #add the provider to the mother's list of providers 
    db.session.commit() 
    return success_response({"mother": mother.serialize()})

"""
Remove a provider from a logged-in mother, by full-name.
"""
@app.route("/api/mothers/<int:mother_id>/providers/", methods=["DEL"])
def remove_provider_from_mother(mother_id):
    mother = Mother.query.get(mother_id)
    if mother is None:
        return failure_response("Mother not found")
    body = json.loads(request.data)
    full_name = body.get('full_name')
    if full_name is None:
        return failure_response("No Full Name added", 400)
    provider_val = Provider.query.filter(Provider.full_name==full_name).first()
    if provider_val is None or provider_val not in mother.providers:
        return failure_response("No Valid provider or Not associated", 400)
    mother.providers.remove(provider_val) #Remove the provider from the mother's list of providers
    db.session.commit() 
    return success_response({"mother": mother.serialize()})


"""
Query providers by state. 
"""
@app.route("/api/mothers/<int:mother_id>/providers/", methods=["GET"])
def query_by_state(mother_id):
    state_name = request.args.get('state') #extract from query parameters, not body since not POST
    if not state_name:
        return failure_response("No state_name provided")
    states = set("Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
        "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming")
    
    if state_name not in states:
        return failure_response("Invalid statename")
    
    providers = Provider.query.filter(Provider.state_name==state_name)
    if not providers:
        return success_response("No providers in this state") #not necc. failure -- not internal error
    #We serialize every provider in the list, displaying their information
    providers_data = [provider.serialize(include_mothers=False) for provider in providers]
    return success_response({"List of providers": providers_data})


#-------PROVIDERS--------#


"""
Route to create the provider. Returns error code 400 if fields not provided, otherwise makes the new Provider, commits it to the database, and
returns a 201 success code along with the serialization.
"""
@app.route("/api/providers/", methods=["POST"])
def create_provider():
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')
    full_name = body.get('full_name')
    email = body.get('email')
    license_number = body.get('license_number')
    state_name = body.get('state_name')
    diploma_date = body.get('diploma_date')
    mother_names = body.get('mothers', [])  # List of mother Fullnames

    # Check for required fields, and non-duplicates for user-name, full-name, or license-number
    if username is None and Mother.query.filter_by(username=username).first() is not None:
        return failure_response("No username provided or duplicate username", 400)
    if password is None:
        return failure_response("No password provided", 400)
    if full_name is None and Mother.query.filter_by(full_name=full_name).first() is not None:
        return failure_response("No full name provided or duplicate fullname", 400)
    if email is None:
        return failure_response("No email provided", 400)
    if license_number is  None and Mother.query.filter_by(license_number=license_number).first() is not None:
        return failure_response("No username provided", 400)
    if state_name is None:
        return failure_response("No statename provided", 400)
    if diploma_date is None:
        return failure_response("No diploma date provided", 400)

    # Create new Provider object
    new_provider = Provider(
        username=username,
        password=password,
        full_name=full_name,
        email=email,
        license_number=license_number,
        state_name=state_name,
        diploma_date=diploma_date
    )

    # Add providers if any
    for mother_fullname in mother_names:
        mother = Mother.query.filter_by(full_name=mother_fullname).first() 

        #NOTE -- Due to this syntax, we must ensure no duplicates in name, and probably username.

        if mother:
            new_provider.mothers.append(mother) #for the field that is list of mothers, append all registered mothers

    # Add new mother to the session and commit
    db.session.add(new_provider)
    db.session.commit()

    return success_response(new_provider.serialize(), 201)


"""
Returns serialization of all providers in Provider table
"""
@app.route("/api/provider/", methods=["GET"])
def get_providers():
    #note query.all() returns every value in this query as a list. 
    providers = [c.serialize() for c in Provider.query.all()] 
    return success_response(providers)



"""
Deletes a provider given id. If provider is not found, returns 404 error code.
"""
@app.route("/api/providers/<int:id>/", methods=["DELETE"])
def delete_provider(id):
    provider = Provider.query.get(id)
    if provider is None:
        return failure_response("Provider not found")
    db.session.delete(provider)
    db.session.commit()
    return success_response(provider.serialize())



"""
Check if a provider with provided username and password exists. 
If does, then returns serialized form in success response 200, else "No valid provider" message with 400 code.
"""
@app.route("/api/providers/login/", methods=["POST"])
def get_spec_provider():
    #assuming the data is being passed in through login fields
    body = json.loads(request.data)
    username = body.get('username')
    password = body.get('password')

    #these checks are in case front-end doesn't handle clicking without filling a field.
    if username is None:
        return failure_response("No username provided", 400)
    if password is None:
        return failure_response("No password provided", 400)
    provider_val = Provider.query.filter(Provider.username==username, Provider.password==password).first() #returns in list format, should only be 1 value due to unique
    if provider_val is None:
        return failure_response("No Valid provider", 400)
    
    return success_response(Provider.serialize(provider_val)) #return serialized with all fields



"""
Returns the list of mothers for logged-in provider. Non-recursive serialization for providers of each mother.
"""
@app.route("/api/mothers/<int:provider_id>/providers/", methods=["GET"])
def get_provider_mothers(provider_id):
    provider = Provider.query.get(provider_id)
    if provider is None:
        return failure_response("Provider not found")
    mothers = provider.mothers
    mothers_data = [Mother.serialize(mother, include_providers=False) for mother in mothers] #don't want to return list of mothers of a doctor
    return success_response({"mothers": mothers_data})



"""
Add a Mother to a logged-in provider, by fullname
"""
@app.route("/api/providers/<int:provider_id>/mothers/", methods=["POST"])
def add_mother_to_provider(provider_id):
    provider = Provider.query.get(provider_id)
    if provider is None:
        return failure_response("Provider not found")
    body = json.loads(request.data)
    full_name = body.get('full_name')
    if full_name is None:
        return failure_response("No Full Name added", 400)
    mother_val = Mother.query.filter(Mother.full_name==full_name).first()
    if mother_val is None or mother_val in provider.mothers:
        return failure_response("No Valid mother or Already associated", 400)
    provider.mothers.append(mother_val) #add the mother to the provider's list of mothers 
    db.session.commit() 
    return success_response({"provider": provider.serialize()})

"""
Remove a mother from a logged-in provider, by full-name.
"""
@app.route("/api/providers/<int:provider_id>/mothers/", methods=["DEL"])
def remove_mother_from_provider(provider_id):
    provider = Provider.query.get(provider_id)
    if provider is None:
        return failure_response("Provider not found")
    body = json.loads(request.data)
    full_name = body.get('full_name')
    if full_name is None:
        return failure_response("No Full Name added", 400)
    mother_val = Mother.query.filter(Mother.full_name==full_name).first()
    if mother_val is None or mother_val not in provider.mothers:
        return failure_response("No Valid Mother or Not associated", 400)
    provider.mothers.remove(mother_val) #Remove the mother from the provider's list of mothers 
    db.session.commit() 
    return success_response({"provider": provider.serialize()})






# run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
