# VATI_Grant_Report
parses the PDF from the pretty salesforce site to actually be able to track the data

The site VATI uses does not export to csv so you can compare how different counties are doing. their this was purposeful or not, this is a way to to make it a csv for a broader overview of the performance of the different VATI grant funded projects.

HOWTO:
- use the VATI dash board and select the county on the top left, my computer then highlights the area then requires me to see where the county/area is then you must click on the area to see the report.
- at the bottom there is a download button, click to download it as pdf.  do this for all counties (50ish)
- put his py script in the same folder as the downloaded pdfs... this script will process all pdf's so use its own folder
- call the script.
- it should output an 'output.csv' to open with your spreadsheet folder.  options are: delimit->tab  encoding->ASCII no qoutes around strings



Thomas Sweeney
Thomas@sweeney.ai
