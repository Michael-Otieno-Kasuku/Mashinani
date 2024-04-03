# Generated by Django 5.0.2 on 2024-04-03 13:18

from django.db import migrations
import openpyxl
from django.core.exceptions import ObjectDoesNotExist

def insert_financial_years(apps, schema_editor):
    FinancialYear = apps.get_model('mashinani', 'FinancialYear')

    try:
        # Load data from Excel workbook
        wb = openpyxl.load_workbook('mashinani/data/data.xlsx')
        sheet = wb['FinancialYear']

        # Iterate over rows in the Excel sheet and extract financial year information
        financial_years_data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from second row
            financial_year = row[0]  # Assuming Financial Year is in the first column
            financial_year_status = row[1]  # Assuming Financial Year Status is in the second column
            
            # Create dictionary for financial year data
            financial_year_data = {
                'financial_year': financial_year,
                'financial_year_status': financial_year_status
            }
            
            # Append financial year data to list
            financial_years_data.append(financial_year_data)

        # Insert data into the model
        for data in financial_years_data:
            FinancialYear.objects.create(**data)
    except FileNotFoundError:
        print("File not found. Please check the path to the Excel file.")
    except Exception as e:
        print(f"An error occurred: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('mashinani', '0010_auto_20240403_1612'),
    ]

    operations = [
        migrations.RunPython(insert_financial_years)
    ]