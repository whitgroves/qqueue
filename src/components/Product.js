import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import { 
  Container, Card, Col, Row, Button, ListGroup, ListGroupItem 
} from 'react-bootstrap';

// Component

export default function Product(props) {
  const { id } = useParams();

  const [product, setProduct] = useState({});

  useEffect(() => {
    fetch('/api/products/'+id).then(res => res.json()).then(data => {
      setProduct(data.product);
    });
  }, [id]);

  return (
    <Container>

      <Row className="gap-1">

        <Col md="auto">
          <Card>
            <Card.Img variant="top" src={product.image_url}/>
            <Card.Body>
                <Card.Text>{product.tagline}</Card.Text>
            </Card.Body>
          </Card>
        </Col>

        <Col>
          <Card>
            
            <Card.Header>Details</Card.Header>

            <Card.Body>
              <Card.Title>{product.name}</Card.Title>
              <Card.Subtitle>${product.price ? product.price.toFixed(2) : 0}</Card.Subtitle>
              <Card.Text>{product.detail}</Card.Text>
            </Card.Body>

            <ListGroup className="list-group-flush">
              <ListGroupItem>
                <a href={product.website} target="_blank" rel="noreferrer">Product Website</a>
              </ListGroupItem>
              <ListGroupItem>Rating</ListGroupItem>
              <ListGroupItem>{product.qty} available</ListGroupItem>
            </ListGroup>

            <Card.Body className="d-grid">
              <Button variant="outline-primary" onClick={() => props.addToCart(product.id)}>
                add to cart +
              </Button>
            </Card.Body>

          </Card>
        </Col>

      </Row>

      <Row className="py-4">
        <Col md="auto">
          <Button href="/market" variant="outline-dark">← market</Button>
        </Col>
        <Col></Col>
        <Col md="auto">
          <Button href="/cart" variant="outline-dark">my cart →</Button>
        </Col>
      </Row>

    </Container>
  );
}