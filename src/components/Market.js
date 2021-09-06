import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Card, Col, Row, Button } from 'react-bootstrap';

// Component

export default function Market(props) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products').then(res => res.json()).then(data => {
      setProducts(data.products);
    });
  }, []); // Remove dependencies so it only loads once.

  return (
    <Container fluid>
      <Row className="gap-4">
          {products.map((product, index) => (
          <Col key={index}>
              <Card  style={{ width: '15rem' }}>
                <Card.Img variant="top" src={product.image_url}/>
                <Card.Body>
                    <Card.Title>{product.name}</Card.Title>
                    <Card.Subtitle>${product.price ? product.price.toFixed(2) : 0}</Card.Subtitle>
                    <Card.Text>{product.tagline}</Card.Text>
                    <Row>
                      <Col>
                        <Button variant="outline-dark" size="sm" href={'/product/'+product.id}>view →</Button>{' '}
                      </Col>
                      <Col md="auto">
                        <Button variant="outline-primary" size="sm" onClick={() => props.addToCart(product.id)}>
                          add to cart +
                        </Button>
                      </Col>
                    </Row>
                </Card.Body>
              </Card>
          </Col>
          ))}
      </Row>
    </Container>
  );
}