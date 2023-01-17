prefixes = """
PREFIX coy: <https://schema.coypu.org/global#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX time: <http://www.w3.org/2006/time#>
"""

prefixes_wb = """
PREFIX wb: <http://worldbank.org/>
PREFIX wbi: <http://worldbank.org/Indicator/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX geo: <https://www.geonames.org/ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

prefixes_wiki = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wds: <http://www.wikidata.org/entity/statement/>
PREFIX wdv: <http://www.wikidata.org/value/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
PREFIX bd: <http://www.bigdata.com/rdf#>
"""

query_0_desc = "Query0: Test query"
query_0 = prefixes + """
SELECT * WHERE{
    ?subject ?predicate ?object
}LIMIT 10
"""

query_test = prefixes + """
SELECT * WHERE{ 
    ?subject ?predicate ?object
}
LIMIT 10
"""

query_test_public_service = prefixes + prefixes_wiki+"""
SELECT * WHERE { 
SERVICE <https://query.wikidata.org/sparql> {
    ?subject rdf:type ?object
}LIMIT 10
}"""

query_test_private_service = prefixes +"""
SELECT * WHERE 
{ SERVICE <https://implisense.coypu.org/dataplatform/proxy/default/sparql> 
 {<https://schema.coypu.org/acled/8909747> a ?o
}
}"""

query_test_private_service_2 = prefixes +"""
SELECT Distinct * WHERE{ 
SERVICE <https://implisense.coypu.org/dataplatform/proxy/default/sparql> {
    <https://schema.coypu.org/acled/8909747> a ?o
}
SERVICE <http://coypu-fuseki.aksw.org/country/sparql> {
    <https://data.coypu.org/country/MAR> a ?o1
}
}"""

query_test_private_public = prefixes +"""
SELECT Distinct * WHERE{ 
SERVICE <https://implisense.coypu.org/dataplatform/proxy/default/sparql> {
    <https://schema.coypu.org/acled/8909747> a ?o
}

SERVICE <https://labs.tib.eu/sdm/worldbank_endpoint/sparql> {
     <http://worldbank.org/Country/DEU> a ?o1
}
}"""


 
query_1_desc = "Query1: fatalities per million population for a country in a year"
query_1 = prefixes + prefixes_wiki+ """
SELECT ?isoCode ?year ((sum(?fatalities_int)/avg(?population))*1000000 as ?fatalities_per_million) (count(?iri) as ?no_of_acled_events) 
WHERE {
    ?iri a coy:AcledEvent ;
    coy:hasIsoCode ?isoCode ;
    coy:hasTimestamp ?timestamp;
    coy:hasFatalities ?fatalities.
    bind(year(?timestamp) as ?year)
    bind (xsd:integer(?fatalities) as ?fatalities_int)
    
    SERVICE <https://query.wikidata.org/sparql>
    {
        ?country_wiki wdt:P31 wd:Q3624078; 
                      wdt:P298 ?country_code_wiki;
                     p:P1082 ?p.

        ?p pq:P585 ?time;
               ps:P1082 ?population.
        bind(year(?time) as ?year_w)
        SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".}  
    }
filter(?year_w=?year && ?country_code_wiki=?isoCode)  
}group by ?isoCode ?year
order by desc (?year) 
LIMIT 10
"""

query_2_desc = "Query 2: Germany WB indicators for year 2021"
query_2 = prefixes + """
select ?country ?iso_code ?year ?topic ?indicator ?indicator_label ?indicator_note ?value
where {
    ?country a wb:AnnualIndicatorEntry;
            wb:hasTopic ?topic;
            wb:hasIndicator ?indicator;
            wb:hasCountry ?country;
            owl:hasValue ?value;        
            time:year ?year.
    ?country rdfs:label ?country_name;
                     dc:identifier ?iso_code;
                     dbo:region ?region.
optional {?indicator rdfs:label ?indicator_label}
optional {?indicator skos:note  ?indicator_note }
         
filter(?year=2021 && ?country=<http://worldbank.org/Country/DEU>)
}
order by ?country ?iso_code ?year
limit 2000
"""

query_3_desc = "Query 3: Gdp per captita for countries in different years WB and Wikidata"
query_3 = prefixes + prefixes_wiki+ """
select ?country ?year ?value ?population (?value/?population as ?gdp_per_capita)
where {

    SERVICE <https://labs.tib.eu/sdm/worldbank_endpoint/sparql/> {
			?indicator a wb:AnnualIndicatorEntry;
                       wb:hasIndicator wbi:NY.GDP.MKTP.CD;
                       wb:hasCountry ?country;
                       owl:hasValue ?value;        
                       time:year ?year.
            ?country rdfs:label ?country_name;
                     dc:identifier ?country_code;
                     dbo:region ?region.
            filter(?year > 2018) 
    }

{
select ?country_code_wiki ?year_w ?population 
    where {SERVICE <https://query.wikidata.org/sparql>{
        ?country_wiki wdt:P31 wd:Q3624078; 
                      wdt:P298 ?country_code_wiki;
                     p:P1082 ?p.

        ?p pq:P585 ?time;
               ps:P1082 ?population.
        bind(year(?time) as ?year_w)
        filter(?year_w > 2018)
        SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".}
            }} 
}
filter(?year_w=?year && ?country_code_wiki=?country_code)
}order by ?country ?year
"""

query_4_desc = "Query 4: Carbon emission and no of disaster events in years for country China"
query_4 = """select  ?country_code ?year ?value ?no_of_disaster_events
where {

service <https://labs.tib.eu/sdm/worldbank_endpoint/sparql>{
        ?indicator a wb:AnnualIndicatorEntry;
                wb:hasIndicator wbi:EN.ATM.CO2E.KT;
                wb:hasCountry ?country;
                owl:hasValue ?value;        
                time:year ?year.
        ?country rdfs:label ?country_name;
                dc:identifier ?country_code;
                dbo:region ?region.
        filter(?country_code='CHN' )
}
{
        select ?year_dis (count(?disaster) as ?no_of_disaster_events)
        where { ########## Please add Implisense service ################
        ?disaster a coy:Disaster;
                        coy:hasLocation ?country_dis;
                        coy:hasTimestamp ?timestamp.
                        
        bind(year(?timestamp) as ?year_dis)
        bind(replace(str(?country_dis),"https://data.coypu.org/country/", "") as ?country_dis_code )                
        filter(?country_dis_code='CHN')        
        }group by ?country_dis_code ?year_dis
}
filter(?year_dis=?year)
}
order by ?year
"""

query_5_desc = "Query 5: find industry for the country"
query_5 = """"select ?company ?company_label ?industry
where
{
########## Please add Implisense service below################
    <https://data.coypu.org/company/7d/DEPIYX8Y4M82> coy:hasName ?company_label.
             
    bind(str(<https://data.coypu.org/company/7d/DEPIYX8Y4M82>) as ?company)
    
    Service <https://dbpedia.org/sparql>{
        ?Company_db a dbo:Company;
                 rdfs:label ?company_label_db;
                 dbp:name ?name;
                 dbo:industry ?industry.
    filter(regex(?company_label_db, ?company_label) && lang(?name)='en')
    }
}
limit 10
"""

query_1_fdq_desc="""Q1: For a given country (?country_code) and indicator (?i), return the value of the indicator and the number of disasters registered per year in that country.
For example:
?country_code = ‘CHN’
?i = <http://worldbank.org/Indicator/EN.ATM.CO2E.KT>
"""
query_1_fdq = """SELECT ?year ?year_dis ?value ?disaster
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator ?i .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator time:year ?year .
    ?country   dc:identifier ?country_code .

    ?disaster a coy:Disaster .
    ?disaster time:year ?year_dis .
    ?disaster geo:countryCode ?country_code .

}
"""

query_1_fdq_ex = prefixes+"""
SELECT ?country_code ?year ?year_dis ?value ?disaster
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator <http://worldbank.org/Indicator/EN.ATM.CO2E.KT> .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator time:year ?year .
    ?country   dc:identifier ?country_code .

    ?disaster a coy:Disaster .
    ?disaster time:year ?year_dis .
    ?disaster geo:countryCode ?country_code .

}
"""
query_1_fdq_ex_sql = """SELECT country_code, year, AVG(value) as carbon_emission, COUNT(disaster) AS no_of_disasters
FROM `query_1_fdq_ex`
WHERE year=year_dis
GROUP By country_code, year
Order By  year ASC"""


query_1_fdq_ex_1 = prefixes+prefixes_wb+"""
SELECT ?country_code ?year (AVG(?value) as ?carbon_emission) (COUNT(?disaster) as ?no_of_disasters)
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator <http://worldbank.org/Indicator/EN.ATM.CO2E.KT> .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator time:year ?year .
    ?country   dc:identifier ?country_code .

    ?disaster a coy:Disaster .
    ?disaster time:year ?year .
    ?disaster geo:countryCode ?country_code .
}
GROUP BY ?country_code ?year
ORDER BY ?year
"""


query_2_fdq_desc="""Q2: For a given country (?country_code), return the life expectancy from World Bank and Wikidata per year for that country.
For example:
?country_code = ‘DEU’
"""
query_2_fdq = """SELECT DISTINCT ?date ?year_WB ?year_exp ?year_exp_WB WHERE {
    ?country a wb:Country .
    ?country dc:identifier ?country_code .
    ?country rdfs:label ?country_name .
    ?country dbo:region ?region .
    ?country owl:sameAs ?sameAsCountry .
    ?country wb:hasAnnualIndicatorEntry ?annualIndicator .
    
    
    ?annualIndicator wb:hasIndicator <http://worldbank.org/Indicator/SP.DYN.LE00.IN> .
    ?annualIndicator owl:hasValue ?year_exp_WB .
    ?annualIndicator time:year ?year_WB .

    ?sameAsCountry p:P2250 ?itemLifeExpectancy .
    ?itemLifeExpectancy ps:P2250 ?year_exp .
    ?itemLifeExpectancy pq:P585 ?date .
}
"""

query_2_fdq_ex = prefixes+ prefixes_wiki+ """
SELECT DISTINCT ?country_code ?country_name ?year_WB ?date ?year_exp ?year_exp_WB WHERE {
    ?country a wb:Country .
    ?country dc:identifier ?country_code .
    ?country rdfs:label ?country_name.
    ?country dbo:region ?region.
    ?country owl:sameAs ?sameAsCountry .
    ?country wb:hasAnnualIndicatorEntry ?annualIndicator .
    
    ?annualIndicator wb:hasIndicator <http://worldbank.org/Indicator/SP.DYN.LE00.IN> .
    ?annualIndicator owl:hasValue ?year_exp_WB .
    ?annualIndicator time:year ?year_WB .

    ?sameAsCountry p:P2250 ?itemLifeExpectancy .
    ?itemLifeExpectancy ps:P2250 ?year_exp .
    ?itemLifeExpectancy pq:P585 ?date .
}
"""

query_2_fdq_ex_sql = """SELECT country_code, country_name, year_WB, AVG(year_exp) AS year_avg_exp_wiki, AVG(year_exp_WB) AS year_avg_exp_WB
FROM `query_2_fdq_ex`
WHERE YEAR(date)=year_WB
GROUP BY country_code, country_name, year_WB"""


query_2_fdq_ex_1 = prefixes_wb+ prefixes_wiki+ """
SELECT DISTINCT ?country_code ?country_name ?year (AVG(?year_exp) as ?year_avg_exp_wiki) (AVG(?year_exp_WB) as ?year_avg_exp_WB) 
WHERE {
    ?country a wb:Country .
    ?country dc:identifier ?country_code .
    ?country rdfs:label ?country_name.
    ?country owl:sameAs ?sameAsCountry .
    ?country wb:hasAnnualIndicatorEntry ?annualIndicator .
    
    ?annualIndicator wb:hasIndicator <http://worldbank.org/Indicator/SP.DYN.LE00.IN> .
    ?annualIndicator owl:hasValue ?year_exp_WB .
    ?annualIndicator time:year ?year .

    ?sameAsCountry p:P2250 ?itemLifeExpectancy .
    ?itemLifeExpectancy ps:P2250 ?year_exp .
    ?itemLifeExpectancy pq:P585 ?time .
    BIND(year(?time) AS ?year)
}
GROUP BY ?country_code ?country_name ?year
ORDER BY ?country_code
"""


query_3_fdq_desc="""Q3: For a given country (?c), return the GDP, the population and the GDP per capita per year for that country.
For example:
?c = ‘DEU’
"""
query_3_fdq = """
SELECT ?year ?value ?population
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator <http://worldbank.org/Indicator/NY.GDP.MKTP.CD> .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator wb:worldBankDateYear ?year .
    ?country <http://purl.org/dc/elements/1.1/identifier> ?c .

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 ?c .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?year .
    ?itemP ps:P1082 ?population .
"""

query_3_fdq_ex = prefixes_wb+ prefixes_wiki+ """
SELECT ?year ?value ?population
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator <http://worldbank.org/Indicator/NY.GDP.MKTP.CD> .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator wb:worldBankDateYear ?year .
    ?country <http://purl.org/dc/elements/1.1/identifier> 'DEU' .

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 'DEU' .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?year .
    ?itemP ps:P1082 ?population .
    }
"""

query_3_fdq_ex_sql = """SELECT isocode, country, YEAR(year) AS year1, (value/population) AS `gdp_per_capita($)`
FROM `query_3_fdq_ex`
ORDER BY year1, isocode
"""

query_3_fdq_ex_1 = prefixes_wb+ prefixes_wiki+ """
SELECT ?year ?country ?isoCode ((?value/?population) as ?gdp_per_capita)
WHERE {
    ?indicator a wb:AnnualIndicatorEntry .
    ?indicator wb:hasIndicator <http://worldbank.org/Indicator/NY.GDP.MKTP.CD> .
    ?indicator wb:hasCountry ?country .
    ?indicator owl:hasValue ?value .
    ?indicator wb:worldBankDateYear ?year .
    ?country <http://purl.org/dc/elements/1.1/identifier> 'DEU' .

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 'DEU' .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?year .
    ?itemP ps:P1082 ?population .
}
ORDER BY ?year ?isoCode
"""



query_4_fdq_desc="""Q4: For a given country (?c) and event type (?et), return the fatality percentage and number of events of the specified type per year for that country.
For example:
?c = ‘SYR’
?et = coy:AcledEvent
"""
query_4_fdq = """SELECT ?timestamp ?time ?fatalities ?population ?iri
WHERE {
    ?iri a ?et .
    ?iri coy:hasIsoCode ?c .
    ?iri coy:hasTimestamp ?timestamp .
    ?iri coy:hasFatalities ?fatalities .

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 ?c .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?time .
    ?itemP ps:P1082 ?population .
}
"""
query_4_fdq_ex = prefixes+prefixes_wiki+"""
SELECT ?timestamp ?time ?fatalities ?population ?iri
WHERE {
    ?iri a coy:AcledEvent .
    ?iri coy:hasIsoCode 'SYR' .
    ?iri coy:hasTimestamp ?timestamp .
    ?iri coy:hasFatalities ?fatalities .

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 'SYR' .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?time .
    ?itemP ps:P1082 ?population .
}
"""
query_4_fdq_ex_sql = """SELECT isocode, country, year, SUM(fatalities*1000000/population) AS fatalities_per_million, count(iri) as no_of_events
FROM `query_4_fdq_ex`
WHERE YEAR(timestamp)=year
GROUP BY year, isocode, country
"""

query_4_fdq_ex_1 = prefixes+prefixes_wiki+"""
SELECT ?isoCode ?year (COUNT(?iri) AS ?no_of_events) 
WHERE {
    ?iri a coy:AcledEvent .
    ?iri coy:hasIsoCode 'IDN' .
    ?iri coy:hasTimestamp ?timestamp .
    ?iri coy:hasFatalities ?fatalities .
    BIND(year(?timestamp) as ?year)

    ?countryWiki p:P298 ?isoCode .
    ?isoCode ps:P298 'IDN' .
    ?countryWiki p:P1082 ?itemP .
    ?itemP pq:P585 ?time .
    ?itemP ps:P1082 ?population .
    BIND(year(?time) as ?year)
}
GROUP BY ?year ?isocode
"""