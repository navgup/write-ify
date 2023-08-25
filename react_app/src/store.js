import { createStore } from 'redux';

// Initial state
const initialState = {
  authToken: null, // Initialize the token to null
};

// Reducer
const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_AUTH_TOKEN':
      return { ...state, authToken: action.token };
    default:
      return state;
  }
};

// Create the store
const store = createStore(rootReducer);

export default store;