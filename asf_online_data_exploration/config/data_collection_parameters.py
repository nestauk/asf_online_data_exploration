"""
Script with parameters for data collection.
"""

# -----TWITTER DATA COLLECTION-----

heating_technologies_ruleset_twitter = [
    {
        "value": '"heat pump" OR "heat pumps" OR #heatpump OR #heatpumps',
        "tag": "general_heat_pumps",
    },
    {
        "value": '"air source hp" OR "air source hps" OR "air-source hp" OR "air-source hps" OR #ashp OR #airsourcehp OR #airsourcehps OR #airsourceheatpump OR #airsourceheatpumps',
        "tag": "ashp",
    },
    {
        "value": '"ground source hp" OR "ground source hps" OR "ground-source hp" OR "ground-source hps" OR #gshp OR #groundsourcehp OR #groundsourcehps OR #groundsourceheatpump OR #groundsourceheatpumps',
        "tag": "gshp",
    },
    {
        "value": '"water source hp" OR "water source hps" OR "water-source hp" OR "water-source hps" OR #wshp OR #watersourcehp OR #watersourcehps OR #watersourceheatpump OR #watersourceheatpumps',
        "tag": "wshp",
    },
    {
        "value": '"air to air hp" OR "air to air hps" OR "air-to-air hp" OR "air-to-air hps" OR "air2air hp" OR "air2air hps" OR "a2a hp" OR "a2a hps" OR #atahp OR #airtoairhp OR #airtoairhps OR #airtoairheatpump OR #airtoairheatpumps OR #a2ahp OR #a2ahps OR #air2airhp OR #air2airhps OR #air2airheatpump OR #air2airheatpumps',
        "tag": "atahp",
    },
    {
        "value": '"air to water hp" OR "air to water hps" OR "air-to-water hp" OR "air-to-water hps" OR "air2water hps" OR "air2water hp" OR "a2w hp" OR "a2w hps" OR #atwhp OR #airtowaterhp OR #airtowaterhps OR #airtowaterheatpump OR #airtowaterheatpumps OR #a2whp OR #a2whps OR #air2waterhp OR #air2waterhps OR #air2waterheatpump OR #air2waterheatpumps',
        "tag": "atwhp",
    },
    {
        "value": '"hybrid hp" OR "hybrid hps" OR "bivalent hp" OR "bivalent hps" OR "warm air hp" OR "warm air hps"',
        "tag": "heat_pump_others",
    },
    {
        "value": '"gas boiler" OR "gas boilers" OR #gasboiler OR #gasboilers',
        "tag": "gas_boilers",
    },
    {
        "value": '"oil boiler" OR "oil boilers" OR #oilboiler OR #oilboilers',
        "tag": "oil_boilers",
    },
    {
        "value": '"hydrogen boiler" OR "hydrogen boilers" OR "h2 boiler" OR "h2 boilers" OR #hydrogenboiler OR #hydrogenboiler OR #h2boiler OR #h2boilers',
        "tag": "hydrogen_boilers",
    },
    {
        "value": '"electric boiler" OR "electric boilers" OR #electricboiler OR #electricboilers',
        "tag": "electric_boilers",
    },
    {
        "value": '"biomass boiler" OR "biomass boilers" OR #biomassboiler OR #biomassboilers',
        "tag": "biomass_boilers",
    },
    {"value": '"solar thermal" OR "solar water heating"', "tag": "solar_thermal"},
    {
        "value": '"district heating" OR "heat network" OR "heat networks"',
        "tag": "district_heating",
    },
    {"value": '"hybrid heating"', "tag": "hybrid_heating"},
    {
        "value": '"hp installation" OR "hp installations" OR "hybrid installation" OR "hybrid installations" OR "hybrid heating installation" OR "hybrid heating installations"',
        "tag": "installations",
    },
    {
        "value": '"hp installer" OR "hp installers" OR "hp engineer" OR "hp engineers" OR "heating engineer" OR "heating engineers" OR "boiler engineer" OR "boiler engineers"',
        "tag": "installers_and_engineers",
    },
    {
        "value": '"retrofit installer" OR "retrofit installers" OR "renewables installer" OR "renewables installers"',
        "tag": "retrofit_or_renewable_installers",
    },
    {
        "value": '"low carbon heating" OR "low-carbon heating" OR #lowcarbonheating OR "home decarbonisation" OR #homedecarbonisation',
        "tag": "low_carbon_heating_and_home_decarbonisation",
    },
    {
        "value": '"bus scheme" OR "boiler upgrade scheme" OR "renewable heat incentive" OR "domestic rhi" OR "clean heat grant" OR "home energy scotland grant" OR "home energy scotland loan" OR "home energy scotland scheme"',
        "tag": "government_grants",
    },
    {
        "value": '"microgeneration certification scheme" OR "mcs certified" OR "mcs certification" OR "mcs installation" OR "mcs installations"',
        "tag": "microgeneration_certification_scheme",
    },
    {
        "value": '"hp cost estimator" OR "hp cost calculator" OR (hp cost (estimate OR estimator OR calculator OR tool) (nesta OR @nesta_uk))',
        "tag": "nesta_cost_estimator_tool",
    },
]

query_parameters_twitter = {
    "tweet.fields": "id,text,author_id,edit_history_tweet_ids,attachments,conversation_id,created_at,lang,context_annotations,entities,geo,public_metrics,source,in_reply_to_user_id,possibly_sensitive,referenced_tweets,reply_settings",
    "user.fields": "id,name,username,created_at,description,location,verified,public_metrics,entities,url",
    "place.fields": "id,country,country_code,name,full_name,geo,place_type,contained_within",
    "media.fields": "media_key,type,url,duration_ms,preview_image_url,public_metrics,alt_text",
    "expansions": "author_id,geo.place_id,attachments.media_keys",
    "max_results": 100,
}

# -----THE GUARDIAN API DATA COLLECTION-----

heating_technologies_ruleset_guardian = [
    {"value": '"heat pump" OR "heat pumps"', "tag": "general_heat_pumps"},
    {
        "value": '"air source hp" OR "air source hps" OR "air-source hp" OR "air-source hps"',
        "tag": "ashp",
    },
    {
        "value": '"ground source hp" OR "ground source hps" OR "ground-source hp" OR "ground-source hps"',
        "tag": "gshp",
    },
    {
        "value": '"water source hp" OR "water source hps" OR "water-source hp" OR "water-source hps"',
        "tag": "wshp",
    },
    {
        "value": '"air to air hp" OR "air to air hps" OR "air-to-air hp" OR "air-to-air hps" OR "air2air hp" OR "air2air hps" OR "a2a hp" OR "a2a hps"',
        "tag": "atahp",
    },
    {
        "value": '"air to water hp" OR "air to water hps" OR "air-to-water hp" OR "air-to-water hps" OR "air2water hps" OR "air2water hp" OR "a2w hp" OR "a2w hps"',
        "tag": "atwhp",
    },
    {
        "value": '"hybrid hp" OR "hybrid hps" OR "bivalent hp" OR "bivalent hps" OR "warm air hp" OR "warm air hps"',
        "tag": "heat_pump_others",
    },
    {"value": '"gas boiler" OR "gas boilers"', "tag": "gas_boilers"},
    {"value": '"oil boiler" OR "oil boilers"', "tag": "oil_boilers"},
    {
        "value": '"hydrogen boiler" OR "hydrogen boilers" OR "h2 boiler" OR "h2 boilers"',
        "tag": "hydrogen_boilers",
    },
    {"value": '"electric boiler" OR "electric boilers"', "tag": "electric_boilers"},
    {"value": '"biomass boiler" OR "biomass boilers"', "tag": "biomass_boilers"},
    {"value": '"solar thermal" OR "solar water heating"', "tag": "solar_thermal"},
    {
        "value": '"district heating" OR "heat network" OR "heat networks"',
        "tag": "district_heating",
    },
    {"value": '"hybrid heating"', "tag": "hybrid_heating"},
    {
        "value": '"hp installation" OR "hp installations" OR "hybrid installation" OR "hybrid installations" OR "hybrid heating installation" OR "hybrid heating installations"',
        "tag": "installations",
    },
    {
        "value": '"hp installer" OR "hp installers" OR "hp engineer" OR "hp engineers" OR "heating engineer" OR "heating engineers" OR "boiler engineer" OR "boiler engineers"',
        "tag": "installers_and_engineers",
    },
    {
        "value": '"retrofit installer" OR "retrofit installers" OR "renewables installer" OR "renewables installers"',
        "tag": "retrofit_or_renewable_installers",
    },
    {
        "value": '"low carbon heating" OR "low-carbon heating" OR "home decarbonisation"',
        "tag": "low_carbon_heating_and_home_decarbonisation",
    },
    {
        "value": '"bus scheme" OR "boiler upgrade scheme" OR "renewable heat incentive" OR "domestic rhi" OR "clean heat grant" OR "home energy scotland grant" OR "home energy scotland loan" OR "home energy scotland scheme"',
        "tag": "government_grants",
    },
    {
        "value": '"microgeneration certification scheme" OR "mcs certified" OR "mcs certification" OR "mcs installation" OR "mcs installations"',
        "tag": "microgeneration_certification_scheme",
    },
    {
        "value": '"hp cost estimator" OR "hp cost calculator" OR (hp AND cost (estimate OR estimator OR calculator OR tool) AND nesta)',
        "tag": "nesta_cost_estimator_tool",
    },
]

query_parameters_guardian = {
    "page-size": 100,
    "use-date": "published",
}

dates_for_guardian_collection = []
years = [2021, 2022]
for y in years:
    params = {}
    params["from-date"] = f"{y}-01-01"
    params["to-date"] = f"{y}-12-31"
    dates_for_guardian_collection.append(params)
dates_for_guardian_collection.append(
    {"from-date": "2023-01-01", "to-date": "2023-01-31"}
)

# -----MEDIA CLOUD API DATA COLLECTION-----
