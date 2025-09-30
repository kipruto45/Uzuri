describe('Academic Leave upload flow', () => {
  it('submits a leave request with attachments to staging', () => {
    // staging base URL should be set via CYPRESS_BASE_URL env var or cypress.config.js
    cy.visit('/academic-leave')
    cy.get('button').contains('New Request').click()
    cy.get('select').select('medical')
    cy.get('input[type=date]').first().type('2025-10-01')
    cy.get('input[type=date]').last().type('2025-10-05')
    cy.get('textarea').type('Testing E2E upload flow')
    // attach a file (requires enabling file upload via cypress-file-upload plugin if needed)
    const fileName = 'test.pdf'
    cy.fixture(fileName).then(fileContent => {
      cy.get('input[type=file]').attachFile({ fileContent, fileName, mimeType: 'application/pdf' })
    })
    cy.get('button').contains('Next').click()
    cy.get('button').contains('Submit').click()
    // expect combined upload modal to show
    cy.contains('Uploading documents').should('exist')
  })
})
