import arcpy, json, os
import arcpy
import urllib.request, urllib.parse, urllib.error

def get_tools():
    return [    
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, example: Perth, Western Australia",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "getSchoolsInSuburb",
                "description": "Get the schools in a given suburb of WA",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "inputSuburb": {
                            "type": "string",
                            "description": "The suburb, example: Perth",
                        },
                    },
                    "required": ["inputSuburb"],
                }
            }
        }
    ]

def get_current_weather(location, unit="celcius"):
    """Get the current weather in a given location - this is just an example of how to handle tool calls"""
    weather_info = {
        "location": location,
        "temperature": "32",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def getSchoolsInSuburb(inputSuburb):
    #################################################
    ## Name: getSchoolsInSuburb
    ##################################################
    ## Description: Queries SLIP Public Services to 
    ## Return Schools in a Specfic Suburb. Returns the
    ## Suburb Boundary and Selects all Schools within.
    ## MUST BE RUN WITHIN AN OPEN ARCGIS PRO SESSION.
    ##################################################
    ## Author: Callan Joiner
    ## Created Date: 28/12/2023
    ## Last Updated: 29/12/2023
    ##################################################

    ### Initialise Script 
    ## Get Current APRX Default GDB
    aprx = arcpy.mp.ArcGISProject('CURRENT')

    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = aprx.defaultGeodatabase

    ### Function to Query Input Suburb Name
    def getSuburbBdy(suburb):
        queryURL = r'https://public-services.slip.wa.gov.au/public/rest/services/SLIP_Public_Services/Boundaries/MapServer/16/query?'
        whereClause = "name=" + "'" + str.upper(suburb) + "'"

        params = {'where': whereClause,
            'geometryType': 'esriGeometryPolygon',
            'returnGeometry': 'true',
            'outSR': 4326,
            'f': 'pjson'
            }

        encode_params = urllib.parse.urlencode(params).encode("utf-8")

        response = urllib.request.urlopen(queryURL, encode_params)
        suburbFeatures = json.loads(response.read())
        suburbGeom = suburbFeatures['features'][0]['geometry']

        return suburbGeom

    ### Function to Determine Schools the are Within the Input Suburb
    def getSchools(suburbGeom):
        ## Determine Latest Schools Map Service Layer ID
        queryURL = r'https://public-services.slip.wa.gov.au/public/rest/services/SLIP_Public_Services/Education/MapServer/Layers'
        lyrParams = {'f': 'pjson'
            }

        encode_params = urllib.parse.urlencode(lyrParams).encode("utf-8")

        response = urllib.request.urlopen(queryURL, encode_params)
        lyrJson = json.loads(response.read())
        lyrs = lyrJson['layers']

        idNums = []

        for lyr in lyrs:
            idNums.append(lyr['id'])
        
        latestSchoolsId= max(idNums)

        # Query Latest Schools Layer
        queryURL = r'https://public-services.slip.wa.gov.au/public/rest/services/SLIP_Public_Services/Education/MapServer/' + str(latestSchoolsId) + '/query?'
        params = {'where': '1=1',
            'outFields': '*',
            'geometry': suburbGeom,
            'spatialRel': 'esriSpatialRelContains',
            'geometryType': 'esriGeometryPolygon',
            'returnGeometry': 'true',
            'outSR': 4326,
            'f': 'pjson'
            }
        
        encode_params = urllib.parse.urlencode(params).encode("utf-8")

        response = urllib.request.urlopen(queryURL, encode_params)
        schoolFeatures = json.loads(response.read())

        return schoolFeatures

    # Run Script
    suburbResp = getSuburbBdy(inputSuburb)
    schoolsResp = getSchools(suburbResp)

    with open(aprx.homeFolder + "\schools.json", "w") as ms_json:
        ms_json.write(str(schoolsResp))

    arcpy.JSONToFeatures_conversion(aprx.homeFolder + "\schools.json", r"schoolsIn_" + inputSuburb)
    lyr = aprx.defaultGeodatabase + "\schoolsIn_" + inputSuburb

    os.remove(aprx.homeFolder + "\schools.json")
    map = aprx.activeMap
    map.addDataFromPath(lyr)

    cam = aprx.activeView.camera
    ext = arcpy.Describe(lyr).extent
    cam.setExtent(ext)

    completionMessage = "Schools in the suburb of " + inputSuburb + " have been added to the map."

    return completionMessage


def call_tool(function_name, function_params, workspace):
    """
    calls one of the defined skill functions.

    Args:
        function_name (string): name of the skill function to call.
        params (dict): required parameters defined in a python dictionary with key value pairs of [param name]:[value]. Example for a function that requires a 'location' parameter: {"location": "Perth"}"

    Returns:
        string: return value of the called function as a json string.
    """

    if function_name == "get_current_weather":
        arcpy.AddMessage("SYSTEM: weather function detected from user intent.")
        location_param = function_params["location"]
        return get_current_weather(location_param)
    elif function_name == "getSchoolsInSuburb":
        arcpy.AddMessage("SYSTEM: get schools in suburb function detected from user intent.")
        inputSuburb_param = function_params["inputSuburb"]
        return getSchoolsInSuburb(inputSuburb_param)
    else:
        arcpy.AddMessage("SYSTEM: Error: unmatched function name.")
        return "Error: unmatched function name."