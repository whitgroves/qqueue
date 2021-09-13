import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Form, Row, Col, Badge, Button } from 'react-bootstrap';

// Component

export default function Sell(props) {
  let history = useHistory();

  // Form validation

  const [validated, setValidated] = useState(false);
  const [showError, setShowError] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setShowError(error.length !== 0);
  }, [error]);

  const handleSubmit = (event) => {

    event.preventDefault();

    let name = event.target.name.value;
    let detail = event.target.detail.value;

    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.stopPropagation();
    } else {

      fetch('/products/sell', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          detail: detail,
          seller_id: props.userId,
        })
      }).then(res => res.json()).then(data => {

        if (data['status'] === 500) {
          setError(data['error']);
        } else {
          setError('');
          history.push(`/market/${data['product']['id']}`);
        }

      })
    }

    setValidated(true);

  }

  return (
    <Card>
      <Card.Body>
        <Card.Title data-testid="sell-card-title">sell a product</Card.Title>
        <Form noValidate validated={validated} onSubmit={handleSubmit}>

          <Form.Group controlId="name" data-testid="sell-card-name">
            <Form.Label>product name</Form.Label>
            <Form.Control placeholder="spaceley's sprockets" required />
          </Form.Group>

          <div className="py-2" />

          <Form.Group controlId="detail" data-testid="sell-card-detail">
            <Form.Label>product detail</Form.Label>
            <Form.Control as="textarea" placeholder="tell me more..." />
          </Form.Group>

          <div className="py-2" />

          <Row>
            <Col className="d-inline-flex align-items-center" md="auto">
              {
                showError
                  ? <Badge bg="danger">{error}</Badge>
                  : ''
              }
            </Col>

            <Col></Col> {/* spacer */}

            <Col md="auto">
              <Button data-testid="sell-submit-button" variant="primary" type="submit">
                list for sale →
              </Button>
            </Col>
          </Row>

        </Form>
      </Card.Body>
    </Card>
  );
}