#!/bin/bash
export PATH="/home/ubuntu/miniconda3/bin:/home/ubuntu/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

# 1. Initialize Conda (only if not already initialized)
if ! conda info > /dev/null 2>&1; then
  echo "Initializing Conda..."
  conda init bash  # Replace bash with your shell if needed
  # The following line restarts the current shell, but ONLY AFTER the conda init command
  exec bash  # Replace bash with your shell if needed, also zsh or fish.
  exit 0 #This exit here will ensure that the script ends after the new shell is executed.
fi

# 2. Activate the Conda environment
echo "Activating Conda environment..."

cd $HOME/HeilbronnScraper
source ~/miniconda3/etc/profile.d/conda.sh
export PATH="/home/ubuntu/miniconda3/bin:/home/ubuntu/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
conda activate scrap_venv

# 3. Run the Python script
echo "Running Python script..."
python $HOME/HeilbronnScraper/main.py

echo "Script finished."
echo "==============================================================="
echo "==============================================================="