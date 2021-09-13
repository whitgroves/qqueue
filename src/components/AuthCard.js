import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Col, Row, Button, Form, Badge } from 'react-bootstrap';

// Component

export default function AuthCard(props) {

  let history = useHistory();

  const isRegistration = props.isRegistration ? props.isRegistration : false;

  // Form validation

  const [validated, setValidated] = useState(false);
  const [showError, setShowError] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setShowError(error.length !== 0);
  }, [error]);

  const handleSubmit = (event) => {

    event.preventDefault();

    let password = event.target.password.value;
    let hasRegistrationError = false;

    if (isRegistration) {
      let passwordConfirm = event.target.password_confirm.value;
      if (password !== passwordConfirm) {
        event.stopPropagation();
        setError('Passwords do not match.');
        hasRegistrationError = true;
      }
    }

    if (!isRegistration || !hasRegistrationError) {
      const form = event.currentTarget;

      if (form.checkValidity() === false) {
        event.stopPropagation();
      }
      else {
        let email = event.target.email.value;
        let endpoint = isRegistration ? '/auth/register' : '/auth/login';

        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: email,
            password: password,
          })

        }).then(res => res.json()).then(data => {

          if (data['status'] === 500) {
            setError(data['error']);
          }
          else {
            setError('');
            props.onAuthenticated(data);
            history.push('/orders')
          }
        });
      }

    }

    setValidated(true);

  }

  // Render

  return (
    <Card>
      <Card.Body>
        <Card.Title data-testid="auth-card-title">{isRegistration ? 'sign up' : 'sign in'}</Card.Title>
        <Form noValidate validated={validated} onSubmit={handleSubmit}>

          <Form.Group controlId="email" data-testid="auth-card-email">
            <Form.Label>email</Form.Label>
            <Form.Control type="email" required />

            <Form.Control.Feedback type="invalid">
              Please enter a valid email.
            </Form.Control.Feedback>

            <Form.Text className="text-muted">
              We never share this.
            </Form.Text>
          </Form.Group>

          <div className="py-2" />

          <Form.Group controlId="password" data-testid="auth-card-password">
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

          <div className="py-2" />

          {
            isRegistration
              ? <Form.Group controlId="password_confirm" data-testid="auth-card-password-confirm">
                <Form.Label>confirm password</Form.Label>
                <Form.Control type="password" required />

                <Form.Control.Feedback type="invalid">
                  Passwords re-enter your password.
                </Form.Control.Feedback>
              </Form.Group>
              : ''
          }

          {
            isRegistration
              ? <div className="py-2" />  // don't want to group with password_confirm
              : ''
          }

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
              <Button data-testid="auth-submit-button" variant="primary" type="submit">
                {isRegistration ? 'sign up' : 'sign in'}
              </Button>
            </Col>
          </Row>

        </Form>
      </Card.Body>
    </Card>
  );
}