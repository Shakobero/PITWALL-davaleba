import pandas as pd
from django.core.management.base import BaseCommand
from car_selectors.models import Make, Model, CarType

class Command(BaseCommand):
    help = 'Import car data from Excel'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='The path to the Excel file containing car data.')

    def handle(self, *args, **kwargs):
       
        excel_file = kwargs['excel_file']
        
        
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            
            make, _ = Make.objects.get_or_create(name=row['Make'])
            
            
            model, _ = Model.objects.get_or_create(name=row['Model'], make=make)
            
            
            CarType.objects.get_or_create(name=row['Type'], model=model)

        self.stdout.write(self.style.SUCCESS('Successfully imported car data'))
