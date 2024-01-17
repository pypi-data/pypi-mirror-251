from kahi.KahiBase import KahiBase
from pymongo import MongoClient, TEXT
from bson.objectid import ObjectId
from pandas import read_excel
from time import time


class Kahi_staff_udea_affiliations(KahiBase):

    config = {}

    def __init__(self, config):
        self.config = config

        self.client = MongoClient(config["database_url"])

        self.db = self.client[config["database_name"]]
        self.collection = self.db["affiliations"]

        self.collection.create_index("external_ids.id")
        self.collection.create_index("names.name")
        self.collection.create_index("types.type")
        self.collection.create_index([("names.name", TEXT)])

        self.file_path = config["staff_udea_affiliations"]["file_path"]
        self.data = read_excel(self.file_path)

        # logs for higher verbosity
        self.facs_inserted = {}
        self.deps_inserted = {}
        self.fac_dep = []

        self.udea_reg = self.collection.find_one(
            {"names.name": "University of Antioquia"})
        if not self.udea_reg:
            print(
                "University of Antioquia not found in database. Creating it with minimal information...")
            udea_reg = self.empty_affiliation()
            udea_reg["updated"].append(
                {"time": int(time()), "source": "manual"})
            udea_reg["names"] = [
                {"name": 'Universidad de Antioquia',
                    "lang": 'es', "source": "staff_udea"}
            ]
            udea_reg["abbreviations"] = ['UdeA']
            udea_reg["year_established"] = 1803
            udea_reg["addresses"] = [
                {
                    "lat": 6.267417,
                    "lng": -75.568389,
                    "postcode": '',
                    "state": "Antioquia",
                    "city": 'Medellín',
                    "country": 'Colombia',
                    "country_code": 'CO'
                }
            ]
            udea_reg["external_ids"] = [
                {"source": 'isni', "id": '0000 0000 8882 5269'},
                {"source": 'fundref', "id": '501100005278'},
                {"source": 'orgref', "id": '2696975'},
                {"source": 'wikidata', "id": 'Q1258413'},
                {"source": 'ror', "id": 'https://ror.org/03bp5hc83'},
                {"source": 'minciencias', "id": '007300000887'},
                {"source": 'nit', "id": '890980040-8'}
            ]
            self.collection.insert_one(udea_reg)
            self.udea_reg = self.collection.find_one(
                {"names.name": "Universidad de Antioquia"})

    def fix_names(self, name):  # reg["Nombre fac"]
        name = name.strip()
        if name == 'Vic Docencia':
            name = "Vicerrectoría de Docencia"
        if name == "Exactas":
            name = "Facultad de Ciencias Exactas y Naturales"
        if name == "Sociales":
            name = "Facultad de Ciencias Sociales y Humanas"
        if name == "Derecho":
            name = "Facultad de Derecho y Ciencias Políticas"
        if name == "Agrarias":
            name = "Facultad de Ciencias Agrarias"
        if name == "Est. Políticos":
            name = "Institutio de Estudios Políticos"
        if name == "Artes":
            name = "Facultad de Artes"
        if name == "Odontología":
            name = "Facultad de Odontología"
        if name == "Comunicaciones":
            name = "Facultad de Comunicaciones y Filología"
        if name == "Educación":
            name = "Facultad de Educación"
        if name == "Idiomas":
            name = "Escuela de Idiomas"
        if name == "Filosofía":
            name = "Instituto de Filosofía"
        if name == "Económicas":
            name = "Facultad de Ciencias Económicas"
        if name == "Ingeniería":
            name = "Facultad de Ingeniería"
        if name == "Medicina":
            name = "Facultad de Medicina"
        if name == "Farmacéuticas":
            name = "Facultad de Ciencias Farmacéuticas y Alimentarias"
        if name == "Microbiología":
            name = "Escuela de Microbiología"
        if name == "Salud Pública":
            name = "Facultad de Salud Pública"
        if name == "Agrarias":
            name = "Facultad de Ciecias Agrarias"
        if name == "Bibliotecología":
            name = "Escuela Interamericana de Bibliotecología"
        if name == "Enfermería":
            name = "Facultad de Enfermería"
        if name == "Educación Física":
            name = "Instituto Universitario de Educación Física y Deporte"
        if name == "Nutrición":
            name = "Escuela de Nutrición y Dietética"
        if name == "Corp Ambiental":
            name = "Corporación Ambiental"
        if name == "Est. Regionales":
            name = "Instituto de Estudios Regionales"
        return name

    def run(self):
        # inserting faculties and departments
        for idx, reg in self.data.iterrows():
            name = self.fix_names(reg["Nombre fac"])
            if name not in self.facs_inserted.keys():
                is_in_db = self.collection.find_one({"names.name": name})
                if is_in_db:
                    if name not in self.facs_inserted.keys():
                        self.facs_inserted[name] = is_in_db["_id"]
                        print(name, " already in db")
                    # continue
                    # may be updatable, check accordingly
                else:
                    entry = self.empty_affiliation()
                    entry["updated"].append(
                        {"time": int(time()), "source": "staff"})
                    entry["names"].append(
                        {"name": name, "lang": "es", "source": "staff_udea"})
                    entry["types"].append(
                        {"source": "staff", "type": "faculty"})
                    entry["relations"].append(
                        {"id": self.udea_reg["_id"], "name": "Universidad de Antioquia", "types": self.udea_reg["types"]})

                    fac = self.collection.insert_one(entry)
                    self.facs_inserted[name] = fac.inserted_id

            if reg["Nombre cencos"] not in self.deps_inserted.keys():
                is_in_db = self.collection.find_one(
                    {"names.name": reg["Nombre cencos"]})
                if is_in_db:
                    if reg["Nombre cencos"] not in self.deps_inserted.keys():
                        self.deps_inserted[reg["Nombre cencos"]
                                           ] = is_in_db["_id"]
                        print(reg["Nombre cencos"], " already in db")
                    # continue
                    # may be updatable, check accordingly
                else:
                    entry = self.empty_affiliation()
                    entry["updated"].append(
                        {"time": int(time()), "source": "staff"})
                    entry["names"].append(
                        {"name": reg["Nombre cencos"], "lang": "es", "source": "staff_udea"})
                    entry["types"].append(
                        {"source": "staff", "type": "department"})
                    entry["relations"].append(
                        {"id": self.udea_reg["_id"], "name": "Universidad de Antioquia", "types": self.udea_reg["types"]})

                    dep = self.collection.insert_one(entry)
                    self.deps_inserted[reg["Nombre cencos"]] = dep.inserted_id

            if (name, reg["Nombre cencos"]) not in self.fac_dep:
                self.fac_dep.append((name, reg["Nombre cencos"]))

        # Creating relations between faculties and departments
        for fac, dep in self.fac_dep:
            fac_id = self.facs_inserted[fac]
            dep_id = self.deps_inserted[dep]
            dep_reg = self.collection.find_one({"_id": ObjectId(dep_id)})
            fac_reg = self.collection.find_one({"_id": ObjectId(fac_id)})
            self.collection.update_one({"_id": fac_reg["_id"]},
                                       {"$push": {
                                           "relations": {
                                               "id": dep_reg["_id"],
                                               "name": dep_reg["names"][0]["name"], "types": dep_reg["types"]}}})
            self.collection.update_one({"_id": dep_reg["_id"]},
                                       {"$push": {
                                           "relations": {
                                               "id": fac_reg["_id"],
                                               "name": fac_reg["names"][0]["name"], "types": fac_reg["types"]}}})

        return 0
