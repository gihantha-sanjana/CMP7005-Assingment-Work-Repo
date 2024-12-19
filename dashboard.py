import subprocess
import sys

# Function to install packages from requirements.txt
def install_requirements():
    try:
        # Install packages using subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")

# Call the function to install requirements
install_requirements()

import pickle
# Load the pickle file
with open("https://github.com/gihantha-sanjana/CMP7005-Assingment-Work-Repo/blob/main/DataSet/random_forest_model.pkl","rb") as file:
    data = pickle.load(file)

# Load the DataSet
print(data)