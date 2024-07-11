from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Association table for many-to-many relationship between Mother and Provider
mother_provider_association = db.Table('mother_provider_association',
    db.Column('mother_id', db.Integer, db.ForeignKey('mothers.id'), primary_key=True),
    db.Column('provider_id', db.Integer, db.ForeignKey('providers.id'), primary_key=True)
)

# Define Mother model
class Mother(db.Model):
    __tablename__ = 'mothers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='Mother')
    public_or_private = db.Column(db.Boolean, nullable=False, default=False)
    opt_in_ads = db.Column(db.Boolean, nullable=False, default=False)
    prev_children = db.Column(db.Integer, nullable=False, default=0)
    deliver_yet = db.Column(db.Boolean, nullable=False, default=False)
    DOB = db.Column(db.Date, nullable=True) #this id DOB of baby. If not given birth yet, urge them to put 1st of expected month.
    providers = db.relationship('Provider', secondary=mother_provider_association, backref='mothers')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'public_or_private': self.public_or_private,
            'opt_in_ads': self.opt_in_ads,
            'prev_children': self.prev_children,
            'deliver_yet': self.deliver_yet,
            'DOB': self.DOB.isoformat() ,
            'providers': [provider.serialize() for provider in self.providers]
        }
# Define Provider model
class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, default='Provider')
    license_number = db.Column(db.String, nullable=True)
    state_name = db.Column(db.String, nullable=True)
    diploma_date = db.Column(db.Date, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'license_number': self.license_number,
            'state_name': self.state_name,
            'diploma_date': self.diploma_date.isoformat(),
            'mothers': [mother.serialize() for mother in self.mothers]
        }

# Function to create hardcoded mothers and providers with associations at start.
def create_hardcoded_mothers_and_providers():
    if Mother.query.count() == 0 and Provider.query.count() == 0:
        mothers_data = [
            {
                'username': 'mother1',
                'password': 'password1',
                'full_name': 'Mother One',
                'email': 'mother1@example.com',
                'public_or_private': True,
                'opt_in_ads': False,
                'prev_children': 1,
                'deliver_yet': True,
                'DOB': date(2024, 5, 15),
                'provider_usernames': ['provider1', 'provider2']  # List of provider usernames
            },
            {
                'username': 'mother2',
                'password': 'password2',
                'full_name': 'Mother Two',
                'email': 'mother2@example.com',
                'public_or_private': False,
                'opt_in_ads': True,
                'prev_children': 0,
                'deliver_yet': False,
                'DOB': date(2024, 10, 1),
                'provider_usernames': ['provider1']  # List of provider usernames
            },
            {
                'username': 'mother3',
                'password': 'password3',
                'full_name': 'Mother Three',
                'email': 'mother3@example.com',
                'public_or_private': True,
                'opt_in_ads': True,
                'prev_children': 2,
                'deliver_yet': False,
                'DOB': date(2025, 1, 1),
                'provider_usernames': ['provider2']  # List of provider usernames
            }
        ]

        providers_data = [
            {
                'username': 'provider1',
                'password': 'password1',
                'full_name': 'Provider One',
                'email': 'provider1@example.com',
                'license_number': '12345',
                'state_name': 'California',
                'diploma_date': date(2000, 1, 1)
            },
            {
                'username': 'provider2',
                'password': 'password2',
                'full_name': 'Provider Two',
                'email': 'provider2@example.com',
                'license_number': '67890',
                'state_name': 'New York',
                'diploma_date': date(2005, 5, 5)
            }
        ]

        # Do providers first, because we need them on hand for the providers list on mother's side
        
        #Note intentional choice -- mothers can choose which providers to add relationship with for chat, not vice versa (privacy)
        
        providers_dict = {}
        for data in providers_data:
            provider = Provider(**data) #instantiate Provider object with this data
            db.session.add(provider)
            providers_dict[provider.username] = provider
            #We add all the providers to the session, and we also keep track of them in providers_dict

        for data in mothers_data:
            provider_usernames = data.pop('provider_usernames')  # Remove provider_usernames list from data -- we end up storing the providers as a whole in 'providers'
            mother = Mother(**data)
            for username in provider_usernames:
                provider = providers_dict.get(username) 
                if provider:
                    mother.providers.append(provider) #add relationship to association table between Mother and Provider instance
            db.session.add(mother)

        db.session.commit()

