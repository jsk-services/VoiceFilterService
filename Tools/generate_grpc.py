import os

if __name__ == "__main__":
    for file in os.listdir("../Protocols"):
        if file.endswith(".proto"):
            os.system(f"python -m grpc_tools.protoc "
                      f"-I../Protocols "
                      f"--python_out=../ "
                      f"--pyi_out=../ "
                      f"--grpc_python_out=../ "
                      f"../Protocols/{file}")