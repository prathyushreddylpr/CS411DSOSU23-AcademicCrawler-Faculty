import csv
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = '/Users/shubhijain/Downloads/awards-20230530.xml'

# Parse the XML file and get the root element
tree = ET.parse(xml_file)
root = tree.getroot()

# Find all 'award' elements
award_elements = root.findall('award')

# Define the CSV file path
csv_file = 'awards_data.csv'

# Define the field names for CSV
fieldnames = ['award_id', 'award_number', 'sponsor_id', 'sponsor_name', 'award_year', 'amount', 'award_name', 'recipient', 'faculty']

# Open the CSV file in write mode
with open(csv_file, 'w', newline='') as file:
    # Create a CSV writer object
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    count = 0
    investigator = None
    project_leader = None

    # Iterate over each 'award' element
    for award_element in award_elements:
        # Increment the counter
        count += 1

        # Extract the desired fields
        award_number = award_element.find('award_number').text
        award_id = award_element.get('id')
        sponsor_id = award_element.find('sponsors/sponsor').get('id')
        sponsor_name = award_element.find('sponsors/sponsor').text
        fiscal_year = award_element.find('fiscal_year').text
        amount_awarded = award_element.find('amount_awarded').text
        award_title = award_element.find('award_title').text
        recipients = award_element.find('recipients').text
        principal_investigator = award_element.find('principal_investigators').text
        if (principal_investigator):
            investigator = principal_investigator.split(':')
        if (investigator and len(investigator) == 2):
            project_leader = investigator[1].strip()

        # Write the data row to the CSV file
        writer.writerow({
            'award_id': award_id,
            'award_number': award_number,
            'sponsor_id': sponsor_id,
            'sponsor_name': sponsor_name,
            'award_year': fiscal_year,
            'amount': amount_awarded,
            'award_name': award_title,
            'recipient': recipients,
            'faculty': project_leader
        })

    # Print the count of award records
    print("Total Award Records:", count)

