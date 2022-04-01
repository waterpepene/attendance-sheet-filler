
# attendance-sheet-filler  
This repo is used to fill in the MCAST apprenticeship scheme attendance sheets with the data you provide. Once you've entered the data, you'll only need to run the script once a month to have an attendance sheet that's already filled out!

To start, fill in all the details in **details.json**, and be sure to preserve formatting and **don't** change any **key names** (like changing *company_name* to *companyName*).
______________________
Everything is pretty self explanatory, but there are a few things to note:

 - **"school_days"**	->  This list is there to mark the days when you're at school, so that the script can mark "E" on the sheet. It goes from 0 to 6, with **0 being Sunday**.
- **"coords_to_ignore"** -> These are coordinates in the form [week, day], that the script will entirely ignore writing over them. For example, if we have "coords_to_ignore": [0,1], the Monday of the first week (week 1 is index 0) is ignored.
 I added this in case of public holidays and the first few days that don't have a date on them.
 - **"font_size"** -> lower this number in case the text overlaps or doesn't fit, or if it fits too well, increase it as you want.
 ______________________________

To install
- Clone this repo
- pip install -r requirements.txt
- main.py