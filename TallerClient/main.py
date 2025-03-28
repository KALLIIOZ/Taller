import tkinter
from logic.user import User

def main():
    user = User()
    print(user.auth("somy", "root"))

if __name__ == "__main__":
    main()