def exitShell():
    print("Leaving Jenshell. See you later!")

def main():
    while True:
        try:
            user_input = input("JenShell> ")
        except EOFError:
            exitShell()
            break
        
        if user_input.strip() == "exit":
            exitShell()
            break

        if user_input.strip() == "":
            continue
            
        args = user_input.split()
        command = args[0]
        arguments = args[1:]

        print(f"Command   : {command}")
        print(f"Arguments : {arguments}")

if __name__ == "__main__":
    main()