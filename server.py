import socketserver

from load_database import load_database, is_duplicate_record


class DBServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024).strip().decode()
                if not data:
                    break
                # print(f"request {data}")
                command, *args = data.split('|')
                if command == "FIND_CUSTOMER":
                    customer_name = args[0].lower()
                    response = self.find_customer(customer_name)

                if command == "ADD_CUSTOMER":
                    customer_name = args[0].lower()
                    customer_age = args[1].lower()
                    customer_address = args[2].lower()
                    customer_phone = args[3].lower()
                    # print(customer_name)
                    if is_duplicate_record(self.server.database, customer_name):
                        response = "Customer already exists"
                    else:
                        customer_record = {
                            "name": customer_name,
                            "age": customer_age,
                            "address": customer_address,
                            "phone": customer_phone
                        }
                        response = self.add_customer(customer_record)

                if command == "DELETE_CUSTOMER":
                    customer_name = args[0].lower()
                    response = self.delete_customer(customer_name)

                if command == "UPDATE_AGE":
                    customer_name = args[0].lower()
                    customer_age = args[1]
                    response = self.update_customer_field(customer_name, "age", customer_age)

                if command == "UPDATE_ADDRESS":
                    customer_name = args[0].lower()
                    customer_address = args[1]
                    response = self.update_customer_field(customer_name, "address", customer_address)

                if command == "UPDATE_PHONE":
                    customer_name = args[0].lower()
                    customer_phone = args[1]
                    response = self.update_customer_field(customer_name, "phone", customer_phone)

                if command == "PRINT_REPORT":
                    response = self.print_report()

                self.request.sendall(response.encode())
            except ConnectionResetError:
                break

    def find_customer(self, customer_name):
        for customer in self.server.database:
            if customer["name"] == customer_name:
                return "|".join(customer.values())
        return f"{customer_name} not found in database"

    def add_customer(self, customer_record):
        self.server.database.append(customer_record)
        sorted(self.server.database, key=lambda record: record['name'])
        return "|".join(customer_record.values())

    def delete_customer(self, customer_name):
        for record in self.server.database:
            if record['name'] == customer_name:
                self.server.database.remove(record)
                return f"{customer_name} deleted successfully"
        return "Customer does not exist"

    def update_customer_field(self, customer_name, field_name, new_value):
        for record in self.server.database:
            if record['name'] == customer_name:
                record[field_name] = new_value
                return f"Update: {field_name} = {new_value} for {customer_name}"
        return "Customer not found"

    def print_report(self):
        report = "".join(['|'.join(record.values()) for record in self.server.database])
        return report


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    database = load_database('data.txt')
    print("Python DB Server is now running...")
    with socketserver.TCPServer((HOST, PORT), DBServer) as server:
        server.database = sorted(database, key=lambda record: record['name'])
        server.serve_forever()
