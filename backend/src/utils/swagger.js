const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const path = require('path');

const setupSwagger = (app) => {
  const swaggerDocument = YAML.load(path.join(__dirname, '../../swagger.yaml'));
  
  app.use('/api/v1/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
  
  console.log('Swagger Docs available at /api/v1/docs');
};

module.exports = setupSwagger;
