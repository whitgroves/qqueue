import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter, Route, Switch, Redirect, } from 'react-router-dom';
import Cookies from 'js-cookie';

// Styles

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Navbar, Nav, NavDropdown } from 'react-bootstrap';

// Components

import Market from './components/Market';
import Product from './components/Product';
import Cart from './components/Cart';
import AuthCard from './components/AuthCard';

// App

function App(props) {

  // Time

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []); // Empty dependencies so it doesn't constantly reload.

  // Cart TODO: move this logic into Cart.js

  let storedCart = Cookies.get('qq_cart');
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

    // A cookie is used to persist the cart between pages.
    Cookies.set('qq_cart', JSON.stringify(hardCopy));
  }

  const addToCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      if (product_id in cartCopy) {
        cartCopy[product_id] += 1;
      } else {
        cartCopy[product_id] = 1;
      }
    })
  }

  const removeFromCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      cartCopy[product_id] -= 1;
      if (cartCopy[product_id] === 0) {
        delete cartCopy[product_id];
      }
    });
  }

  const removeAllFromCartHandler = (product_id) => {
    updateCart((cartCopy) => {
      delete cartCopy[product_id];
    });
  }

  const emptyCartHandler = () => {
    updateCart((cartCopy) => {
      for (var key in cartCopy) {
        delete cartCopy[key];
      }
    });
  }

  // Auth

  let storedToken = props.testToken ? props.testToken : Cookies.get('qq_token');
  let storedId = props.testUser ? props.testUser.id : Cookies.get('qq_user_id');
  let storedEmail = props.testUser ? props.testUser.email : Cookies.get('qq_user_email');

  const [token, setToken] = useState(storedToken ? storedToken : '');
  const [userId, setUserId] = useState(storedId ? parseInt(storedId) : 0); // There are no users with ID 0.
  const [userEmail, setUserEmail] = useState(storedEmail ? storedEmail : '');

  const [loggedIn, setLoggedIn] = useState(token !== '');

  const onAuthHandler = useCallback((data) => {
    setLoggedIn(true);

    if (data && data.token) {
      setToken(data.token);
      setUserId(data.user.id);
      setUserEmail(data.user.email);

      const inOneHour = new Date(new Date().getTime() + (60 * 60) * 1000);

      Cookies.set('qq_token', data.token, { expires: inOneHour });
      Cookies.set('qq_user_id', data.user.id, { expires: inOneHour });
      Cookies.set('qq_user_email', data.user.email, { expires: inOneHour });
    }
  }, []);

  useEffect(() => {
    if (token && userId > 0) {
      fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: token,
          id: userId,
        })
      }).then(res => res.json()).then(data => onAuthHandler(data));
    }
  }, [token, userId, onAuthHandler]);

  const onLogoutHandler = () => {
    setLoggedIn(false);

    setToken('');
    setUserId(0);
    setUserEmail('');

    Cookies.remove('qq_token');
    Cookies.remove('qq_user_id');
    Cookies.remove('qq_user_email');

    Cookies.remove('qq_cart');  // clear the cart on logout
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
              {loggedIn ? <Nav.Link href="/orders">orders</Nav.Link> : ''}
            </Nav>

            <Nav>
              <Nav.Link href="/cart" data-testid="nav-link-cart">cart</Nav.Link>
              {loggedIn ? '' : <Nav.Link href="/login">login</Nav.Link>}
              {loggedIn ? '' : <Nav.Link href="/register">register</Nav.Link>}
              {
                loggedIn
                  ?
                  <NavDropdown title={userEmail} id="nav-account-dropdown" >
                    <NavDropdown.Item href="/account">account</NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="/logout" onClick={onLogoutHandler}>
                      logout
                    </NavDropdown.Item>
                  </NavDropdown>
                  : ''
              }
            </Nav>

          </Navbar.Collapse>

        </Container>
      </Navbar>

      <Container>
        <BrowserRouter>
          <Switch>

            <Route path="/market">
              <Market
                isVendor={false}
                addToCart={addToCartHandler}
              />
            </Route>

            <Route path="/product/:id">
              <Product
                isVendor={false}
                vendorId={userId}
                addToCart={addToCartHandler}
              />
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

            <Route path="/register">
              <AuthCard
                isRegistration={true}
                onAuthenticated={onAuthHandler}
              />
            </Route>

            <Route path="/login">
              <AuthCard
                isRegistration={false}
                onAuthenticated={onAuthHandler}
              />
            </Route>

            <Route path="/logout">
              <Redirect to="/home" />
            </Route>

            <Route path="/404">
              Looks like you got here by accident. Try one of these:{' '}
              <a href="/home">home</a>{' '}
              <a href="/market">market</a>{' '}
              <a href="/orders">orders</a>{' '}
            </Route>

          </Switch>
        </BrowserRouter>
      </Container>

      <div className="py-5" />  {/* so last row isn't covered by footer */}

      <Navbar className="fixed-bottom" bg="dark" variant="dark">
        <Container>
          <Navbar.Text className="text-muted">
            The current time is {currentTime}.
          </Navbar.Text>
          <Navbar.Text className="text-muted">
            <Container >
              {
                itemsInCart === 1
                  ? 'There is 1 item in my '
                  : `There are ${itemsInCart} items in my `
              }
              <a href="/cart" className="text-muted">cart</a>.
            </Container>
          </Navbar.Text>
        </Container>
      </Navbar>

    </div>
  );

}

export default App;
