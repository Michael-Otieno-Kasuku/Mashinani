from django.core.management.base import BaseCommand
from django_extensions.management.commands.graph_models import Command as GraphModelsCommand

class Command(BaseCommand):
    help = 'Generate an Entity-Relationship (ER) diagram for the Bursary project and save it as a PNG file.'

    def handle(self, *args, **options):
        # Specify the project and app names
        project_name = 'bursary'
        app_name = 'mashinani'

        # Specify the output file path with the PNG extension
        output_file = 'database_design.png'

        # Specify the models you want to include in the ER diagram
        models_to_include = [
            'mashinani.Bank',
            'mashinani.Institution',
            'mashinani.Account',
            'mashinani.Constituency',
            'mashinani.Voter',
            'mashinani.Student',
            'mashinani.FinancialYear',
            'mashinani.BursaryApplication',
        ]

        # Construct the arguments for graph_models command
        graph_models_args = ['--output', output_file, '--all-applications']
        graph_models_args.extend(models_to_include)

        try:
            # Run the graph_models command
            GraphModelsCommand().run_from_argv(['manage.py', 'graph_models'] + graph_models_args)

            # Print success message
            self.stdout.write(self.style.SUCCESS(f'Success: ER diagram saved as {output_file} for the Bursary project.'))
        except Exception as e:
            # Handle any exceptions during the execution
            error_message = f'Error: Unable to generate the ER diagram. {e}'
            self.stdout.write(self.style.ERROR(error_message))
