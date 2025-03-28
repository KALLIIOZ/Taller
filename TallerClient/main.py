import tkinter
from logic.user import User

def main():
    user = User()
    print(user.get_user(4))

if __name__ == "__main__":
    main()