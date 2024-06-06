def is_field_missing(customer_record):
    fields = customer_record.split("|")
    return len(fields) != 4


def is_valid_first_name(first_name):
    if not first_name or not first_name.isalpha():
        return False
    else:
        return True


def is_valid_address(address):
    if not address:
        return True
    else:
        for char in address:
            if not (char.isalnum() or char in " -."):
                return False
    return True


def is_valid_phone_number(phone_number):
    if not phone_number:
        return True
    trim_phone_number = phone_number.replace(' ', '').replace('-', '')
    if not trim_phone_number.isdigit():
        return False
    if len(trim_phone_number) == 7:
        return phone_number[3] == '-'

    elif len(trim_phone_number) == 10:
        return phone_number[3] == ' ' and phone_number[7] == '-'
    else:
        return False


def is_valid_age(age):
    if not age:
        return True
    elif not age.isdigit():
        return False
    else:
        return 1 <= int(age) <= 120


def is_valid_record(record):
    fields = record.split("|")
    first_name = fields[0].strip()
    age = fields[1].strip()
    address = fields[2].strip()
    phone_number = fields[3].strip()
    if not is_valid_first_name(first_name):
        print("Record skipped [invalid name field]: {}".format(record))
        return False
    if not is_valid_age(age):
        print("Record skipped [invalid age field]: {}".format(record))
        return False
    if not is_valid_address(address):
        print("Record skipped [invalid address field]: {}".format(record))
        return False
    if not is_valid_phone_number(phone_number):
        print("Record skipped [invalid phone field]: {}".format(record))
        return False
    return True


def is_duplicate_record(database, customer_name):
    for record in database:
        if record['name'] == customer_name.lower():
            return True
    return False


def load_database(filename):
    database = []
    with open(filename) as file:
        for customer_record in file:
            if is_field_missing(customer_record):
                print("Record skipped [missing field(s)]: {}".format(customer_record))
            elif not is_valid_record(customer_record):
                continue
            elif is_duplicate_record(database, customer_record.split("|")[0]):
                print("Record skipped [customer already exist]: {}".format(customer_record))
            else:
                fields = customer_record.split("|")
                customer_record_dict = {
                    "name": fields[0].lower(),
                    "age": fields[1].lower(),
                    "address": fields[2].lower(),
                    "phone": fields[3].lower(),
                }
                database.append(customer_record_dict)
    return database
