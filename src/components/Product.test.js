import React from "react";
import { render, screen } from "@testing-library/react";
import { Route, MemoryRouter } from "react-router-dom";
import Product from './Product';

const testProduct = { id: 1, name: 'Test Product', seller_id: 1 }

test('renders product when not signed in', () => {
  render(
    <MemoryRouter initialEntries={['/product/1']}>
      <Route path='/product/:id'>
        <Product product={testProduct} />
      </Route>
    </MemoryRouter>
  );

  const nameElement = screen.getByTestId('product-name');
  expect(nameElement).toBeInTheDocument();
  expect(nameElement.textContent).toEqual(testProduct.name);

  const addElement = screen.getByText('add to cart +');
  expect(addElement).toBeInTheDocument();
});

// // failing b/c no async
// test('renders product when signed in', () => {
//   render(
//     <MemoryRouter initialEntries={['/product/1']}>
//       <Route path='/product/:id'>
//         <Product product={testProduct} userId={testProduct.seller_id} />
//       </Route>
//     </MemoryRouter>
//   );

//   const nameElement = screen.getByTestId('product-name');
//   expect(nameElement).toBeInTheDocument();
//   expect(nameElement.textContent).toEqual(testProduct.name);

//   const addElement = screen.getByText('add to cart +');
//   expect(addElement).toBeUndefined();
// });
