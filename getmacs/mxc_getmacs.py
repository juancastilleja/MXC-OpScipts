import json
import requests
import csv
import time

#Cambiar de acuerdo a cada SP
APIKey = ""
OrgMX = ""

#Parametros de la API de Meraki
headers = {'X-Cisco-Meraki-API-Key' : APIKey , 'Content-Type' : 'application/json'}
payload = {'timespan' : '7200'}

def __Main__(Org):
    #Genera Array Meraki
    url = 'https://dashboard.meraki.com/api/v0/organizations/' + OrgMX + '/inventory'
    #GET a Meraki
    r = requests.get(url, headers=headers)
    r.json()
    json_data = json.loads(r.text)
    array = len(json_data)
    ##FIN de creacion array Meraki Inventory
    def __MACWAN(MAC):
        split = MAC.split(":")
        ultimodigito = split[5]
        integer = int(ultimodigito, 16)
        sumaint = integer + 5
        hexa = hex(sumaint)
        hexstr = str(hexa)
        hexsplit = hexstr.split("x")
        ultimodigitohex = str(hexsplit[1])
        MACWAN = split[0] + ":" + split[1] + ":" + split[2] + ":" + split[3] + ":" + split[4] + ":" + ultimodigitohex
        return MACWAN

    def __AbreCSV():
        # Variables del CSV
        global writer
        global outputCsv
        global filename
        filename = "ReporteMAC_" + OrgMX + ".csv"
        outputCsv = open(filename, 'wb')
        fieldnames = ['NETWORK', 'MAC', 'MACWAN1', 'SERIAL']
        writer = csv.DictWriter(outputCsv, fieldnames=fieldnames)
        writer.writeheader();

    #Abre CSV para la Org
    __AbreCSV()
    #Busqueda principal
    for x in range(0, array):
        networkId = json_data[x]['networkId']
        mac = json_data[x]['mac']
        serial = json_data[x]['serial']
        #Network Name
        url2 = 'https://dashboard.meraki.com/api/v0/networks/' + networkId
        r2 = requests.get(url2, headers=headers)
        if r2.status_code == 200:
            r2.json()
            json_data2 = json.loads(r2.text)
            networkName = json_data2['name']
            networkName = networkName.encode('ascii', 'ignore')
        else:
            networkName = "Null"
        macwan1 = __MACWAN(mac)
        #macwan1 = macwan1.encode('utf-8', 'ignore').decode('utf-8')
        data = {'NETWORK': networkName, 'MAC': mac, 'MACWAN1': macwan1, 'SERIAL': serial}
        writer.writerow(data)
        time.sleep(0.1)
        x=x+1
    #Cierra CSV
    outputCsv.close()
#Inicia codigo
__Main__("MX")
