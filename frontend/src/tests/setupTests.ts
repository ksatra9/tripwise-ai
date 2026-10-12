import '@testing-library/jest-dom';

// Polyfill window.scrollTo if needed in jsdom
if (typeof window !== 'undefined') {
  window.scrollTo = () => {};
}
