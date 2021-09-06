import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Col, Row, Button, Form, Badge } from 'react-bootstrap';

// Component

export default function Login(props) {
  const { loginType } = useParams();
  let history = useHistory();

  // Form submission
  const [validated, setValidated] = useState(false);
  const [loginError, setLoginError] = useState('');
  const [showLoginError, setShowLoginError] = useState(false);

  const handleSubmit = (event) => {
    
    const form = event.currentTarget;

    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      event.preventDefault();
      let email = event.target.login_email.value;
      let password = event.target.login_password.value;

      fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          email: email,
          password: password
        })
      }).then(res => res.json()).then(data => {
        if ('error' in data) {
          setValidated(false);
          setLoginError(data['error']);
          setShowLoginError(true);
        } else {
          setLoginError('');
          setShowLoginError(false);
          props.onLogin(data);
          history.push('/orders')
        }
      });
    }

    setValidated(true);
    
  }

  // Render

  return (
    <Card>
      <Card.Body>
        <Card.Title>{loginType} login</Card.Title>
        <Form noValidate validated={validated} onSubmit={handleSubmit}>

          <Form.Group controlId="login_email">
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

          <Form.Group controlId="login_password">
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

          <div class="py-2" />

          <Row>
            <Col className="d-inline-flex align-items-center" md="auto">
              { 
                showLoginError 
                  ? <Badge pill bg="danger">{loginError}</Badge> 
                  : ''
              }
            </Col>

            <Col></Col> {/* spacer */}

            <Col md="auto">
              <Button variant="primary" type="submit">sign in →</Button>
            </Col>
          </Row>

        </Form>
      </Card.Body>
    </Card>
  );
}