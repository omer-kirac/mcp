require('dotenv').config();

module.exports = {
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  anthropicApiKey: process.env.ANTHROPIC_API_KEY
};
