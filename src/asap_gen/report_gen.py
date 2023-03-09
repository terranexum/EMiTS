import math
import os, sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Set the directory path to search
dir_path = '../ASAPs/USA/Colorado/Cities'

def generate_report_content(file_path):

    # read in data from utility spreadsheet
    df = pd.read_excel(file_path)

    # Use the 'thousands' argument to specify the thousands separator
    df = pd.to_numeric(df, errors='coerce', downcast='integer')

    # Use the 'converters' argument to remove the '$' symbol and any commas from the currency value
    currency_converter = lambda x: float(x.replace('$', '').replace(',', '')) if isinstance(x, str) else x
    df = pd.to_numeric(df.apply(currency_converter), errors='coerce')


    '''
    Introduction
        Brief overview of the purpose and goals of the plan

    Current Energy Usage and Cost
        Number of commercial customers and their total energy consumption in kWh last year
        Total cost of electricity for commercial customers
        Number of residential customers and their total energy consumption in kWh last year
        Total cost of electricity for residential customers

    Potential Cost Savings with Prime Mover System
        Cost of a Prime Mover system
        Potential revenue generation by owning a Prime Mover system
        Calculation of potential cost savings for commercial and residential customers who switch to Prime Mover systems

    Transition to 100% Renewable Energy
        Calculation of the number of Prime Mover systems needed to supply 100% renewable energy to commercial and residential customers
        Timeline for transition to 100% renewable energy

    Conclusion
        Summary of the plan and its potential benefits
    '''

    # define the output file name
    output_filename = "sustainability_plan.pdf"

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    '''
    This code uses the SimpleDocTemplate class to create a PDF document and the
    Paragraph, Spacer, Table, and TableStyle classes to add content to the document. 
    It also uses the getSampleStyleSheet function to define styles for the content.

    '''
    # create a PDF document with letter size paper
    doc = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=18)





    '''
    Introductory Section
        Brief overview of the purpose and goals of the plan
    '''

    # define the introductory section text
    intro_text = "Introductory Section\n\nThis sustainability plan outlines the goals and strategies for achieving 100% renewable energy supply to commercial and residential customers."

    # define the style for the introductory section text
    intro_style = ParagraphStyle(
        name="IntroStyle",
        fontSize=14,
        leading=14*1.2,
        spaceBefore=0.5*inch,
        spaceAfter=0.5*inch,
    )

    # create a Paragraph object with the introductory section text and style
    intro_paragraph = Paragraph(intro_text, intro_style)

    # add the Paragraph object to the document
    doc.addPageTemplates([intro_paragraph])



    '''
    Current Energy Usage and Cost
        Number of commercial customers and their total energy consumption in kWh last year
        Total cost of electricity for commercial customers
        Number of residential customers and their total energy consumption in kWh last year
        Total cost of electricity for residential customers

    The code adds a heading for the Current Energy Usage and Cost section to the 
    content list and creates a spacer to add some whitespace. It then creates a table 
    with the data and adds it to the content list.
    '''


    # Create a list for the content
    content = []

    # extract value of cells

    c_customer_base = df.iloc[40, 3]
    c_annual_demand_kWh = df.iloc[40, 4]
    c_annual_cost = df.iloc[40, 6]
    c_co2_emissions = df.iloc[40, 5]
    c_frac_demand_served = 1
    c_frac_cost_savings = 0.2

    r_customer_base = df.iloc[41, 3]
    r_annual_demand_kWh = df.iloc[41, 4]
    r_annual_cost = df.iloc[41, 6]
    r_co2_emissions = df.iloc[41, 5]
    r_frac_demand_served = 1
    r_frac_cost_savings = 0.2



    # calculate total energy consumption in kWh
    total_kwh = c_annual_demand_kWh + r_annual_demand_kWh

    # calculate total cost of electricity
    total_cost = c_annual_cost + r_annual_cost

    # print results
    print('Total energy consumption (kWh):', total_kwh)
    print('Total electricity cost:', total_cost)


    # Add the heading
    content.append(Paragraph("Current Energy Usage and Cost", styles['Heading1']))
    content.append(Spacer(1, 0.2 * inch))

    # Create the table data
    data = [['', 'Commercial', 'Residential'],
            ['Number of Customers', c_customer_base, r_customer_base],
            ['Total kWh Used Last Year', c_annual_demand_kWh, r_annual_demand_kWh],
            ['Total Spent on Electricity Last Year', '$' + str(c_annual_cost), '$' + str(r_annual_cost)]]

    # Create the table and add it to the content
    table = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 10)])
    content.append(table)




    '''
    Potential Cost Savings with Prime Mover System
        Cost of a Prime Mover system
        Potential revenue generation by owning a Prime Mover system
        Calculation of potential cost savings for commercial and residential customers who switch to Prime Mover systems

    This code creates a table with the relevant data, and adds a brief conclusion about
    the cost savings.

    '''


    # Create the table data
    data = [['', 'Commercial', 'Residential'],
            ['Number of Customers', c_customer_base, r_customer_base],
            ['Total kWh Used Last Year', c_annual_demand_kWh, r_annual_demand_kWh],
            ['Total Spent on Electricity Last Year', '$' + str(c_annual_cost), '$' + str(r_annual_cost)]]


    # Define data for the table

    current_mo = c_annual_cost/c_customer_base/12
    proposed_mo = current_mo*(1-c_frac_cost_savings)
    savings_mo = current_mo - proposed_mo
    savings_yr = savings_mo * 12

    data_c = [
        ['Potential Cost Savings with Prime Mover System - Commercial'],
        [''],
        ['Current Electricity Cost Per Month', '$' + str(current_mo)],
        ['Proposed Cost with Prime Mover System Per Month', '$' + str(proposed_mo)],
        ['Monthly Cost Savings', '$' + str(savings_mo)],
        ['Yearly Cost Savings', '$' + str(savings_yr)],
    ]

    current_mo = r_annual_cost/r_customer_base/12
    proposed_mo = current_mo*(1-r_frac_cost_savings)
    savings_mo = current_mo - proposed_mo
    savings_yr = savings_mo * 12

    data_r = [
        ['Potential Cost Savings with Prime Mover System - Residential'],
        [''],
        ['Current Electricity Cost Per Month', '$' + str(current_mo)],
        ['Proposed Cost with Prime Mover System Per Month', '$' + str(proposed_mo)],
        ['Monthly Cost Savings', '$' + str(savings_mo)],
        ['Yearly Cost Savings', '$' + str(savings_yr)],
    ]





    # Add the section header
    content.append(Paragraph('<h2>Potential Cost Savings with Prime Mover System</h2>', styles['Heading2']))

    # Add a spacer
    content.append(Spacer(1, 0.25*inch))

    # Add the table
    t=Table(data, len(data[0])*[1.5*inch], len(data)*[0.4*inch])
    t.setStyle(TableStyle([
                        ('TEXTCOLOR',(0,0),(-1,0),styles['Heading3'].textColor),
                        ('BACKGROUND',(0,0),(-1,0),styles['Heading3'].backgroundColor),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('ALIGN',(0,0),(-1,0),'CENTER'),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
                        ('BACKGROUND', (0, 1), (-1, 1), '#F0F0F0'),
                        ('GRID', (0, 0), (-1, -1), 0.25, '#CCCCCC')
                        ]))
    content.append(t)

    # Add a spacer
    content.append(Spacer(1, 0.5*inch))

    # Add a conclusion
    content.append(Paragraph('By switching to the Prime Mover system, businesses and homes can save significant amounts of money on their monthly electricity bills. Over the course of a year, this can add up to a substantial amount of savings, making the initial investment in the Prime Mover system well worth it.', styles['Normal']))



    '''
    Transition to 100% Renewable Energy
        Calculation of the number of Prime Mover systems needed to supply 100% renewable energy to commercial and residential customers
        Timeline for transition to 100% renewable energy

    This code calculates the number of Prime Mover systems needed to provide 100% 
    renewable energy for all residential and commercial customers, based on the total 
    energy usage calculated in the previous section. It then calculates the cost of 
    implementing the necessary number of systems, and notes that the revenue generated 
    by selling electricity back to the grid could help to pay for the systems in a 
    relatively short amount of time. Finally, it adds the content to the section and 
    appends it to the story.

    '''

    # Section 4: Transition to 100% Renewable Energy
    section_title = "4. Transition to 100% Renewable Energy\n\n"
    content.append(Paragraph(section_title, styles["Heading2"]))

    pm_unit_gen_kWh = 20.484
    pm_unit_gen_capex = 27000
    pm_unit_gen_count = 0
    pm_unit_storage_kWh = 20
    pm_unit_storage_capex = 12882
    pm_unit_storage_count = 0
    pm_unit_w_profit = 1.20 * (pm_unit_gen_capex + pm_unit_storage_capex)
    pm_unit_shipping = 850



    # Calculate number of Prime Mover systems needed for 100% renewable energy
    total_energy_usage = r_annual_demand_kWh + c_annual_demand_kWh
    pm_system_capacity = pm_unit_storage_kWh
    pm_systems_needed = math.ceil(total_energy_usage / pm_system_capacity)
    pm_system_cost = pm_unit_w_profit + pm_unit_shipping
    total_pm_systems_cost = pm_system_cost * pm_systems_needed
    total_current_cost = total_cost
    payback_period = total_pm_systems_cost / total_current_cost

    # Add content to section
    section_content = f"To transition to 100% renewable energy, it would require {pm_systems_needed} Prime Mover systems to provide enough electricity for all residential and commercial customers. This would cost ${pm_systems_needed * pm_system_cost:,} to implement. However, with the revenue generated by selling electricity back to the grid, the Prime Mover systems could pay for themselves in as little as {payback_period:.2f} years.\n\n"

    content.append(Paragraph(section_content, styles["Normal"]))




    '''
    Build the final document

    This code builds the PDF using the build method of the SimpleDocTemplate class. 
    '''

    # Build the PDF
    doc.build(content)


# Loop through all files in the directory
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # Check if the file has a .xls extension
        if file.endswith('.xls'):
            # Get the full path to the file
            file_path = os.path.join(root, file)
            
            # Create a new PDF with reportlab
            pdf_path = os.path.splitext(file_path)[0] + '.pdf'
            c = canvas.Canvas(pdf_path)
            
            # Add content to the PDF here
            generate_report_content(file_path)
            
            # Save the PDF and close the canvas
            c.save()

            sys.exit(1)
