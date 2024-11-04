<%page args="display_name, service_class"/>\
<%
    import json

    service_config = {
      "services": [
          {
              "displayName": display_name,
              "serviceClass": service_class,
              "descriptionUrl": "",
              "providedInterfaces": [
                  "ni.measurementlink.measurement.v1.MeasurementService",
                  "ni.measurementlink.measurement.v2.MeasurementService",
              ],
              "path": "start.bat",              
              "annotations": {
                "ni/service.description": "",
                "ni/service.collection": "",
                "ni/service.tags": []
              }
          }
       ]
    }
%>\
${json.dumps(service_config, indent=2)}