# Create yesterday's date string
$date = Get-Date; 
$yesterday=$date.AddDays(-1); 
$yesterday_date = $yesterday.ToString('yyyy-MM-dd')

# Download access logs 
scp bertwagner@bertwagner.com:~/logs/bertwagner.com/https/access.log.$yesterday_date ./access.log

# Activate the virtual env
./.venv/scripts/activate.ps1

# Run the python script
python process_data.py