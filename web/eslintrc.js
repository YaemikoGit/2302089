module.exports = {
  env: {
    node: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:security/recommended',
  ],
  plugins: ['security'],
  rules: {
    'no-unused-vars': 'warn',  // warn about unused variables
    'eqeqeq': 'error',         // enforce strict equality
    'no-console': 'warn',      // warn on console statements
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-fs-filename': 'error',
    // Add more security or style rules here
  },
};