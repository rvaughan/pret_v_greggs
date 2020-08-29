import csv
from datetime import datetime
import os
from lxml import etree as ET


def _toFloat(value:str)->float:
    if value is None or value == "":
        return 0.0

    return float(value)


if __name__ == "__main__":
    onlyfiles = [f for f in os.listdir('../raw_data') if os.path.isfile(os.path.join('../raw_data', f))]

    today = datetime.today().strftime('%Y-%m-%d')

    all_businesses = []
    businesses = []

    for filename in onlyfiles:
        if 'xml' in filename:
            tree = ET.parse('../raw_data/{}'.format(filename))
            root = tree.getroot().find('EstablishmentCollection')
            for child in root:
                business = {}
                include = False
                for node in child:
                    if node.tag == 'BusinessName':
                        business['name'] = node.text
                        if 'Greggs' in node.text:
                            include = True
                        elif 'Pret-A-Manger' in node.text:
                            include = True
                    elif node.tag == 'FHRSID':
                        business['id'] = int(node.text)
                    elif node.tag == 'Geocode':
                        for subnode in node:
                            if subnode.tag == 'Latitude':
                                business['latitude'] = _toFloat(subnode.text)
                            else:
                                business['longitude'] = _toFloat(subnode.text)
                    elif node.tag == 'LocalAuthorityCode':
                        business['local_area_code'] = int(node.text)
                    elif node.tag == 'LocalAuthorityName':
                        business['local_area_name'] = node.text
                    elif node.tag == 'RatingDate':
                        business['rated'] = node.text
                    elif node.tag == 'RatingValue':
                        business['rating'] = node.text

                if include:
                    businesses.append(business)

                all_businesses.append(business)

    csv_columns = ['id', 'name', 'local_area_code', 'local_area_name', 'latitude', 'longitude', 'rated', 'rating']
    csv_file = "{}.csv".format(today)
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in businesses:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    csv_file = "all/{}.csv".format(today)
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in all_businesses:
                writer.writerow(data)
    except IOError:
        print("I/O error")
