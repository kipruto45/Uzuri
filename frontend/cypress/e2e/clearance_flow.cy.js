// Cypress E2E spec: upload -> preview -> download -> edit -> delete

describe('Clearance flow', () => {
  beforeEach(() => {
    cy.intercept('GET', '/api/clearance/', { fixture: 'clearance_empty.json' }).as('list')
    cy.visit('/clearance')
    cy.wait('@list')
  })

  it('uploads, previews, downloads, edits and deletes a clearance document', () => {
    // stub upload
    cy.intercept('POST', '/api/clearance/', { id: 123, title: 'Test Doc', created_at: new Date().toISOString(), size: 1024 }).as('upload')
    cy.get('input[placeholder="Document title"]').type('Test Doc')
    // simulate file upload via fixture
    cy.get('input[type=file]').attachFile('test.pdf')
    cy.wait('@upload')

    // stub download blob
    cy.intercept('GET', '/api/clearance/123/download/', { fixture: 'test.pdf' }).as('download')

    cy.contains('Test Doc').should('exist')
    cy.contains('Preview').click()
    cy.wait('@download')
    cy.get('button').contains('Close').click()

    // Edit metadata
    cy.intercept('PATCH', '/api/clearance/123/', { id: 123, title: 'Test Doc v2', department: 'Dept' }).as('patch')
    cy.contains('Edit').click()
    cy.get('input').contains('Title')
    cy.get('input').first().clear().type('Test Doc v2')
    cy.get('button').contains('Save').click()
    cy.wait('@patch')
    cy.contains('Test Doc v2').should('exist')

    // Delete
    cy.intercept('DELETE', '/api/clearance/123/', { statusCode: 204 }).as('del')
    cy.contains('Delete').click()
    cy.wait('@del')
    cy.contains('Test Doc v2').should('not.exist')
  })
})
