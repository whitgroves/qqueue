import { render, screen, waitFor } from '@testing-library/react';
import { createMemoryHistory } from 'history';
import { Router, Route, useParams, MemoryRouter } from 'react-router-dom';
import { act } from 'react-dom/test-utils';

import Product from './Product';

function renderWithProviders(
  ui,
  {
    route = '/',
    params = '/',
    history = createMemoryHistory({ initialEntries: [route] }),
  } = {}
) {
  console.log("route:", route) // see below
  console.log("params:", params) // see below
  return {
    ...render(
      <Router history={history}>
        <Route path={params}>
          {ui}
        </Route>
      </Router>
    ),
    history,
  };
}

test('renders product data', async () => {

  let testProduct = { 'id': 1, 'name': 'Test Product' }

  const { findByTestId } = renderWithProviders(<Product product={testProduct} />, {
    route: '/product/1',
    params: '/product/:id',
  })

  const name = await waitFor(() => findByTestId('product-name'));

  expect(name).toHaveTextContent(testProduct.name);

});

// const routerParams = { useParams }

// jest.spyOn(routerParams, 'useParams').mockReturnValue({ id: 1 });

// test('renders product data', () => {

//   let testProduct = { 'id': 1, 'name': 'Test Product' }

//   render(
//     <Product product={testProduct} /> , { wrapper: MemoryRouter }
//   );

//   const nameElement = screen.getByTestId('product-name');
//   expect(nameElement).toBeInTheDocument();
//   expect(nameElement.innerText).toEqual(testProduct.name);

// });
