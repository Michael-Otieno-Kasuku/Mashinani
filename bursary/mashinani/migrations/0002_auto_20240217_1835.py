from django.db import migrations

def insert_institutions(apps, schema_editor):
    Institution = apps.get_model('mashinani', 'Institution')

    universities_list = [
        "University of Nairobi",
        "Kenyatta University",
        "Egerton University",
        "Moi University",
        "Strathmore University",
        "Jomo Kenyatta University of Agriculture and Technology",
        "Maseno University",
        "Kisii University",
        "Technical University of Kenya",
        "United States International University",
        "Daystar University",
        "Mount Kenya University",
        "African Virtual University",
        "Maasai Mara University",
        "Pwani University",
        "University of Eastern Africa, Baraton",
        "Kiriri Women's University of Science and Technology",
        "KCA University",
        "Zetech University",
        "Multimedia University of Kenya",
        "Scott Christian University",
        "Great Lakes University of Kisumu",
        "Kenya Highlands Evangelical University",
        "Presbyterian University of East Africa",
        "African Nazarene University",
        "Adventist University of Africa",
        "St. Paul's University",
        "Riara University",
        "Pan Africa Christian University",
        "Management University of Africa",
        "International Leadership University",
        "Africa International University",
        "Kirinyaga University",
        "Karatina University",
        # Add more university names as needed
    ]

    colleges_list = [
        "Kenya Medical Training College",
        "Technical University of Mombasa",
        "Eldoret Polytechnic",
        "Kenya Institute of Management",
        "Kabete National Polytechnic",
        "Kisumu National Polytechnic",
        "Rift Valley Institute of Science and Technology",
        "Meru National Polytechnic",
        "Kenya Institute of Mass Communication",
        "Kiambu Institute of Science and Technology",
        "Machakos Institute of Technology",
        "Thika Technical Training Institute",
        "Kisii National Polytechnic",
        "Mombasa Technical Training Institute",
        "Kakamega National Polytechnic",
        "Nairobi Technical Training Institute",
        "Karen Technical Training Institute",
        "Kaimosi Friends University College",
        "Kenya Water Institute",
        "Kenya Utalii College",
        "Kenya Institute of Highways and Building Technology",
        "Co-operative University of Kenya",
        "Murang'a University College",
        "Kisumu Polytechnic",
        "Nairobi Institute of Business Studies",
        "Eldoret Technical Training Institute",
        "East Africa School of Aviation",
        "Railway Training Institute",
        "Kenya Forestry College",
        "Kenya Institute of Surveying and Mapping",
        "Machakos University",
        "St. Joseph's Technical Institute",
        "Kenya Utalii College",
        "Mwangaza College",
        "Kenya School of Government",
        "Eldoret Aviation Training Institute",
        "Baraton Teachers' Training College",
        "Kisii College of Accountancy",
        "Kenya Utalii College",
        "Mathenge Technical Training Institute",
        "Nairobi Aviation College",
        "Rift Valley Technical Training Institute",
        "The Kenya Polytechnic University College",
        "Kenya Institute of Supplies Management",
        "Kitale Technical Training Institute",
        # Add more college names as needed
    ]

    # Insert 35 Universities
    for university_name in universities_list:
        Institution.objects.get_or_create(name=university_name)

    # Insert 50 Colleges
    for college_name in colleges_list:
        Institution.objects.get_or_create(name=college_name)

class Migration(migrations.Migration):

    dependencies = [
        ('mashinani', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_institutions),
    ]
