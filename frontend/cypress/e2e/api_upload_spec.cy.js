describe('Academic Leave API upload (API-only)', () => {
  it('creates a leave request and uploads a document via API', () => {
    const base = Cypress.env('API_BASE') || 'http://localhost:8000'
    // create leave request
    cy.request({
      method: 'POST',
      url: `${base}/academic-leave/requests/`,
      body: {
        leave_type: 'medical',
        start_date: '2025-10-01',
        end_date: '2025-10-03',
        reason: 'API-only test upload'
      },
      failOnStatusCode: false,
    }).then((res) => {
      expect([200,201]).to.include(res.status)
      const id = res.body.id
      expect(id).to.be.a('number')
      // upload a file using cy.fixture and cy.request with formData
      cy.fixture('test.pdf', 'binary').then((fileBinary) => {
        const blob = Cypress.Blob.binaryStringToBlob(fileBinary, 'application/pdf')
        const form = new FormData()
        form.append('file', blob, 'test.pdf')
        cy.request({
          method: 'POST',
          url: `${base}/academic-leave/requests/${id}/submit_document/`,
          body: form,
          headers: {
            // let Cypress set content-type for multipart
          },
          // Cypress will not automatically set correct multipart headers for FormData in node; failOnStatusCode false to capture responses
          failOnStatusCode: false,
        }).then((uRes) => {
          expect([200,201]).to.include(uRes.status)
        })
      })
    })
  })
})
