import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';

// Styles

import 'bootstrap/dist/css/bootstrap.min.css';
import {
  Container, Card, Col, Row, Button, //ListGroup, ListGroupItem
} from 'react-bootstrap';

// Component

export default function Product(props) {

  // Editing

  let history = useHistory();

  const { id } = useParams();
  const { userId } = props;

  const [product, setProduct] = useState(props.product ? props.product : {});
  const [canEdit, setCanEdit] = useState(false);

  useEffect(() => {
    fetch('/products/' + id).then(res => res.json()).then(data => {
      if (data.status === 200) {
        setProduct(data.product);
        setCanEdit(data.product.seller_id === userId);
      }
      //  else {
      //   history.push('/market');  // redirect to market if id not in database
      // }
    });
  }, [id, userId, history]);

  let imageUrl = product && product.image_url ? product.image_url : 'https://via.placeholder.com/300';

  const [showError, setShowError] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    setShowError(error.length !== 0);
  }, [error]);

  const unlist = () => {
    fetch(`/products/deactivate/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: props.userId,
      })
    }).then(res => res.json()).then(data => {
      if (data['status'] === 500) {
        setError(data['error']);
      } else {
        setError('');
        history.push('/market/');
      }
    })
  }

  // Render

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
                ?
                <Card.Body className="d-grid">
                  <Button variant="outline-danger" onClick={() => unlist()}>
                    unlist
                  </Button>
                </Card.Body>
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
          <Button href="/cart" variant="outline-dark">my cart →</Button>
        </Col>
      </Row>

    </Container>
  );
}