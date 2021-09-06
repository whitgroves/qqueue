import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Cookies from 'js-cookie';

// Styles

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Navbar, Nav, NavDropdown } from 'react-bootstrap';

// Components

import Market from './components/Market';
import Product from './components/Product';
import Cart from './components/Cart';
import Login from './components/Login';
import Register from './components/Register';

// App

function App() {

  // Time

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []); // Empty dependencies so it doesn't constantly reload.

  // Cart

  // localStorage is used to persist cart between pages.
  // TODO: retrieve from a cookie.
  let storedCart = JSON.parse(localStorage.getItem('cart'));

  const [cart, setCart] = useState(storedCart ? storedCart : {});
  const [itemsInCart, setItemsInCart] = useState(0);

  useEffect(() => {
    if (Object.keys(cart).length > 0) {
      setItemsInCart(Object.values(cart).reduce((a, b) => a + b));
    } else {
      setItemsInCart(0);
    }
  }, [cart]);

  const updateCart = (update) => {
    let hardCopy = { ...cart };
    update(hardCopy);
    setCart(hardCopy);
    // localStorage is used to persist cart between pages.
    // TODO: store as a cookie.
    localStorage.setItem('cart', JSON.stringify(hardCopy));
  }

  const addToCartHandler = (product_id) => {
    const addToCart = (cartCopy) => {
      if (product_id in cartCopy) {
        cartCopy[product_id] += 1;
      } else {
        cartCopy[product_id] = 1;
      }
    }
    updateCart(addToCart);
  }

  const removeFromCartHandler = (product_id) => {
    const removeFromCart = (cartCopy) => {
      cartCopy[product_id] -= 1;
      if (cartCopy[product_id] === 0) {
        delete cartCopy[product_id];
      }
    }
    updateCart(removeFromCart);
  }

  const removeAllFromCartHandler = (product_id) => {
    const removeAllFromCart = (cartCopy) => {
        delete cartCopy[product_id];
    }
    updateCart(removeAllFromCart);
  }

  const emptyCartHandler = () => {
    const emptyCart = (cartCopy) => {
      for (var key in cartCopy) {
        delete cartCopy[key];
      }
    }
    updateCart(emptyCart);
  }

  // Auth
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        access_token: Cookies.get('access_token')
      })
    }).then(res => res.json()).then(data => {
      onLoginHandler(data);
    });
  }, []);  // Only runs once

  const onLoginHandler = (data) => {
    let success = data.status === 200;
    setLoggedIn(success);
    if (success) {
      const expires = (60 * 60) * 1000
      const inOneHour = new Date(new Date().getTime() + expires)
      Cookies.set('access_token', data.access_token, { expires: inOneHour})
    }
  }

  const onRegisterHandler = (data) => {
    console.log(data);
  }

  const registerLinks = () => {
    return (
      <NavDropdown title="register" id="nav_login_dropdown" bg="dark">
        <NavDropdown.Item href="/register/customer">customer</NavDropdown.Item>
        <NavDropdown.Item href="/register/vendor">vendor</NavDropdown.Item>
      </NavDropdown>
    );
  }

  const loginLinks = () => {
    return (
      <NavDropdown title="login" id="nav_login_dropdown" bg="dark">
        <NavDropdown.Item href="/login/customer">customer</NavDropdown.Item>
        <NavDropdown.Item href="/login/vendor">vendor</NavDropdown.Item>
      </NavDropdown>
    );
  }

  const customerAccountLinks = () => {
    return <Nav.Link href="/account">my account</Nav.Link>;
  }

  // Render

  return (
    <div id="wrapper" className="d-grid gap-3">

      <Navbar collapseOnSelect bg="dark" variant="dark" expand="lg" sticky="top">
        <Container>

          <Navbar.Brand href="/home">qqueue</Navbar.Brand>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />

          <Navbar.Collapse id="basic-navbar-nav">

            <Nav className="me-auto">
              <Nav.Link href="/market">market</Nav.Link>
              <Nav.Link href="/about">stores</Nav.Link>
            </Nav>

            <Nav>

              <Nav.Link href="/cart">my cart</Nav.Link>
              { loggedIn ? '' : registerLinks() }{' '}
              { loggedIn ? '' : loginLinks() }{' '}
              { loggedIn ? customerAccountLinks() : '' }
            </Nav>

          </Navbar.Collapse>

        </Container>
      </Navbar>
      
      <Container>
        <BrowserRouter>
          <Switch>

            <Route path="/market">
              <Market addToCart={addToCartHandler}/>
            </Route>

            <Route path="/product/:id">
              <Product addToCart={addToCartHandler}/>
            </Route>

            <Route path="/cart">
              <Cart 
                cart={cart}
                cartCount={itemsInCart}
                addToCart={addToCartHandler}
                removeFromCart={removeFromCartHandler}
                removeAllFromCart={removeAllFromCartHandler}
                emptyCart={emptyCartHandler}
              />
            </Route>

            <Route path="/login/:loginType">
              <Login 
                onLogin={onLoginHandler}
              />
            </Route>

            <Route path="/register/:registrationType">
              <Register 
                onRegister={onRegisterHandler}
              />
            </Route>

          </Switch>
        </BrowserRouter>
      </Container>

      <div className="py-5"/>  {/* so last row isn't covered by footer */}

      <Navbar className="fixed-bottom" bg="dark" variant="dark">
        <Container>
          <Navbar.Text className="text-muted">
            The current time is {currentTime}.
          </Navbar.Text>
          <Navbar.Text className="text-muted">
            <Container >
              {
                itemsInCart === 1
                  ? 'There is 1 item in '
                  : `There are ${itemsInCart} items in `
              }
              <a href="/cart" className="text-muted">my cart</a>.
            </Container>
          </Navbar.Text>
        </Container>
      </Navbar>

    </div>
  );
}

export default App;
