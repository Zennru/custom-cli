def main():
    while True:
        try:
            user_input = input("JenShell> ")

            if user_input == "exit":
                print("Keluar dari Jenshell. Sampai jumpa!")
                break

        except KeyboardInterrupt:
            print()  # Newline setelah ^C
            continue

if __name__ == "__main__":
    main()