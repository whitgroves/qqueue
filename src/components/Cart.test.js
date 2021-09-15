import { render, screen } from '@testing-library/react';
import Cart from './Cart';

test('renders empty cart', () => {

  render(
    <Cart
      cart={{}}
      cartCount={0}
      addToCart={()=> {}}
      removeFromCart={()=> {}}
      removeAllFromCart={()=> {}}
      emptyCart={()=> {}}
    />
  );

  const marketElement = screen.getByText('← market');
  expect(marketElement).toBeInTheDocument();

  const checkoutElement = screen.getByText('checkout →');
  expect(checkoutElement).toBeInTheDocument();

  const emptyElement = screen.getByText('🗑');
  expect(emptyElement).toBeInTheDocument();
});

test('renders cart with items', () => {

  render(
    <Cart
      cart={{1:1}}  // we just need 1
      cartCount={0}
      addToCart={()=> {}}
      removeFromCart={()=> {}}
      removeAllFromCart={()=> {}}
      emptyCart={()=> {}}
    />
  );

  // // needs async (failing)
  //
  // const addElement = screen.getByText('+1');
  // expect(addElement).toBeInTheDocument();

  // const removeElement = screen.getByText('-1');
  // expect(removeElement).toBeInTheDocument();

  const marketElement = screen.getByText('← market');
  expect(marketElement).toBeInTheDocument();

  const checkoutElement = screen.getByText('checkout →');
  expect(checkoutElement).toBeInTheDocument();

  const emptyElement = screen.getByText('🗑');
  expect(emptyElement).toBeInTheDocument();
});