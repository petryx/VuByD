import os
import connexion
from flask_sqlalchemy import SQLAlchemy

#API7:2019 — Security misconfiguration
vuln_by_design = connexion.App(__name__, specification_dir='./api_specs')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(vuln_by_design.root_path, 'database/database.db')
vuln_by_design.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
vuln_by_design.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#API2:2019 — Broken authentication
vuln_by_design.app.config['SECRET_KEY'] = '|+Utur4M@Fan'


db = SQLAlchemy(vuln_by_design.app)

vuln_by_design.add_api('openapi3.yml')




