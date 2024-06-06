import os
import socket
import sys

from load_database import *


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = self.connect_to_server()

    def connect_to_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        return client_socket

    def send_request(self, request):
        self.client_socket.sendall(request.encode())
        response = self.client_socket.recv(1024).decode()
        if request == "PRINT_REPORT":
            print('** Database contents **')
            print(response)
        else:
            print(f"Server response: {response}")

    def find_customer(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        self.send_request(f"FIND_CUSTOMER|{customer_name}")

    def add_customer(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        customer_age = get_valid_input("Customer Age: ", is_valid_age,
                                       "Age must be an integer (1>=age<=120). Please try again...")
        customer_address = get_valid_input("Customer Address: ", is_valid_address,
                                           "Invalid address. Please enter an address with alphanumeric characters, spaces, periods, or dashes.")
        customer_phone = get_valid_input("Customer Phone: ", is_valid_phone_number,
                                         "Invalid phone number. Please enter a 7 or 10 digit phone number with appropriate formatting.")
        self.send_request(
            f"ADD_CUSTOMER|{customer_name}|{customer_age}|{customer_address}|{customer_phone}")

    def delete_customer(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        self.send_request(f"DELETE_CUSTOMER|{customer_name}")

    def update_customer_age(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        customer_age = get_valid_input("Customer Age: ", is_valid_age,
                                       "Age must be an integer (1>=age<=120). Please try again...")
        self.send_request(f"UPDATE_AGE|{customer_name}|{customer_age}")

    def update_customer_address(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        customer_address = get_valid_input("Customer Address: ", is_valid_address,
                                           "Invalid address. Please enter an address with alphanumeric characters, spaces, periods, or dashes.")
        self.send_request(f"UPDATE_ADDRESS|{customer_name}|{customer_address}")

    def update_customer_phone(self):
        customer_name = get_valid_input("Customer Name: ", is_valid_first_name,
                                        "Invalid name. Please enter alphabetic characters only.")
        customer_phone = get_valid_input("Customer Phone: ", is_valid_phone_number,
                                         "Invalid phone number. Please enter a 7 or 10 digit phone number with appropriate formatting.")
        self.send_request(f"UPDATE_PHONE|{customer_name}|{customer_phone}")

    def print_report(self):
        self.send_request("PRINT_REPORT")

    def run(self):
        while True:
            clear_screen()
            display_menu()

            selection = input("Select: ")
            if selection == "1":
                self.find_customer()
                press_any_key_to_continue()
            elif selection == "2":
                self.add_customer()
                press_any_key_to_continue()
            elif selection == "3":
                self.delete_customer()
                press_any_key_to_continue()
            elif selection == "4":
                self.update_customer_age()
                press_any_key_to_continue()
            elif selection == "5":
                self.update_customer_address()
                press_any_key_to_continue()
            elif selection == "6":
                self.update_customer_phone()
                press_any_key_to_continue()
            elif selection == "7":
                self.print_report()
                press_any_key_to_continue()
            elif selection == "8":
                print("Good bye!")
                break
            else:
                print("Invalid selection. Please select a valid option.")

        self.client_socket.close()


def press_any_key_to_continue():
    print("\n\nPress any key to continue...", end='', flush=True)
    if os.name == 'nt':  # For Windows
        import msvcrt
        msvcrt.getch()
    else:  # For Unix-like systems
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print("")


def display_menu():
    print("Customer Management Menu\n")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit\n")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_valid_input(prompt_message, validation_func, error_message):
    while True:
        user_input = input(prompt_message).strip()
        if validation_func(user_input):
            return user_input
        else:
            print(error_message)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    client = Client(HOST, PORT)
    client.run()
