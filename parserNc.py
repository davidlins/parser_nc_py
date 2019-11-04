#!/usr/bin/env python
import io
import csv
import os
import tika
tika.initVM()
from tika import parser
from re import sub


def handleValue(key, buf,nrValues):
    if not  key in nrValues:
        line = buf.readline()
        line = buf.readline()
        nrValues[key] = getMoney(line)

def getMoney(line):
    s = sub(r',','.',sub(r'[^0-9|,]', '',line.split("|")[0]))
    value  = 0.0
    if s: 
        value  = float(s)
        if "D" in line or not "|" in line:
            value *= -1
    return value

def handleFile(fileName,nrList):
    lastNrNota = ""
    nrValues = {}

    parsed = parser.from_file(fileName)
    buf = io.StringIO(parsed["content"])
    line = buf.readline()
    while(line):
        if "Nr. nota Folha Data pregão" in line:
            line = buf.readline()
            line = buf.readline()
            nrNotaLineList = line.split(" ")
            nrNota = nrNotaLineList[0]
            if nrNota != lastNrNota:
                lastNrNota = nrNota
                nrValues = dict({NR_NOTA : nrNota , DATA :  sub(r'[\n]', '',nrNotaLineList[2])})
                nrList.append(nrValues)
        elif "Valor dos negócios" in line:
            handleValue(VALOR_NEGOCIO, buf,nrValues)
        elif "Taxa operacional" in line:
            handleValue(TX_OPERACIONAL, buf,nrValues)
        elif "ISS" in line:
            handleValue(ISS, buf,nrValues)
        elif "Taxa registro BMF" in line:
            handleValue(TX_REG_BMF, buf,nrValues)
        elif "Taxa BMF (emol+f.gar)" in line:
            handleValue(TX_BMF, buf,nrValues)
        elif "IRRF Day Trade(Projeção)" in line:
            handleValue(IRRF, buf,nrValues)
        elif "Total líquido da nota" in line:
            handleValue(TOTAL_LIQ_NOTA, buf,nrValues)

        line = buf.readline()

def writeCSV(nrList,fileName):
    with open(fileName, 'w') as csvfile:
        fieldnames = nrList[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(nrList)



NR_NOTA        = "Nr Nota"
DATA           = "Data Pregão"
VALOR_NEGOCIO  = "Valor dos Negocios"
TX_OPERACIONAL = "Taxa Operacional"
ISS            = "ISS"
TX_REG_BMF     = "Taxa Registro BMF"
TX_BMF         = "Taxa BMF (emol+f.gar)"
IRRF           = "IRRF Day Trade(Projeção)"
TOTAL_LIQ_NOTA = "Total líquido da nota"

nrList     = []
dirName    = "/home/davidlins/Development/code/private/parser_nc_py/notas/"
for root, dirs, files in os.walk(dirName):
    for filename in files:
        handleFile(dirName+filename,nrList)

writeCSV(nrList,"ajustes.csv")

#for nrValues in nrList:
#    print(nrValues)
