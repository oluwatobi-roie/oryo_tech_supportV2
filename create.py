from app import app
from models import db
from models.users_model import User



with app.app_context():
    abuja_tech = User(
        username='abujatech',
        f_name="Emmanuel",
        l_name='Sample',
        email='abujatech@oryoltd.com',
        role='3',
    )
    abuja_tech.set_password('demo123')

    phc_tech = User (
        username='phctech',
        f_name="Ezekiel",
        l_name='Sample',
        email='phc@oryoltd.com',
        role='3',
    )
    phc_tech.set_password('demo123')


    db.session.add(abuja_tech)
    db.session.add(phc_tech)
    db.session.commit()
    print("\nUsers Created Successfully \n\n")
