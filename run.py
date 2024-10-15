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
        return_xml = 'hello'
        return Response({'hello': return_xml}, mimetype='application/xml')


@api.route("/pnp/WORK-REQUEST")
class PnPWorkReq(Resource):

    @api.produces(["application/xml; charset=utf-8"])
    @api.doc(description="""
    ### PnP WORK-REQUEST
  ```
  curl -X 'POST' \\
    '{{ scheme }}://{{ host }}:{{ port }}/pnp/WORK-REQUEST' \\
    -H 'accept: application/xml' \\
    -H 'Content-Type: application/xml' \\
    -d '<pnp xmlns="urn:cisco:pnp" version="1.0" udi="PID:CSR1000V,VID:V00,SN:99CWJ5DOLWQ">
          <info xmlns="urn:cisco:pnp:work-info" correlator="CiscoPnP-1.0-R33.200930-I1-P592-T43891-2">
              <deviceId>
                  <udi>PID:CSR1000V,VID:V00,SN:99CWJ5DOLWQ</udi>
                  <macAddress></macAddress>
                  <hostname>Router</hostname>
                  <authRequired>false</authRequired>
                  <viaProxy>false</viaProxy>
                  <securityAdvise>Password in clear text in unsecured transport</securityAdvise>
              </deviceId>
              <reason>
                  <reload>
                      <message>factory-reset</message><code>PnP Service Info 2408</code>
                      <startupConfigPresent>false</startupConfigPresent>
                  </reload>
              </reason>
          </info>
        </pnp>'
  ```
    """)
    def post(self):
        xml_data = request.get_data().decode()
        parsed_payload = xmltodict.parse(xml_data)
        logger.info(parsed_payload)
        device_info = {
            '@xmlns': 'urn:cisco:pnp',
            '@version': '1.0',
            '@udi': '',
            '@usr': 'admin',
            '@pwd': 'cisco',
            'request': {
                '@correlator': '',
                '@xmlns': 'urn:cisco:pnp:device-info',
                'deviceInfo': {
                    '@type': 'all'
                }
            }
        }
        device_info['@udi'] = parsed_payload['pnp']['@udi']
        device_info['request']['@correlator'] = parsed_payload['pnp']['info']['@correlator']

        return {'pnp': device_info}, 200

@api.route("/pnp/WORK-RESPONSE")
class PnPWorkResp(Resource):

    @api.produces(["application/xml; charset=utf-8"])
    @api.doc(description="""
    ### PnP WORK-RESPONSE
  ```
    curl -X 'POST' \\
    '{{ scheme }}://{{ host }}:{{ port }}/pnp/WORK-RESPONSE' \\
    -H 'accept: application/xml' \\
    -H 'Content-Type: application/xml' \\
    -d '<pnp xmlns="urn:cisco:pnp" version="1.0" udi="PID:CSR1000V,VID:V00,SN:95HUSMATW2U">
          <response xmlns="urn:cisco:pnp:device-info" correlator="CiscoPnP-1.0-R33.200930-I1-P592-T47132-2" success="1">
            <thisProfileName>pnp-zero-touch</thisProfileName>
            <udi>
              <primary-chassis>PID:CSR1000V,VID:V00,SN:95HUSMATW2U</primary-chassis>
            </udi>
            <imageInfo>
              <versionString>17.3.4a</versionString>
              <imageFile>bootflash:packages.conf</imageFile>
              <imageHash />
              <returnToRomReason>reload</returnToRomReason>
              <bootVariable />
              <bootLdrVariable />
              <configVariable />
              <configReg>0x2102</configReg>
              <configRegNext />
            </imageInfo>
            <hardwareInfo>
              <hostname>Router</hostname>
              <vendor>cisco</vendor>
              <platformName>CSR1000V</platformName>
              <processorType>VXE</processorType>
              <hwRevision>VXE</hwRevision>
              <mainMemSize>2121553596</mainMemSize>
              <ioMemSize>3149400</ioMemSize>
              <boardId>95HUSMATW2U</boardId>
              <boardReworkId />
              <processorRev />
              <midplaneVersion />
              <location />
              <deviceType />
            </hardwareInfo>
            <fileSystemList>
              <fileSystem name="bootflash" type="disk" size="6286540800" freespace="5438058496" readable="true" writable="true" />
              <fileSystem name="webui" type="disk" size="2013806592" freespace="1910181888" readable="true" writable="false" />
              <fileSystem name="nvram" type="nvram" size="33554432" freespace="33551308" readable="true" writable="false" />
            </fileSystemList>
            <profileInfo>
              <profile profile-name="pnp-zero-touch" discovery-created="true" created-by="DHCP">
                <primary-server>
                  <protocol>http</protocol>
                  <server-address>
                    <ipv4>192.168.100.100</ipv4>
                    <port>5000</port>
                  </server-address>
                </primary-server>
              </profile>
            </profileInfo>
            <stackInfo>
              <stackable>false</stackable>
            </stackInfo>
            <deviceModeInfo>
              <isControllerManaged>false</isControllerManaged>
              <mustReloadToChange>true</mustReloadToChange>
              <initialDeviceMode>autonomous</initialDeviceMode>
              <newDeviceMode>autonomous</newDeviceMode>
            </deviceModeInfo>
          </response>
        </pnp>'
  ```
    """)
    def post(self):
        xml_data = request.get_data().decode()
        parsed_payload = xmltodict.parse(xml_data)
        logger.info(parsed_payload)
        return Response(status=200)



if __name__ == "__main__":
    app.run(debug=True)