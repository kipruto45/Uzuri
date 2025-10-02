describe('Dashboard smoke', () => {
  it('loads dashboard and shows key widgets', () => {
    cy.visit('/')
    cy.get('h1').contains('Dashboard')
    cy.get('section').should('exist')
  })
})
