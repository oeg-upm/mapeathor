import mapeathor

from flask import Flask, send_file, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Resource, Api, reqparse
from werkzeug import datastructures
import tempfile

parser = reqparse.RequestParser()
parser.add_argument('file',type=datastructures.FileStorage, location='files')
parser.add_argument('url')
parser.add_argument('format')

app = Flask(__name__)
api = Api(app)

# Input:
## file: Excel file
### [or]
## url: Google Drive

## format: output mapping format

# Output:
## file: output mapping

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/api/'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={ 
        'app_name': "Mapeathor"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


class Mapeathor(Resource):
    def get(self):
        swag = swagger(app)
        swag['info']['version'] = "1.0.0"
        swag['info']['title'] = "Mapeathor"
        return jsonify(swag)
        
    def post(self):
        
        """
        Translate mapping document
        ---
        
        components:
          schemas:
            Excel:
              type: object
              properties:
                format:
                  type: string
                  enum: [ "rml", "r2rml", "yarrrml"]
                file:
                  type: file
                  description: XLS[X] file to convert
            GSpreadSheet:
              type: object
              properties:
                format:
                  type: string
                  enum: [ "rml", "r2rml", "yarrrml"]
                url:
                  type: string
                  description: Google Spreadsheet url to convert

        summary: Uploads a file.
        consumes:
            - multipart/form-data
        produces:
            - binary/octet-stream
        parameters:
            - in: formData
              name: format
              type: text
              enum: [ "rml", "r2rml", "yarrrml"]
              description: Mapping output format
            - in: formData
              name: url
              type: string
              description: Google Spreadsheet url to convert
            - in: formData
              name: file
              type: file
              description: XLS[X] file to convert
        responses:
            '200':
                description: 'Mapping file in the specified format'
            '401':
                description: 'Bad request'
            '500':
                description: 'Internal tool error'
        """
        
        data = parser.parse_args()
        
        print(data)
        
        if data['file'] is None and data['url'] is None:
            return {'message':'File or URL not found'}
        if data['format'] is None:
            return {'message':'No output mapping format specified'}
        else:
            
            temp_out = tempfile.NamedTemporaryFile(prefix="mapeathor-api").name
            
            if data['file'] is None:
                
                temp_in = mapeathor.gdriveToXMLX(data['url'])
            
            else:
                
                temp_in = tempfile.NamedTemporaryFile(prefix="mapeathor-api").name

                data['file'].save(temp_in)
            
            mapeathor.setMappingLanguage(data["format"])
            
            outputFile = mapeathor.generateMapping(temp_in, temp_out)
            
            return send_file(outputFile, as_attachment=True)
            

api.add_resource(Mapeathor, API_URL)


def run(host="0.0.0.0", port=5000):
    
    print("API URL: "+API_URL)
    print("SWAGGER URL: "+SWAGGER_URL)
    
    app.run(debug=False, host=host, port=port)

if __name__ == '__main__':
    run()

