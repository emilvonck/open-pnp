from flask import make_response, Flask, request, Response
from flask_restx import Api, Resource
import xmltodict
import logging
import sys
app = Flask(__name__)
api = Api(app, default_mediatype="application/xml")

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout,
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(xmltodict.unparse(data, pretty=True), code)
    resp.headers.extend(headers or {})
    return resp


api.representations["application/xml"] = output_xml

@api.route("/pnp/HELLO")
class PnPHello(Resource):

    def get(self):
        return '', 200


@api.route("/pnp/WORK-REQUEST")
class PnPWorkReq(Resource):

    @api.produces(["application/xml; charset=utf-8"])
    @api.doc(description="""
    ### PnP WORK-REQUEST
  ```
  curl -X 'POST' \\
    '{{ scheme }}://{{ host }}:{{ port }}/pnp/WORK-REQUEST' \\
    -H 'accept: application/xml' \\
    -H 'Content-Type: application/json' \\
    -d '<pnp xmlns="urn:cisco:pnp" version="1.0" udi="PID:WS-C3750X-24T-E,VID:V04,SN:FDO1703P2EB">
          <info xmlns="urn:cisco:pnp:work-info" correlator="CiscoPnP-1.0-1465-25A1212C">
             <deviceId>
              <udi>PID:WS-C3750X-24T-E,VID:V04,SN:FDO1703P2EB</udi>
              <hostname>Router</hostname>
              <authRequired>true</authRequired>
              <viaProxy>false</viaProxy>
              <securityAdvise>Password in clear text in unsecured transport</securityAdvise>
             </deviceId>
            </info>
          </pnp>'
  ```
    """)
    def post(self):
        xml_data = request.get_data().decode()
        parsed_data = xmltodict.parse(xml_data)
        udi_raw = parsed_data['pnp']['@udi']
        udi_list = udi_raw.split(',')
        udi_parsed = {i.split(':')[0]: i.split(':')[1] for i in udi_list}
        return_data = {**parsed_data['pnp']}
        logger.info(xml_data)
        logger.info(udi_parsed)

        return_xml = xmltodict.unparse({'pnp': return_data})

        return Response(return_xml, mimetype='application/xml')



if __name__ == "__main__":
    app.run(debug=True)