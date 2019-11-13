#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import glob
from pathlib import Path
from lxml import etree
import pandas as pd
from pprint import pprint

def getTree(xmlPath):
    tree = etree.parse(xmlPath)
    root = tree.getroot()
    return root

#parse XML node tag to easily readable text
def parseTag(tag):
    tagElements = tag.strip().split('}')
    return tagElements[1]

#test if a string can be converted to integer
def isInt(x):
    try:
        a = int(x)
    except ValueError:
        return False
    else:
        return True

#get clinical information from a TCGA clinical xml file
def getPatientInfo(root):
    clinicalDictionary = dict()
    for child in root:
        if parseTag(child.tag) == 'patient':
            for grandchild in child:
                if len(list(grandchild)) == 0:
                    value = str(grandchild.text)
                    clinicalDictionary[parseTag(grandchild.tag)] = value
    return clinicalDictionary

def getAdminInfo(root):
    adminDictionary = dict()
    for child in root:
        if parseTag(child.tag) == 'admin':
            for grandchild in child:
                if len(list(grandchild)) == 0:
                    value = str(grandchild.text)
                    adminDictionary[parseTag(grandchild.tag)] = value
    return adminDictionary

def getMsiInfo(root):
    msiDictionary = dict()
    msiChildList = root.findall('.//bio:msi_mono_di_nucleotide_assay_status', root.nsmap)
    if len(msiChildList) != 0:
        for msiChild in msiChildList:
            msiParent = msiChild.getparent()
            for child in msiParent:
                if len(list(child)) == 0:
                    value = str(child.text)
                    msiDictionary[parseTag(child.tag)] = value
    return msiDictionary

def parseTCGAXML(xmlPath):
    root = getTree(xmlPath)
    clinicalDictionary = getPatientInfo(root)
    adminDictionary = getAdminInfo(root)
    msiDictionary = getMsiInfo(root)

    clinicalList = list()

    clinicalList.append(clinicalDictionary["bcr_patient_barcode"])

    clinicalList.append(adminDictionary["project_code"])

    clinicalList.append(adminDictionary["disease_code"])

    clinicalList.append(msiDictionary.get("bcr_aliquot_barcode", "NA"))

    clinicalList.append(msiDictionary.get("msi_mono_di_nucleotide_assay_status", "NA"))

    return clinicalList

def main():
    manifest = sys.argv[1]
    wdir = Path("/lustre/work/user/sunhb/TCGA/TCGA_Clinical/Biospecimen_Supplement/")
    res = []
    df = pd.read_csv(manifest, sep="\t")
    labelList = ["bcr_patient_barcode", "project_code", "disease_code", "bcr_aliquot_barcode", "msi_mono_di_nucleotide_assay_status"]
    for ix, line in df.iterrows():
        fpath = wdir.joinpath(line.id, line.filename)
        clinicalList = parseTCGAXML(str(fpath))
        res.append(clinicalList)
    res = pd.DataFrame(res)
    res.columns = labelList
    res.to_csv("TCGA_MSI.txt", sep="\t", index=False)

if __name__ == "__main__":
    main()