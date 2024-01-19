def main_function():
    import os
    import subprocess

    # Specify the path to your DLLs folder
    dlls_folder = os.path.join(os.path.dirname(__file__), "..\\PyQt5\\Qt5\\bin")
    designer_location =os.path.join(os.path.dirname(__file__) , "bin\designer.exe")
    #print(dlls_folder)

    # Get the current PATH
    current_path = os.environ.get("PATH", "")
    #print(current_path)


    # Add the DLLs folder to the PATH
    os.environ["PATH"] = f"{dlls_folder};{current_path}"

    # Run your executable
    #print("Current Working Directory:", os.getcwd())
    subprocess.run([designer_location])
    input()

if __name__ == "__main__":
    main_function()