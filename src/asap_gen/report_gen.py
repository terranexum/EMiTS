import math
import os, sys
import pandas as pd
import locale
import datetime
import xlrd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from os import devnull
from dotenv import load_dotenv

load_dotenv()

# Set the directory path to search
DIR_PATH = os.getenv('DIR_PATH')

def generate_report_content(file_path, pdf_path, doc):

    #print('Working on', file_path)

    # read in data from utility spreadsheet


    wb = xlrd.open_workbook(file_path, logfile=open(devnull, 'w'))
    df = pd.read_excel(wb, engine='xlrd')
    

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

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    '''
    This code uses the SimpleDocTemplate class to create a PDF document and the
    Paragraph, Spacer, Table, and TableStyle classes to add content to the document. 
    It also uses the getSampleStyleSheet function to define styles for the content.

    '''


    # Create a list for the individual content to be added
    content = []

    # extract filename without extension
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    #print(filename)

    # remove last 4 characters
    asap_area = filename[:-4]
    #print(asap_area)

    # get report date
    today = datetime.date.today()
    asap_date = today.strftime("%B %d, %Y")

    # Add the document heading
    content.append(Paragraph(asap_area, styles['Heading1']))
    content.append(Paragraph("Accelerated Sustainability Action Plan (ASAP) | TerraNexum Inc.", styles['Heading2']))
    content.append(Paragraph(asap_date, styles['Heading3']))
    content.append(Spacer(1, 0.2 * inch))


    '''
    Introductory Section
        Brief overview of the purpose and goals of the plan
    '''

    # Add the heading
    content.append(Paragraph("Section 1. Introduction", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # create a Paragraph object with the introductory section text and style
    content.append(Paragraph("TerraNexum's goal is to develop and help implement accelerated plans for renewable energy and energy storage deployment to achieve profitable emissions reduction at city and county levels - at the scale of multiple megatons of CO2 emissions reductions.", styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))
    content.append(Paragraph("Our ASAPs seek to outline goals and strategies for achieving a complete shift to renewable energy supply on an accelerated timeline within this specific locality. At this time, we are presenting facts and figures for decarbonizing electricity consumption through replacement with renewable energy production and energy storage systems.", styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))






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

    # extract value of cells

    # Set the locale to the user's default
    locale.setlocale(locale.LC_ALL, '')

    # Format the number as currency with a dollar sign and commas
    #c_annual_cost = locale.currency(c_annual_cost, symbol=True, grouping=True)

    total_cost = 0
    total_co2 = 0
    rshift = -2
    cshift = -1

    c_customer_base = df.iloc[40+rshift, 3+cshift]
    c_annual_demand_kWh = df.iloc[40+rshift, 4+cshift]
    c_annual_cost = df.iloc[40+rshift, 6+cshift]
    c_co2_emissions = df.iloc[40+rshift, 5+cshift]
    r_customer_base = df.iloc[41+rshift, 3+cshift]
    r_annual_demand_kWh = df.iloc[41+rshift, 4+cshift]
    r_annual_cost = df.iloc[41+rshift, 6+cshift]
    r_co2_emissions = df.iloc[41+rshift, 5+cshift]
    
    c_frac_cost_savings = 0.8
    r_frac_cost_savings = 0.8

    no_elec_flag = False

    if not pd.isnull(c_customer_base): c_customer_base = pd.to_numeric(c_customer_base, errors='coerce', downcast='integer')
    else: c_customer_base = 0
        
    if not pd.isnull(c_annual_demand_kWh): c_annual_demand_kWh = pd.to_numeric(c_annual_demand_kWh, errors='coerce', downcast='integer')
    else: c_annual_demand_kWh = 0
    
    if not pd.isnull(c_annual_cost): c_annual_cost = c_annual_cost
    else: c_annual_cost = 0
    
    if not pd.isnull(c_co2_emissions): c_co2_emissions = pd.to_numeric(c_co2_emissions, errors='coerce', downcast='integer')
    else: c_co2_emissions = 0

    if not pd.isnull(r_customer_base): r_customer_base = pd.to_numeric(r_customer_base, errors='coerce', downcast='integer')
    else: r_customer_base = 0
        
    if not pd.isnull(r_annual_demand_kWh): r_annual_demand_kWh = pd.to_numeric(r_annual_demand_kWh, errors='coerce', downcast='integer')
    else: r_annual_demand_kWh = 0
    
    if not pd.isnull(r_annual_cost): r_annual_cost = r_annual_cost
    else: r_annual_cost = 0

    if not pd.isnull(r_co2_emissions): r_co2_emissions = pd.to_numeric(r_co2_emissions, errors='coerce', downcast='integer')
    else: r_co2_emissions = 0

    if c_customer_base == 0 or r_customer_base == 0:
        print("Customer count missing for", asap_area)
        no_elec_flag = True

    total_cost += c_annual_cost
    total_cost += r_annual_cost

    total_co2 += c_co2_emissions
    total_co2 += r_co2_emissions

    if no_elec_flag == True:
        # Add heading
        content.append(Paragraph("No Electrical Customers at Present", styles['Heading2']))
        content.append(Spacer(1, 0.2 * inch))
        content.append(Paragraph("Although there are data for this locality for commercial and/or residential energy usage, no customers were reported receiving electric service. It is likely that the reported service is only for natural gas.", styles['Normal']))
        content.append(Spacer(1, 0.2 * inch))
        content.append(Paragraph("Please check back at a later time when our ASAPs account for achieving emissions reductions where natural gas is being used as well.", styles['Normal']))
        content.append(Spacer(1, 0.2 * inch))

        return content

    # Add the heading
    content.append(Paragraph("Section 2. Current Energy Usage and Cost", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # Create the table data
    c_customers = locale.format_string("%d", c_customer_base, grouping=True)
    r_customers = locale.format_string("%d", r_customer_base, grouping=True)

    c_kWh = locale.format_string("%d", c_annual_demand_kWh, grouping=True)
    r_kWh = locale.format_string("%d", r_annual_demand_kWh, grouping=True)

    c_cost = locale.currency(c_annual_cost, symbol=True, grouping=True)
    r_cost = locale.currency(r_annual_cost, symbol=True, grouping=True)

    c_co2 = locale.format_string("%d", c_co2_emissions, grouping=True)
    r_co2 = locale.format_string("%d", r_co2_emissions, grouping=True)

    data = [['', 'Commercial', 'Residential'],
            ['Number of Customers', c_customers, r_customers],
            ['Total kWh Consumed', c_kWh, r_kWh],
            ['Total Cost of Electricity', c_cost, r_cost],
            ['Total CO2 Emissions', c_co2, r_co2]
            ]

    section_content = f"The numbers in this section were supplied from the 2021 Community Energy Report for this locality, as published by Xcel Energy on its website. A copy of this report is available within the source folder on our GitHub repository where this ASAP was published. The potential is high for " + asap_area + " to achieve rapid emissions reductions.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    # Create the table and add it to the content
    table = Table(data, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 10)])
    content.append(table)
    content.append(Spacer(1, 0.2 * inch))





    '''
    Potential Cost Savings with Prime Mover System
        Cost of a Prime Mover system
        Potential revenue generation by owning a Prime Mover system
        Calculation of potential cost savings for commercial and residential customers who switch to Prime Mover systems

    This code creates a table with the relevant data, and adds a brief conclusion about
    the cost savings.

    '''

    # Add the heading
    content.append(Paragraph("Section 3. Potential Cost Savings with Our Prime Mover Program", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # Define data for the table
    current_mo = locale.currency(c_annual_cost/c_customer_base/12, symbol=True, grouping=False)
    proposed_mo = locale.currency((c_annual_cost/c_customer_base/12)*(1-c_frac_cost_savings), symbol=True, grouping=False)
    c_pm_savings_mo = (c_annual_cost/c_customer_base/12)*(c_frac_cost_savings)
    savings_mo = locale.currency(c_pm_savings_mo, symbol=True, grouping=False)
    savings_yr = locale.currency(((c_annual_cost/c_customer_base/12)*(c_frac_cost_savings)) * 12, symbol=True, grouping=False)

    data_c = [
        ['Commercial Savings', 'Amount'],
        ['Monthly Electric Bill Today', str(current_mo)],
        ['Monthly Electric Bill after Prime Mover', str(proposed_mo)],
        ['Monthly Cost Savings', str(savings_mo)],
        ['Yearly Cost Savings', str(savings_yr)],
    ]

    current_mo = locale.currency(r_annual_cost/r_customer_base/12, symbol=True, grouping=False)
    proposed_mo = locale.currency((r_annual_cost/r_customer_base/12)*(1-r_frac_cost_savings), symbol=True, grouping=False)
    r_pm_savings_mo = (r_annual_cost/r_customer_base/12)*(r_frac_cost_savings)
    savings_mo = locale.currency(r_pm_savings_mo, symbol=True, grouping=False)
    savings_yr = locale.currency(((r_annual_cost/r_customer_base/12)*(r_frac_cost_savings)) * 12, symbol=True, grouping=False)

    data_r = [
        ['Residential Savings', 'Amount'],
        ['Monthly Electric Bill Today', str(current_mo)],
        ['Monthly Electric Bill after Prime Mover', str(proposed_mo)],
        ['Monthly Cost Savings', str(savings_mo)],
        ['Yearly Cost Savings', str(savings_yr)],
    ]

    section_content = f"Our Prime Mover program is literally designed to bring “power to the people” on multiple levels. People can be in charge of their own energy future by supplying renewable power to themselves at home and to their companies at work. This results in lower electric bills for themselves, their employers, and for commercial building owners. Once a Prime Mover owns their equipment, which consists of at least one portable solar charging station and a battery energy storage unit, they will be able to ensure their own sutstainability and resilience while profitably serving their community in doing the same. They will also be able to add to a growing market supporting local electricians and renewable energy companies who can provide upgrades such as EV charging conversions directly. New jobs and new businesses will then have an opportunity to spring up to satisfy this demand as it continues to grow.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))
    

    # Add the table
    table = Table(data_c, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 10)])
    content.append(table)
    #content.append(Spacer(1, 0.5*inch))

    # Add the table
    table = Table(data_r, style=[('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 10)])
    content.append(table)
    content.append(Spacer(1, 0.5*inch))

    # Funding Innovations
    section_content = f"The Prime Mover Program has two segments, commercial/industrial as well as residential. For businesses with commercial and industrial buildings, Colorado's C-PACE is an innovative program that offers financing of up to 30% of a building's value, and assesses those repayments on the annual property tax for that property for up to 25 years. This financing is in addition to tax credits and incentives at federal, state, and local levels.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))
    section_content = f"For residences, C-PACE is not available, but residential loans such as those available through Colorado's RENU program as well as federal and state tax credits already exist for home solar installations as well as battery storage.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))
    content.append(Paragraph('By purchasing one or more Prime Mover systems under our program, businesses and homes can save significant amounts of money on their monthly electricity bills. Over the course of a year, this can add up to a substantial amount of savings, making the initial investment in the Prime Mover system well worth it.', styles['Normal']))
    content.append(Spacer(1, 0.5*inch))
    content.append(Paragraph('Prime Mover systems are ideal as the foundation of an open source hardware platform. Software that is developed by and for system users to expand the capabilities of their systems could be released for free under open source licenses for the broadest personal, non-profit, and commercial use.', styles['Normal']))
    content.append(Spacer(1, 0.5*inch))


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

    # Add the heading
    content.append(Paragraph("Section 4. Transition to 100% Renewable Energy", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    pm_unit_gen_kWh = 20.484
    pm_unit_gen_capex = 27000
    pm_unit_gen_count = 0
    pm_unit_storage_kWh = 20
    pm_unit_storage_capex = 12882
    pm_unit_storage_count = 0
    pm_unit_shipping = 850
    pm_unit_w_profit = 1.20 * (pm_unit_gen_capex + pm_unit_storage_capex + pm_unit_shipping)

    # Calculate number of Prime Mover systems needed for 100% renewable energy
    total_energy_usage = r_annual_demand_kWh + c_annual_demand_kWh
    pm_system_capacity = pm_unit_storage_kWh
    pm_systems_needed = math.ceil(total_energy_usage / pm_system_capacity / 365)
    pm_system_cost = pm_unit_w_profit + pm_unit_shipping
    total_pm_systems_cost = locale.currency(pm_system_cost * pm_systems_needed, symbol=True, grouping=True)
    pm_system_price = locale.currency(pm_system_cost, symbol=True, grouping=True)
    
    pm_system_savings_c_yr = c_pm_savings_mo * 12
    pm_system_savings_r_yr = r_pm_savings_mo * 12
    pm_system_savings = pm_system_savings_c_yr + pm_system_savings_r_yr
    #print(total_cost, pm_system_savings)
    pm_total_savings = pm_system_savings * pm_systems_needed
    
    payback_period = (pm_system_cost * pm_systems_needed) / pm_total_savings
    if payback_period > 25:
        print("Payback period of", str(payback_period), "too long for", asap_area, ". Not outputting report.")
        return []
    

    pm_systems_needed = locale.format_string("%d", pm_systems_needed, grouping=True)
    pm_system_savings = locale.currency(pm_system_savings, symbol=True, grouping=True)
    pm_total_savings = locale.currency(pm_total_savings, symbol=True, grouping=True)
    
    # Add content to section

    section_content = f"A single Prime Mover system costs {pm_system_price}. To transition to 100% renewable energy, it would require {pm_systems_needed} Prime Mover systems to provide enough electricity for all residential and commercial customers in " + asap_area + ". This would cost {total_pm_systems_cost} to implement.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"With the energy savings Prime Mover owners would see by generating and storing their own electricity, which is {pm_system_savings} per year per system and thus {pm_total_savings} per year across all systems within " + asap_area + ", the Prime Mover systems could pay for themselves in {payback_period:.0f} years.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"This timeframe is too long for businesses to have to wait to be cash flow positive. Below, we present information on Colorado's C-PACE program, an innovative program that would allow Prime Mover systems associated with commercial/industrial buildings and properties to be financed over as much as 25 years. Already, 118 projects have been financed with $250M in project financing, resulting in 781,603 tons of lifetime GHG emissions reduction and $77.9M of lifetime cost savings. Projects have been as small as $53K to as large as $55.5M.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))


    '''
    Making it Happen
        C-PACE Program Information 
        Timeline for transition to 100% renewable energy
    '''

    # Add the heading
    content.append(Paragraph("Section 5. Profitably Funding this Transition", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # Add content to section
    section_content = f"C-PACE (Colorado Property Assessed Clean Energy) is a statewide financing program for financing projects in renewable energy, energy efficiency, and water conservation, to include both retrofits as well as new construction. Projects are financed through private capital. C-PACE is designed to be a self-sustaining program and is sponsored by the Colorado Energy Office (CEO).\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"With the advent of C-PACE, Class B and C buildings now have no reason to remain inefficient and more costly to operate now that the following benefits are possible, as reported by the Rocky Mountain Institute (RMI) in February 2020: a 15% or greater savings with bundled low and no cost improvements, a 35% savings with capital improvements, NOI (net operating income) increases between 2.4 and 5.6%, and property value increases between $5 and $11 per SF. Thus, for a 50,000 SF building, a building owner could see $250,000 to $550,000 in increased value. \n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"C-PACE is an innovative financing tool for existing buildings that provides commercial and industrial building owners with the following benefits: 1) 100% financing - no out-of-pocket expenses, 2) is long-term, up to 25 years at a fixed interest rate, and 3) financing is done through a special purpose tax assessment on a property, such that C-PACE payments get paid annually through the property tax bill. The repayment obligation is transferrable to new building owners upon sale of the property, and no personal guarantees or positive cash flow are required to secure this financing. If you have tenants or hotel guests, the tax assessment can be passed through to them.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"The goal of C-PACE is for energy savings to be greater than the PACE payments, enabling cash flow positive projects from day one.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Eligible commercial and industrial property types include: offices, retail stores, hotels, industrial plants, agricultural facilities, healthcare facilities, mixed-use facilities, education (non-public), warehouses/storage buildings, non-profit buildings (non-public), and multifamily buildings with 5 or more units.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Eligible improvements include solar PV, EV charging stations, energy storage, beneficial electrification, high-efficiency lighting, and more. Costs related to eligible improvements are also eligible, which include: engineering studies, architectural fees, energy audits, renewable energy feasibility studies, roof upgrades associated with rooftop solar PV, building structural reinforcement upgrades to support rooftop solar PV, environmental clean-up activities needed to install eligible equipment, commissioning and maintenance contracts up to five years, equipment extended warranties (as for PV system inverters), finance closing costs, and fees to administer the program (2.25% of project costs, capped at $50,000.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))



    '''
    Community Benefits through TerraNexum
    '''

    # Add the heading
    content.append(Paragraph("Section 6. Community Benefits through TerraNexum", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # Add content to section
    section_content = f"Our name TerraNexum means 'earth network.' Our company works to accelerate the energy and carbon transition by designing intelligent networks of systems able to advance sustainability and resilience. We develop these systems through applying our extensive knowledge in managing energy, carbon, and other resources, and we design optimized networks to aid in energy, resource, and information flows using the tools of quantum optimization, geospatial and subsurface analytics, and cloud computing.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Our energy and carbon management partners are in all major stakeholder areas, from renewable energy production and storage to electric utilities, companies who wish to remove carbon from the atmosphere, even companies wishing to renovate old oil/gas reservoirs to provide clean, large-scale utility storage of renewable energy. Wherever energy and carbon intersect, there is a point on our network to integrate that work.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Our technology partners include businesses within cloud computing and quantum computing. We are participants within NVIDIA's Inception Program, Microsoft's Startups Hub, and AWS Activate.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Our community partners include universities and groups able to benefit from the free and open-source, open-hardware work we do and seek to continue to do. We are seeking to help local universities within Colorado raise $30M for both quantum and sustainability R&D and workforce development. \n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"Our next step, with the data and results provided in this report, is to create a detailed geospatial visualization of how " + asap_area + " can be serviced over time to reach 100% renewable energy over various timeframes. Watch how the energy transition could unfold, through monthly snapshots into the future.\n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"For additional information on any of the above and for references for your further outreach, please use the contact information below. \n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))


    '''
    Contact Information
    '''

    # Add the heading
    content.append(Paragraph("Contact Information", styles['Heading2']))
    #content.append(Spacer(1, 0.2 * inch))

    # Add content to section
    section_content = f"For Prime Mover Program inquiries, please contact Dahl Winters, the Chief Executive Officer at TerraNexum Inc., at dwinters@terranexum.com, 303-800-5707. You can also read more about TerraNexum at terranexum.com. \n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))

    section_content = f"For C-PACE inquiries, please contact Tracy Phillips, the Program Director at C-PACE, at tphillips@copace.com, 720-933-8143. You can also read more about C-PACE at copace.com. \n\n"
    content.append(Paragraph(section_content, styles["Normal"]))
    content.append(Spacer(1, 0.2 * inch))


    '''
    Build the final document

    This code builds the PDF using the build method of the SimpleDocTemplate class. 
    '''

    return content




print('dir_path', DIR_PATH)
# Loop through all files in the directory
for root, dirs, files in os.walk(DIR_PATH):
    for file in files:
        # Check if the file has a .xls extension
        if file.endswith('.xls'):

            try:
                # Get the full path to the file
                file_path = os.path.join(root, file)
                
                # Create a new PDF with reportlab
                pdf_path = os.path.splitext(file_path)[0] + '.pdf'

                if os.path.exists(pdf_path): os.remove(pdf_path) 

                # create a PDF document with letter size paper
                doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=72,
                    leftMargin=72, topMargin=72, bottomMargin=72)

                # Add content to the PDF here and build
                report = generate_report_content(file_path, pdf_path, doc)

                if len(report) > 0:
                    doc.build(report)

            except Exception as err:
                print(pdf_path, f"Unexpected {err=}, {type(err)=}")
                raise


            #sys.exit(1)
