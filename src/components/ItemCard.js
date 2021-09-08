import React, { useState, useEffect } from 'react';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { Card, Col, Row, Button } from 'react-bootstrap';

// Component

export default function ItemCard(props) {
  let product = props.product;
  return (
    <Card style={{ width: '15rem' }}>
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
              {
                props.isVendor
                  ? ''
                  : 
                    <Button variant="outline-primary" size="sm" onClick={() => props.addToCart(product.id)}>
                      add to cart +
                    </Button>
              }
            </Col>
          </Row>
      </Card.Body>
    </Card>
  );
}