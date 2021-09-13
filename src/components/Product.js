import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import {
  Container, Card, Col, Row, Button, //ListGroup, ListGroupItem
} from 'react-bootstrap';

// Component

export default function Product(props) {
  const { id } = useParams();

  const [product, setProduct] = useState({});
  const [canEdit, setCanEdit] = useState(false);

  useEffect(() => {
    fetch('/products/' + id).then(res => res.json()).then(data => {
      setProduct(data.product);
      setCanEdit(data.product.seller_id === props.userId);
    });
  }, [id, props.userId]);

  let imageUrl = product && product.image_url ? product.image_url : 'https://via.placeholder.com/300';

  return (
    <Container>

      <Row className="gap-1">

        <Col md="auto">
          <Card>
            <Card.Img variant="top" src={imageUrl} />
            {
              product && product.tagline
                ?
                <Card.Body>
                  <Card.Text>
                    {product.tagline}
                  </Card.Text>
                </Card.Body>
                : ''
            }
          </Card>
        </Col>

        <Col>
          <Card>

            <Card.Header>Details</Card.Header>

            <Card.Body>
              <Card.Title data-testid="product-name">{product.name}</Card.Title>
              {
                product && product.price
                  ? <Card.Subtitle>${product.price.toFixed(2)}</Card.Subtitle>
                  : ''
              }

              {
                product && product.detail
                  ? <Card.Text>{product.detail}</Card.Text>
                  : ''
              }
            </Card.Body>

            {
              canEdit
                ? 'seller actions go here'
                :
                <Card.Body className="d-grid">
                  <Button variant="outline-primary" onClick={() => props.addToCart(product.id)}>
                    add to cart +
                  </Button>
                </Card.Body>
            }

          </Card>
        </Col>

      </Row>

      <Row className="py-4">
        <Col md="auto">
          <Button href="/market" variant="outline-dark">← market</Button>
        </Col>

        <Col></Col>

        <Col md="auto">
          {
            props.isVendor
              ? ''
              : <Button href="/cart" variant="outline-dark">my cart →</Button>
          }
          {
            props.isVendor
              ? <Button href={`/store/${props.vendorId}`} variant="outline-dark">my store →</Button>
              : ''
          }
        </Col>
      </Row>

    </Container>
  );
}