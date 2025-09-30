const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:5173',
    supportFile: false,
    specPattern: 'cypress/e2e/**/*.cy.js'
  }
})
