#!/usr/bin/env python
import os, 	sys
##
# this python file is a script that imports all readable TEI data from the disk.
##
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "decommentariis.settings")
os.environ.setdefault("CTS_DATA_PATH", "/Users/smcphee/Development/sources/commentarius/data/canonical/CTS_XML_TEI/perseus/")
from decommentariis.models import TEIEntry, TEISection
from decommentariis.xml_file import TEIDataSource
# print(TEIEntry.objects.all())
path = os.environ.get("CTS_DATA_PATH")

## functions for the script.
def open_source(path, filename):
	return open(path + filename, 'r')

def save_sections(section_numbers, entry):
	if section_numbers and (len(section_numbers)):
		i = 10
		for section in section_numbers:
			teiSection = None
			urn = '{0}:{1}'.format(entry.cts_urn, section)

			if TEISection.objects.filter(cts_urn = urn).exists():
				teiSection = TEISection.objects.get(cts_urn = urn)
				print('\t\tExisting Section {0}'.format(urn))
			else:
				teiSection = TEISection()
				teiSection.cts_urn = urn
				print('\t\tNew Section {0}'.format(urn))

			teiSection.entry = entry
			teiSection.section_ref = section
			teiSection.cts_sequence = i
			teiSection.save()
			i += 10
	else :
		# no section numbers, delete entry, it's pointless.
		print('DELETE {0}\n\t{1}'.format(entry.cts_urn, entry.bibliographic_entry))
		entry.delete()

def savedb(urn):
	entry = None
	section_numbers = None
	if TEIEntry.objects.filter(cts_urn = urn).exists():
		entry = TEIEntry.objects.get(cts_urn=urn)
		section_numbers = entry.loadURN()
		print('UPDATE {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
	else:
		entry = TEIEntry(urn)
		section_numbers = entry.loadURN()
		print('NEW {0}\n\t{1}'.format(urn, entry.bibliographic_entry))
	
	entry.save()
	save_sections(section_numbers, entry)

def readdatafromline(line, prefix):
	line = line.rstrip().rstrip('.xml')
	pathcomponents = line.split('/')
	if len(pathcomponents):
		urn = prefix + pathcomponents[len(pathcomponents)-1]
		try:
			savedb(urn)
		except Exception as ex:
			print("\n!!! {0} has unparseable data: {1}".format(urn, ex))

## the script
# first, the latins
latinFile = open_source(path, "latinLit.txt")
for line in latinFile.readlines():
	readdatafromline(line, 'urn:cts:latinLit:')

# then, the greeks
greekFile = open_source(path, "greekLit.txt")
for line in greekFile.readlines():
	readdatafromline(line, 'urn:cts:greekLit:')
