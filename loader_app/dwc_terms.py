__author__ = '@jotegui'

dwc_terms = {
    'Record': {
        'type': {'url': 'http://purl.org/dc/terms/type', 'def': 'Nature of the resource (StillImage, Sound, Event..)'},    
        'modified': {'url': 'http://purl.org/dc/terms/modified', 'def': 'Last modified'},
        'language': {'url': 'http://purl.org/dc/terms/language', 'def': ''},
        'license': {'url': 'http://purl.org/dc/terms/license', 'def': ''},
        'rightsHolder': {'url': 'http://purl.org/dc/terms/rightsHolder', 'def': ''},
        'accessRights': {'url': 'http://purl.org/dc/terms/accessRights', 'def': 'Who can access the resource'},
        'bibliographicCitation': {'url': 'http://purl.org/dc/terms/bibliographicCitation', 'def': ''},
        'references': {'url': 'http://purl.org/dc/terms/references', 'def': 'Reference to a related resource'},
        'institutionID': {'url': 'http://rs.tdwg.org/dwc/terms/institutionID', 'def': 'Institution identifier'},
        'collectionID': {'url': 'http://rs.tdwg.org/dwc/terms/collectionID', 'def': 'Collection identifier'},
        'datasetID': {'url': 'http://rs.tdwg.org/dwc/terms/datasetID', 'def': 'Dataset identifier'},
        'institutionCode': {'url': 'http://rs.tdwg.org/dwc/terms/institutionCode', 'def': 'Name or acronym of the institution having custory of the resource'},
        'collectionCode': {'url': 'http://rs.tdwg.org/dwc/terms/collectionCode', 'def': 'Name or acronym of the collection'},
        'datasetName': {'url': 'http://rs.tdwg.org/dwc/terms/datasetName', 'def': ''},
        'ownerInstitutionCode': {'url': 'http://rs.tdwg.org/dwc/terms/ownerInstitutionCode', 'def': 'Name or acronym of the institution owner of the resource'},
        'basisOfRecord': {'url': 'http://rs.tdwg.org/dwc/terms/basisOfRecord', 'def': 'Nature of the record: Human Observation, Preserved Specimen...'},
        'informationWithheld': {'url': 'http://rs.tdwg.org/dwc/terms/informationWithheld', 'def': 'Declaration of existing, but hidden, information'},
        'dataGeneralizations': {'url': 'http://rs.tdwg.org/dwc/terms/dataGeneralizations', 'def': 'Actions taken to blur information'},
        'dynamicProperties': {'url': 'http://rs.tdwg.org/dwc/terms/dynamicProperties', 'def': 'Additional measurements or facts'}
    },
    'Occurrence': {
        'occurrenceID': {'url': 'http://rs.tdwg.org/dwc/terms/occurrenceID', 'def': 'Identifier for the occurrence'},
        'catalogNumber': {'url': 'http://rs.tdwg.org/dwc/terms/catalogNumber', 'def': 'Identifier for the record within the collection'},
        'recordNumber': {'url': 'http://rs.tdwg.org/dwc/terms/recordNumber', 'def': ''},
        'recordedBy': {'url': 'http://rs.tdwg.org/dwc/terms/recordedBy', 'def': ''},
#        'individualID': {'url': 'http://rs.tdwg.org/dwc/terms/individualID', 'def': ''},  # Missing in last version of DWC
        'individualCount': {'url': 'http://rs.tdwg.org/dwc/terms/individualCount', 'def': 'Number of individuals'},
        'sex': {'url': 'http://rs.tdwg.org/dwc/terms/sex', 'def': 'Sex of the biological individuals'},
        'lifeStage': {'url': 'http://rs.tdwg.org/dwc/terms/lifeStage', 'def': 'Age class or life stage of the individuals'},
        'reproductiveCondition': {'url': 'http://rs.tdwg.org/dwc/terms/reproductiveCondition', 'def': ''},
        'behavior': {'url': 'http://rs.tdwg.org/dwc/terms/behavior', 'def': 'Description of the behavior shown by the organism at the time of the observation'},
        'establishmentMeans': {'url': 'http://rs.tdwg.org/dwc/terms/establishmentMeans', 'def': 'Process by which the individual became established (native, introduced, managed...)'},
#        'occurrenceStatus': {'url': 'http://rs.tdwg.org/dwc/terms/occurrenceStatus', 'def': 'Presence or absence of the taxon at the location'},
#        'preparations': {'url': 'http://rs.tdwg.org/dwc/terms/preparations', 'def': ''},
#        'disposition': {'url': 'http://rs.tdwg.org/dwc/terms/disposition', 'def': ''},
        'associatedMedia': {'url': 'http://rs.tdwg.org/dwc/terms/associatedMedia', 'def': 'List of identifiers of media associated with the observation'},
        'associatedReferences': {'url': 'http://rs.tdwg.org/dwc/terms/associatedReferences', 'def': 'List of identifiers of references associated with the observation'},
        'associatedSequences': {'url': 'http://rs.tdwg.org/dwc/terms/associatedSequences', 'def': 'List of identifiers of sequences associated with the observation'},
        'associatedTaxa': {'url': 'http://rs.tdwg.org/dwc/terms/associatedTaxa', 'def': 'List of identifiers of other taxa associated with the observation'},
        'otherCatalogNumbers': {'url': 'http://rs.tdwg.org/dwc/terms/otherCatalogNumbers', 'def': 'List of previous or alternative identifiers'},
        'occurrenceRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/occurrenceRemarks', 'def': 'Comments about the occurrence'}
    },
    'Organism': {
        'organismID': {'url': 'http://rs.tdwg.org/dwc/terms/organismID', 'def': 'Identifier for the organism instance'},
        'organismName': {'url': 'http://rs.tdwg.org/dwc/terms/organismName', 'def': 'Textual name assigned to the organism instance'},
        'organismScope': {'url': 'http://rs.tdwg.org/dwc/terms/organismScope', 'def': 'Kind of organism instance (pack, colony...)'},
        'associatedOccurrences': {'url': 'http://rs.tdwg.org/dwc/terms/associatedOccurrences', 'def': 'List of identifiers of occurrences associated with the organism'},
        'associatedOrganisms': {'url': 'http://rs.tdwg.org/dwc/terms/associatedOrganisms', 'def': 'List of identifiers of other organisms associated with the organism'},
        'previousIdentifications': {'url': 'http://rs.tdwg.org/dwc/terms/previousIdentifications', 'def': 'List of previous assignments of names to the organism'},
        'organismRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/organismRemarks', 'def': 'Comments about the organism'}
    },
#    'MaterialSample': {
#        'materialSampleId': {'url': 'http://rs.tdwg.org/dwc/terms/materialSampleID', 'def': ''}
#    },
    'Event': {
        'eventID': {'url': 'http://rs.tdwg.org/dwc/terms/eventID', 'def': 'Identifier for the information related to the event'},    
        'fieldNumber': {'url': 'http://rs.tdwg.org/dwc/terms/fieldNumber', 'def': 'Identifier for the event in the field'},
#        'eventDate': {'url': 'http://rs.tdwg.org/dwc/terms/eventDate', 'def': 'Date of the observation'},
        'eventTime': {'url': 'http://rs.tdwg.org/dwc/terms/eventTime', 'def': 'Time of the observation, if separated from Date'},
        'startDayOfYear': {'url': 'http://rs.tdwg.org/dwc/terms/startDayOfYear', 'def': 'Earliest 365-based day of the observation (e.g. 1=Jan 1st, 366=Dec 31st)'},
        'endDayOfYear': {'url': 'http://rs.tdwg.org/dwc/terms/endDayOfYear', 'def': 'Latest 365-based day of the observation (e.g. 1=Jan 1st, 366=Dec 31st)'},
        'year': {'url': 'http://rs.tdwg.org/dwc/terms/year', 'def': 'Four-digit year of the observation'},
        'month': {'url': 'http://rs.tdwg.org/dwc/terms/month', 'def': 'Ordinal month of the observation'},
        'day': {'url': 'http://rs.tdwg.org/dwc/terms/day', 'def': 'Integer day of the observation'},
        'verbatimEventDate': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimEventDate', 'def': 'The original, verbatim representation of the date'},
        'habitat': {'url': 'http://rs.tdwg.org/dwc/terms/habitat', 'def': 'Description of the Habitat'},
        'samplingProtocol': {'url': 'http://rs.tdwg.org/dwc/terms/samplingProtocol', 'def': 'Name or reference to the method used for sampling'},
        'samplingEffort': {'url': 'http://rs.tdwg.org/dwc/terms/samplingEffort', 'def': 'Amount of effort expended for sampling'},
        'fieldNotes': {'url': 'http://rs.tdwg.org/dwc/terms/fieldNotes', 'def': 'A reference to any notes taken in the field, or the content of those notes'},
        'eventRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/eventRemarks', 'def': 'Comments about the event'}
    },
    'Location': {
        'locationID': {'url': 'http://rs.tdwg.org/dwc/terms/locationID', 'def': 'Identifier for the location'},
        'higherGeographyID': {'url': 'http://rs.tdwg.org/dwc/terms/higherGeographyID', 'def': 'Identifier for the geographic region of the event'},
        'higherGeography': {'url': 'http://rs.tdwg.org/dwc/terms/higherGeography', 'def': 'Hyerarchical descending list of geographic terms for the event circunscription'},
        'continent': {'url': 'http://rs.tdwg.org/dwc/terms/continent', 'def': ''},
        'waterBody': {'url': 'http://rs.tdwg.org/dwc/terms/waterBody', 'def': ''},
        'islandGroup': {'url': 'http://rs.tdwg.org/dwc/terms/islandGroup', 'def': ''},
        'island': {'url': 'http://rs.tdwg.org/dwc/terms/island', 'def': ''},
        'country': {'url': 'http://rs.tdwg.org/dwc/terms/country', 'def': ''},
        'countryCode': {'url': 'http://rs.tdwg.org/dwc/terms/countryCode', 'def': 'Standard code for the country of the observation'},
        'stateProvince': {'url': 'http://rs.tdwg.org/dwc/terms/stateProvince', 'def': ''},
        'county': {'url': 'http://rs.tdwg.org/dwc/terms/county', 'def': ''},
        'municipality': {'url': 'http://rs.tdwg.org/dwc/terms/municipality', 'def': ''},
        'locality': {'url': 'http://rs.tdwg.org/dwc/terms/locality', 'def': 'Specific description of the event location'},
        'verbatimLocality': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimLocality', 'def': 'The original, verbatim representation of the location'},
        'verbatimElevation': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimElevation', 'def': 'The original, verbatim representation of the elevation values'},
        'minimumElevationInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/minimumElevationInMeters', 'def': ''},
        'maximumElevationInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/maximumElevationInMeters', 'def': ''},
        'verbatimDepth': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimDepth', 'def': 'The original, verbatim representation of the depth values'},
        'minimumDepthInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/minimumDepthInMeters', 'def': ''},
        'maximumDepthInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/maximumDepthInMeters', 'def': ''},
        'minimumDistanceAboveSurfaceInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/minimumDistanceAboveSurfaceInMeters', 'def': ''},
        'maximumDistanceAboveSurfaceInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/maximumDistanceAboveSurfaceInMeters', 'def': ''},
        'locationAccordingTo': {'url': 'http://rs.tdwg.org/dwc/terms/locationAccordingTo', 'def': 'Information about the source of the location'},
        'locationRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/locationRemarks', 'def': 'Comments about the location'},
        'verbatimCoordinates': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimCoordinates', 'def': 'The original, verbatim representation of the coordinates'},
        'verbatimLatitude': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimLatitude', 'def': 'The original, verbatim representation of the latitude'},
        'verbatimLongitude': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimLongitude', 'def': 'The original, verbatim representation of the longitude'},
        'verbatimCoordinateSystem': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimCoordinateSystem', 'def': 'The original, verbatim representation of the coordinate system (decimal degrees, UTM...)'},
        'verbatimSRS': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimSRS', 'def': 'The original, verbatim representation of the Spatial Reference System (WGS84, NAD27...)'},
#        'decimalLatitude': {'url': 'http://rs.tdwg.org/dwc/terms/decimalLatitude', 'def': ''},
#        'decimalLongitude': {'url': 'http://rs.tdwg.org/dwc/terms/decimalLongitude', 'def': ''},
        'geodeticDatum': {'url': 'http://rs.tdwg.org/dwc/terms/geodeticDatum', 'def': ''},
#        'coordinateUncertaintyInMeters': {'url': 'http://rs.tdwg.org/dwc/terms/coordinateUncertaintyInMeters', 'def': ''},
        'coordinatePrecision': {'url': 'http://rs.tdwg.org/dwc/terms/coordinatePrecision', 'def': ''},
        'pointRadiusSpatialFit': {'url': 'http://rs.tdwg.org/dwc/terms/pointRadiusSpatialFit', 'def': 'Ratio of the point-radius area to the true spatial representation of the location'},
        'footprintWKT': {'url': 'http://rs.tdwg.org/dwc/terms/footprintWKT', 'def': 'Well-Known Text representation of the shape of the location'},
        'footprintSRS': {'url': 'http://rs.tdwg.org/dwc/terms/footprintSRS', 'def': 'Well-Known Text representation of the Spatial Reference System'},
        'footprintSpatialFit': {'url': 'http://rs.tdwg.org/dwc/terms/footprintSpatialFit', 'def': 'Ratio of the footprintWKT area to the true spatial representation of the location'},
        'georeferencedBy': {'url': 'http://rs.tdwg.org/dwc/terms/georeferencedBy', 'def': 'Who georeferenced the location'},
        'georeferencedDate': {'url': 'http://rs.tdwg.org/dwc/terms/georeferencedDate', 'def': 'When was the location georeferenced'},
        'georeferenceProtocol': {'url': 'http://rs.tdwg.org/dwc/terms/georeferenceProtocol', 'def': 'What method/s was/were used to georeference the location'},
        'georeferenceSources': {'url': 'http://rs.tdwg.org/dwc/terms/georeferenceSources', 'def': 'List of resources (maps, gazetteers...) used to georeference the location'},
        'georeferenceVerificationStatus': {'url': 'http://rs.tdwg.org/dwc/terms/georeferenceVerificationStatus', 'def': 'Categorical indicator of the verification status of the georeference'},
        'georeferenceRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/georeferenceRemarks', 'def': 'Comments about the georeferencing'}
    },
#    'GeologicalContext': {
#        'geologicalContextID': {'url': 'http://rs.tdwg.org/dwc/terms/geologicalContextID', 'def': ''},    
#        'earliestEonOrLowestEonothem': {'url': 'http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem', 'def': ''},
#        'latestEonOrHighestEonothem': {'url': 'http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem', 'def': ''},
#        'earliestEraOrLowestErathem': {'url': 'http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem', 'def': ''},
#        'latestEraOrHighestErathem': {'url': 'http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem', 'def': ''},
#        'earliestPeriodOrLowestSystem': {'url': 'http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem', 'def': ''},
#        'latestPeriodOrHighestSystem': {'url': 'http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem', 'def': ''},
#        'earliestEpochOrLowestSeries': {'url': 'http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries', 'def': ''},
#        'latestEpochOrHighestSeries': {'url': 'http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries', 'def': ''},
#        'earliestAgeOrLowestStage': {'url': 'http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage', 'def': ''},
#        'latestAgeOrHighestStage': {'url': 'http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage', 'def': ''},
#        'lowestBiostratigraphicZone': {'url': 'http://rs.tdwg.org/dwc/terms/lowestBiostratigraphicZone', 'def': ''},
#        'highestBiostratigraphicZone': {'url': 'http://rs.tdwg.org/dwc/terms/highestBiostratigraphicZone', 'def': ''},
#        'lithostratigraphicTerms': {'url': 'http://rs.tdwg.org/dwc/terms/lithostratigraphicTerms', 'def': ''},
#        'group': {'url': 'http://rs.tdwg.org/dwc/terms/group', 'def': ''},
#        'formation': {'url': 'http://rs.tdwg.org/dwc/terms/formation', 'def': ''},
#        'member': {'url': 'http://rs.tdwg.org/dwc/terms/member', 'def': ''},
#        'bed': {'url': 'http://rs.tdwg.org/dwc/terms/bed', 'def': ''}
#    },
    'Identification': {
        'identificationID': {'url': 'http://rs.tdwg.org/dwc/terms/identificationID', 'def': 'Identifier for the Identification'},
        'identificationQualifier': {'url': 'http://rs.tdwg.org/dwc/terms/identificationQualifier', 'def': 'Expression of doubts about the identification'},
        'typeStatus': {'url': 'http://rs.tdwg.org/dwc/terms/typeStatus', 'def': 'Nomenclatural type applied to the subjct'},
        'identifiedBy': {'url': 'http://rs.tdwg.org/dwc/terms/identifiedBy', 'def': 'Who identified the organism'},
        'dateIdentified': {'url': 'http://rs.tdwg.org/dwc/terms/dateIdentified', 'def': 'When was the organism identified'},
        'identificationReferences': {'url': 'http://rs.tdwg.org/dwc/terms/identificationReferences', 'def': 'References used in the identification'},
        'identificationVerificationStatus': {'url': 'http://rs.tdwg.org/dwc/terms/identificationVerificationStatus', 'def': 'Categorical indicator of the verification status of the identification'},
        'identificationRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/identificationRemarks', 'def': 'Comments about the identification'}

    },
    'Taxon': {
        'taxonID': {'url': 'http://rs.tdwg.org/dwc/terms/taxonID', 'def': 'Identifier for the Taxon'},
        'scientificNameID': {'url': 'http://rs.tdwg.org/dwc/terms/scientificNameID', 'def': 'Identifier for the nomenclatural details'},
        'acceptedNameUsageID': {'url': 'http://rs.tdwg.org/dwc/terms/acceptedNameUsageID', 'def': 'Identifier for the name usage'},
        'parentNameUsageID': {'url': 'http://rs.tdwg.org/dwc/terms/parentNameUsageID', 'def': 'Identifier for the name usage of the direct higher-rank parent taxon'},
        'originalNameUsageID': {'url': 'http://rs.tdwg.org/dwc/terms/originalNameUsageID', 'def': 'Identifier for the original name usage'},
        'nameAccordingToID': {'url': 'http://rs.tdwg.org/dwc/terms/nameAccordingToID', 'def': 'Identifier for nameAccordingTo'},
        'namePublishedInID': {'url': 'http://rs.tdwg.org/dwc/terms/namePublishedInID', 'def': 'Identifier for namePublishedIn'},
        'taxonConceptID': {'url': 'http://rs.tdwg.org/dwc/terms/taxonConceptID', 'def': 'Identifier for the taxonomic concept'},
#        'scientificName': {'url': 'http://rs.tdwg.org/dwc/terms/scientificName', 'def': ''},
        'acceptedNameUsage': {'url': 'http://rs.tdwg.org/dwc/terms/acceptedNameUsage', 'def': 'Full name of the currently valid taxon'},
        'parentNameUsage': {'url': 'http://rs.tdwg.org/dwc/terms/parentNameUsage', 'def': 'Full name of the firect higher-rank parent taxon'},
        'originalNameUsage': {'url': 'http://rs.tdwg.org/dwc/terms/originalNameUsage', 'def': 'Original full name of the taxon'},
        'nameAccordingTo': {'url': 'http://rs.tdwg.org/dwc/terms/nameAccordingTo', 'def': 'Reference to the source of the taxon'},
        'namePublishedIn': {'url': 'http://rs.tdwg.org/dwc/terms/namePublishedIn', 'def': 'Reference to the publication of the taxon'},
        'namePublishedInYear': {'url': 'http://rs.tdwg.org/dwc/terms/namePublishedInYear', 'def': 'Year of publication of the taxon'},
        'higherClassification': {'url': 'http://rs.tdwg.org/dwc/terms/higherClassification', 'def': 'Concatenated list of higher-rank taxa'},
        'kingdom': {'url': 'http://rs.tdwg.org/dwc/terms/kingdom', 'def': ''},
        'phylum': {'url': 'http://rs.tdwg.org/dwc/terms/phylum', 'def': ''},
        'class': {'url': 'http://rs.tdwg.org/dwc/terms/class', 'def': ''},
        'order': {'url': 'http://rs.tdwg.org/dwc/terms/order', 'def': ''},
        'family': {'url': 'http://rs.tdwg.org/dwc/terms/family', 'def': ''},
        'genus': {'url': 'http://rs.tdwg.org/dwc/terms/genus', 'def': ''},
        'subgenus': {'url': 'http://rs.tdwg.org/dwc/terms/subgenus', 'def': ''},
        'specificEpithet': {'url': 'http://rs.tdwg.org/dwc/terms/specificEpithet', 'def': ''},
        'infraspecificEpithet': {'url': 'http://rs.tdwg.org/dwc/terms/infraspecificEpithet', 'def': ''},
        'taxonRank': {'url': 'http://rs.tdwg.org/dwc/terms/taxonRank', 'def': 'Rank of the taxon (species, subspecies, genus...)'},
        'verbatimTaxonRank': {'url': 'http://rs.tdwg.org/dwc/terms/verbatimTaxonRank', 'def': 'The original, verbatim representation of the taxon rank'},
        'scientificNameAuthorship': {'url': 'http://rs.tdwg.org/dwc/terms/scientificNameAuthorship', 'def': 'Authorship information for the scientific Name'},
        'vernacularName': {'url': 'http://rs.tdwg.org/dwc/terms/vernacularName', 'def': ''},
        'nomenclaturalCode': {'url': 'http://rs.tdwg.org/dwc/terms/nomenclaturalCode', 'def': 'Code used for constructing the scientific name (ICZN, ICBN, BC...'},
        'taxonomicStatus': {'url': 'http://rs.tdwg.org/dwc/terms/taxonomicStatus', 'def': 'Status of the use of the scientificName (invalid, misapplied, accepted...)'},
        'nomenclaturalStatus': {'url': 'http://rs.tdwg.org/dwc/terms/nomenclaturalStatus', 'def': 'Status of the conformance of nomenclature (nom. ambig., nom. illeg., ...)'},
        'taxonRemarks': {'url': 'http://rs.tdwg.org/dwc/terms/taxonRemarks', 'def': 'Commments about the taxon or name'}
    }
}
