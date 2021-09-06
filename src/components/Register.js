import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Col, Row, Button, Form, Badge } from 'react-bootstrap';

// Component

export default function Register(props) {
  const { registrationType } = useParams();

  // Form submission
  const [validated, setValidated] = useState(false);
  const [error, setError] = useState('');
  const [showError, setShowError] = useState(false);

  const handleSubmit = (event) => {
    
    const form = event.currentTarget;
    let password = event.target.register_password.value;
    let passwordConfirm = event.target.register_password_confirm.value;

    event.preventDefault();
    if (password !== passwordConfirm) {
      event.stopPropagation();
      setError('Passwords do not match.');
      setShowError(true);
    } else if (form.checkValidity() === false) {
      event.stopPropagation();
    } else {
      let email = event.target.register_email.value;

      fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          email: email,
          password: password
        })
      }).then(res => res.json()).then(data => {
        if ('error' in data) {
          setValidated(false);
          setError(data['error']);
          setShowError(true);
        } else {
          setError('');
          setShowError(false);
          props.onRegister(data);
        }
      });
    }

    setValidated(true);
    
  }

  // Render

  return (
    <Card>
      <Card.Body>
        <Card.Title>{registrationType} registration</Card.Title>
        <Form noValidate validated={validated} onSubmit={handleSubmit}>

          <Form.Group controlId="register_email">
            <Form.Label>email</Form.Label>
            <Form.Control type="email" required />

            <Form.Control.Feedback type="invalid">
              Please enter a valid email.
            </Form.Control.Feedback>

            <Form.Text className="text-muted">
              We never share this.
            </Form.Text>
          </Form.Group>

          <div class="py-2"/>

          <Form.Group controlId="register_password">
            <Form.Label>password</Form.Label>
            <Form.Control type="password" required />

            <Form.Control.Feedback type="invalid">
              Please enter your password.
            </Form.Control.Feedback>

            <Form.Text className="text-muted">
              We can't see this.
              {' '}
              <a 
                href="https://security.stackexchange.com/q/33860" 
                target="_blank" 
                rel="noreferrer" 
                tabIndex={-1}
              >
                Learn more.
              </a>
            </Form.Text>
          </Form.Group>

          <div class="py-2"/>

          <Form.Group controlId="register_password_confirm">
            <Form.Label>confirm password</Form.Label>
            <Form.Control type="password" required />

            <Form.Control.Feedback type="invalid">
              Passwords re-enter your password.
            </Form.Control.Feedback>
          </Form.Group>

          <div class="py-2" />

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
              <Button variant="primary" type="submit">sign up</Button>
            </Col>
          </Row>

        </Form>
      </Card.Body>
    </Card>
  );
}