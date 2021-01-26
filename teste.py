marcas

for m in marcas:
    Brand.objects.create(name=m['name'])

for m in models:
    b = Brand.objects.get(id=m['brand'])
    Model.objects.create(brand=b, name=m['name'])


for c in cars:
    b = Brand.objects.get(id=c['brand'])
    m = Model.objects.get(id=c['model'])

    Car.objects.create(
        license_plate=c['license_plate'],
        brand=b,
        model=m,
        year=c['year'],
        version=c['version'],
        transmission=c['transmission'],
        mileage=c['mileage'],
        car_type=c['car_type'],
        color=c['color'],
        min_sale_value=c['sale_value'] 
    )

marcas = [{'name': 'Fiat'},
 {'name': 'GM - Chevrolet'},
 {'name': 'Volkswagen'},
 {'name': 'Renault'},
 {'name': 'Ford'},
 {'name': 'Hyundai'},
 {'name': 'Nissan'},
 {'name': 'Toyota'},
 {'name': 'Jeep'}]

models = [{'name': 'Uno', 'brand': 1},
 {'name': 'Toro', 'brand': 1},
 {'name': 'Siena', 'brand': 1},
 {'name': 'Onix', 'brand': 2},
 {'name': 'S-10', 'brand': 2},
 {'name': 'Classic', 'brand': 2},
 {'name': 'Gol', 'brand': 3},
 {'name': 'Amarok', 'brand': 3},
 {'name': 'Golf', 'brand': 3},
 {'name': 'Ka', 'brand': 5},
 {'name': 'Ecosport', 'brand': 5},
 {'name': 'Fiesta', 'brand': 5}]

cars = [{'license_plate': 'MEL-5695',
  'brand': 1,
  'model': 1,
  'year': 2016,
  'version': 'EVO ATTRACTIVE 8V FLEX 4P MANUAL',
  'transmission': 'M',
  'mileage': 105000,
  'car_type': 'hatch',
  'color': 'black',
  'sale_value': 28900},
 {'license_plate': 'PIA2A19',
  'brand': 1,
  'model': 2,
  'year': 2019,
  'version': '1.8 16V EVO FLEX ENDURANCE AT6',
  'transmission': 'AT',
  'mileage': 105000,
  'car_type': 'pick-up',
  'color': 'red',
  'sale_value': 89890},
 {'license_plate': 'NHE1E15',
  'brand': 1,
  'model': 3,
  'year': 2015,
  'version': '1.0 MPI EL 8V FLEX 4P MANUAL',
  'transmission': 'M',
  'mileage': 68000,
  'car_type': 'sedan',
  'color': 'silver',
  'sale_value': 35990},
 {'license_plate': 'UAE2D71',
  'brand': 2,
  'model': 4,
  'year': 2019,
  'version': '1.4 MPFI LTZ 8V FLEX 4P MANUAL',
  'transmission': 'M',
  'mileage': 30622,
  'car_type': 'hatch',
  'color': 'red',
  'sale_value': 60990},
 {'license_plate': 'PIA1T87',
  'brand': 2,
  'model': 5,
  'year': 2018,
  'version': '2.8 LS 4X4 CD 16V TURBO DIESEL 4P MANUAL',
  'transmission': 'M',
  'mileage': 68362,
  'car_type': 'pick-up',
  'color': 'silver',
  'sale_value': 112850},
 {'license_plate': 'NIA1W75',
  'brand': 2,
  'model': 6,
  'year': 2015,
  'version': '1.0 MPFI LS 8V FLEX 4P MANUAL',
  'transmission': 'M',
  'mileage': 76000,
  'car_type': 'sedan',
  'color': 'white',
  'sale_value': 29990}]