import math

from ..models import Consumption

def select() -> list :
    records = list(Consumption.objects.all().values())

    if len(records) == 0 :
        return None
    #end if

    id = 0
    records.sort(key = lambda record: record['year'])
    for record in records :
        id += 1
        record['id']              = id
        record['population']      = record['population'] ** 2
        record['consumptionRate'] = record['consumptionRate'] ** 2
    #end for

    return records
#end def

def insert(entity: dict) -> str :
    year            = entity['param0']
    population      = entity['param1']
    consumptionRate = entity['param2']

    if Consumption.objects.filter (
        year  = year
    ).exists() : return 'Data already exist'

    Consumption (
        year            = year, 
        population      = math.sqrt(int(population)),
        consumptionRate = math.sqrt(float(consumptionRate))
    ).save()
    
    return None
#end def

def bulkInsert(entities: list) -> str :
    for row in entities:
        year            = row['year']
        population      = row['population']
        consumptionRate = row['consumption']

        errMsg = __valueValidator(year, population, consumptionRate)
        if errMsg != None :
            return errMsg
        #end if
        
        if Consumption.objects.filter (
            year  = year
        ).exists() : continue

        Consumption (
            year            = year, 
            population      = math.sqrt(int(population)), 
            consumptionRate = math.sqrt(float(consumptionRate))
        ).save()        
    #end for

    return None
#end def

def update(entity: dict) -> str :
    year            = entity['param0']
    population      = entity['param1']
    consumptionRate = entity['param2']

    errMsg = __valueValidator(year, population, consumptionRate)
    if errMsg != None :
        return errMsg
    #end if

    record = Consumption.objects.get(year = year)
    if record == None :
        return 'Data not exist'
    #end if

    record.population      = math.sqrt(int(population))
    record.consumptionRate = math.sqrt(float(consumptionRate))

    record.save()
    return None
#end def    

def delete(entity: dict) -> str :
    lastRecord = select()[-1]
    lastYear   = lastRecord['year']

    year = int(entity['param0'])

    if year != lastYear :        
        return 'Can only delete last data'
    #end if
    
    record = Consumption.objects.get(year = year)
    if record == None :
        return 'Data not exist'
    #end if
    
    record.delete()
    return None
#end def

def __valueValidator(year, population, consumptionRate) -> str :
    intYear            = int(year)
    intPopulation      = int(population)
    intConsumptionRate = float(consumptionRate)

    if intYear < 1900 or intYear > 2200:
        return 'Invalid value for year'
    #end if
    
    if intPopulation < 0:
        return 'Invalid value for population'
    #end if
    
    if intConsumptionRate < 0.0:
        return 'Invalid value for consumptionRate'
    #end if
#end def